from datetime import datetime, time, timedelta
from functools import wraps

import pytz
from telegram import Update
from telegram.ext import CallbackContext

from db import load_random_transcript
from docxparser import parse_transcripts, upload_transcripts
from settings import ADMIN_ID
from utils import temp_fpath


def restricted(func):
    """ Check if handler called by admin"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id == ADMIN_ID:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def transcript_file_upload_handler(update: Update, context: CallbackContext):
    """ Upload docx file with transcripts."""
    new_file = update.message.document.file_name
    f = update.message.document.get_file().download(custom_path=temp_fpath(new_file))
    transcripts = parse_transcripts(f)
    try:
        upload_transcripts(transcripts)
    except Exception as e:
        update.message.reply_text('Something went wrong')
        raise
    reply_text = '{} transcripts have been added'.format(len(transcripts))
    update.message.reply_text(reply_text)


def movie_callback(context):
    """ Send random transcript. Callback for job """
    job = context.job
    transcript = load_random_transcript()
    context.bot.send_message(job.context, text=transcript)


def movie_handler(update: Update, context):
    """ Send random transcript. Response to request """
    transcript = load_random_transcript()
    update.message.reply_text(transcript)


def set_transcript_job(update: Update, context):
    """  """
    try:
        chat_id = update.message.chat_id
        # parse from argument time to schedule
        _st = datetime.strptime(context.args[0], '%H:%M:%S').time()
        now = datetime.now(tz=pytz.timezone('Asia/Oral'))
        dt = now.replace(hour=_st.hour, minute=_st.minute, second=_st.second)

        # build job movie id
        job_id = 'movie_{}'.format(dt.strftime('%H_%M_%S'))
        new_movie_job = context.job_queue.run_daily(movie_callback, dt, context=chat_id)
        context.user_data[job_id] = new_movie_job
        update.message.reply_text('Time set for random transcript.')
    except (ValueError, IndexError):
        update.message.reply_text('Usage: /set_transcript_job <time>. <time> format - H:M:S')


def unset_transcript_jobs(update, context):
    """ Remove the job if the user changed their mind. """
    to_remove = []
    for k, _ in context.user_data.items():
        if 'movie' in k:
            job = context.user_data[k]
            job.schedule_removal()
            to_remove.append(k)

    if to_remove:
        for k in to_remove:
            del context.user_data[k]

    update.message.reply_text('Timer successfully unset!')
