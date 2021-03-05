import psycopg2

from auto_remove.config import TIME_RANGE_PROTECT_START, TIME_RANGE_PROTECT_END, SPECIFIC_DATE_INIT, \
    SPECIFIC_TIME_INIT_START, SPECIFIC_TIME_INIT_END


def get_video_file_name(connection, start_date, end_date):
    if not connection:
        return []

    # query db
    cursor = connection.cursor()
    query = f"""
                select file_uri, start_point 
                from video vi 
                where true
                and vi.start_point::date between date '{start_date}' and date '{end_date}'
                and not (vi.start_point::time between time '{TIME_RANGE_PROTECT_START}' and '{TIME_RANGE_PROTECT_END}')
                order by vi.start_point desc
            """
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()

    # extract location name from file name
    list_video_name = []
    for row in record:
        list_video_name.append(row[0])

    return list_video_name


def get_video_by_location_datetime(connection, start_date=None, end_date=None):
    if not connection:
        return []

    # query db
    cursor = connection.cursor()
    query = f"""
                select file_name, start_point 
                from video_information vi 
                where true
                and (
                    file_name like '%CANTHO%'
                    or 
                    file_name like '%MYTHO11%'
                )
                and vi.start_point::date between date '{SPECIFIC_DATE_INIT}' and date '{SPECIFIC_DATE_INIT}'
                and not (vi.start_point::time between time '{SPECIFIC_TIME_INIT_START}' and '{SPECIFIC_TIME_INIT_END}')
                order by vi.start_point desc
            """
    cursor.execute(query)
    record = cursor.fetchall()
    cursor.close()

    # extract location name from file name
    list_video_name = []
    for row in record:
        list_video_name.append(row[0])

    return list_video_name


def mark_skipping(connection, start_date, end_date):
    if not (connection and start_date and end_date):
        print('Fail!')
        return False

    # query db
    cursor = connection.cursor()
    query = f"""
                update video
                set deleted_at = timezone('utc', now())
                where true 
                and start_point ::date between date '{start_date}' and date '{end_date}'
                and not (
                    start_point::time between time '{TIME_RANGE_PROTECT_START}' 
                    and '{TIME_RANGE_PROTECT_END}'
                )
                and state = 0
            """

    try:
        cursor.execute(query)

        # commit changes
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        return False
    finally:
        cursor.close()
        return True


def mark_skipping_specific(connection, start_date=None, end_date=None):
    if not (connection and start_date and end_date):
        print('Fail!')
        return False

    # query db
    cursor = connection.cursor()
    query = f"""
                update video_state
                set state_video_state = 5
                where id_video in (
                    select id_video
                    from video_information vi 
                    where true
                    and (
                        file_name like '%CANTHO%'
                        or 
                        file_name like '%MYTHO11o%'
                    )
                    and vi.start_point::date between date '{SPECIFIC_DATE_INIT}' and date '{SPECIFIC_DATE_INIT}'
                    and not (
                        vi.start_point::time between time '{SPECIFIC_TIME_INIT_START}' 
                        and '{SPECIFIC_TIME_INIT_END}'
                    )
                    order by vi.start_point asc 
                )
                and state_video_state = 0
            """

    try:
        cursor.execute(query)

        # commit changes
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        return False
    finally:
        cursor.close()
        return True
