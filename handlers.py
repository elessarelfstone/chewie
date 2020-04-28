import os
from functools import wraps

from telegram import Update

from docxparser import parse_talks, upload_talks
from settings import ADMIN_ID
from utils import fpath


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id == ADMIN_ID:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def transcript_file_upload_handler(update: Update, context):
    # check if it's me
    new_file = update.message.document.file_name
    f = update.message.document.get_file().download(custom_path=fpath(new_file))
    talks = parse_talks(f)
    try:
        upload_talks(talks)
    except Exception:
        update.message.reply_text('Something went wrong')
    reply_text = '{} talks have been added'.format(len(talks))
    update.message.reply_text(reply_text)




