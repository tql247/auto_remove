import psycopg2

from auto_remove.config import USER, PASSWORD, DB_SERVER, DB_PORT, DB_NAME
from auto_remove.utils.handler import handle


def main():
    connection = psycopg2.connect(
                    user=USER,
                    password=PASSWORD,
                    host=DB_SERVER,
                    port=DB_PORT,
                    database=DB_NAME
                )

    handle(connection)


if __name__ == '__main__':
    main()
