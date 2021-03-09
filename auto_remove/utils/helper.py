import os
import shutil

from auto_remove.access.access import get_video_file_name, get_video_by_location_datetime, mark_skipping_specific, \
    mark_skipping
from auto_remove.config import PENDING_FOLDER, RECYCLE_BIN_FOLDER


def file_transferring(file_list, from_dir, to_dir):
    """
    Transfer/Moving (not copy) file that list in file_name from from_dir to to_dir
    :param to_dir: string
    :param from_dir: string
    :type file_list: list of string
    :return TRUE or FALSE
    """
    if not os.path.isdir(to_dir) or not os.path.isdir(from_dir):
        print("Path is invalid")
        return False

    num_file = len(file_list)
    for idx, file_name in enumerate(file_list):
        print(f'\r {idx}/{num_file}: {file_name} is tranferring')
        if not os.path.exists(os.path.join(from_dir, file_name)):
            print(f'\r {file_name} not exist')
        else:
            file_path = os.path.join(from_dir, file_name)
            to_path = os.path.join(to_dir, file_name)
            shutil.move(file_path, to_path)

    return True


def get_video_by_specific(connection):
    return get_video_by_location_datetime(connection)


def moving_video(connection, start_date, end_date):
    list_video = get_video_file_name(connection, start_date, end_date)
    file_transferring(list_video, PENDING_FOLDER, RECYCLE_BIN_FOLDER)
    mark_skipping(connection, start_date, end_date)
    # list_video = get_video_by_specific(connection)
    # file_transferring(list_video, PENDING_FOLDER, RECYCLE_BIN_FOLDER)
    # mark_skipping_specific(connection, start_date, end_date)
