import logging
import pickle
from datetime import timedelta
from time import time


from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (Updater, Job, MessageHandler,
                          Filters, CommandHandler, CallbackContext)

from handlers import movie_handler, transcript_file_upload_handler, set_transcript_job, unset_transcript_jobs
from settings import TOKEN, JOBS_PICKLE_PATH, JOB_STATE, JOB_DATA


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

GET_RANDOM_TRANSCRIPT = '🎞 Random transcript'


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(GET_RANDOM_TRANSCRIPT)
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Hi! How can I help you?",
        reply_markup=get_base_reply_keyboard(),
    )


def do_service(update: Update, context: CallbackContext):

    text = update.message.text
    if text == GET_RANDOM_TRANSCRIPT:
        movie_handler(update, context)


def load_jobs(jq):
    with open(JOBS_PICKLE_PATH, 'rb') as fp:
        while True:
            try:
                next_t, data, state = pickle.load(fp)
            except EOFError:
                break  # loaded all jobs

            # New object with the same data
            job = Job(**{var: val for var, val in zip(JOB_DATA, data)})

            # Restore the state it had
            for var, val in zip(JOB_STATE, state):
                attribute = getattr(job, var)
                getattr(attribute, 'set' if val else 'clear')()

            job.job_queue = jq
            next_t -= time()  # convert from absolute to relative time
            jq._put(job, next_t)


def save_jobs(jq):

    with jq._queue.mutex:  # in case job_queue makes a change
        if jq:
            job_tuples = jq._queue.queue
        else:
            job_tuples = []

        with open(JOBS_PICKLE_PATH, 'wb') as fp:
            for next_t, job in job_tuples:

                # This job is always created at the start
                if job.name == 'save_jobs_job':
                    continue

                # Threading primitives are not pickleable
                data = tuple(getattr(job, var) for var in JOB_DATA)
                state = tuple(getattr(job, var).is_set() for var in JOB_STATE)

                # Pickle the job
                pickle.dump((next_t, data, state), fp)


def save_jobs_job(context):
    save_jobs(context.job_queue)


def main():

    print("start")

    updater = Updater(TOKEN, use_context=True)

    job_queue = updater.job_queue

    job_queue.run_repeating(save_jobs_job, timedelta(minutes=1))

    # handler = MessageHandler(Filters.all, test_message_handler)
    test_handler = MessageHandler(Filters.document, transcript_file_upload_handler)

    # updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(test_handler)
    updater.dispatcher.add_handler(CommandHandler("start", do_start))
    updater.dispatcher.add_handler(CommandHandler("set_transcript_job",
                                                  set_transcript_job,
                                                  pass_args=True,
                                                  pass_job_queue=True,
                                                  pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler("unset_transcript_jobs", unset_transcript_jobs, pass_chat_data=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,
                                                  do_service))

    try:
        load_jobs(job_queue)

    except FileNotFoundError:
        # First run
        pass

    updater.start_polling()
    updater.idle()

    save_jobs(job_queue)


if __name__ == '__main__':
    main()


