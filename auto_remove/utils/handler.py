from auto_remove.utils.helper import moving_video
import pytz
from datetime import datetime, timedelta


def video_remove(connection):
    today = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    start_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    moving_video(connection, start_date, end_date)
    return True


def handle(connection):
    success = video_remove(connection)
    if success:
        print('Transfer successfully')
        return True

    return False
