import utils
import sqlite3

import psycopg


class DatabaseHelper:
    HOSTNAME = 'localhost'
    DATABASE = 'postgres'
    USERNAME = 'postgres'
    PASSWORD = 'root'
    PORT = 5432

    __connection = ''
    __cursor = ''
    __is_db_created = False

    def __init__(self) -> None:
        self.get_connection()
        self.__cursor = self.__connection.cursor()
        if not DatabaseHelper.__is_db_created:
            self.__cursor.execute("""
                    CREATE SEQUENCE IF NOT EXISTS rooms_id_seq;
                    """)

            self.__cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rooms(
                        id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('rooms_id_seq'),
                        room_number INTEGER
                        );
                    """)

            self.__cursor.execute("""
                    CREATE SEQUENCE IF NOT EXISTS orders_id_seq;
                    """)

            a = self.__cursor.execute("""
                    SELECT COUNT(room_number) FROM rooms
                    """)
            if a == 0:
                for i in range(5):
                    self.__cursor.execute(f"""
                            INSERT INTO rooms(room_number)
                                VALUES('{i + 1}');
                            """)

            self.__cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders(
                        id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('orders_id_seq'),
                        room_id INTEGER NOT NULL,
                        start_time timestamp NOT NULL,
                        end_time timestamp NOT NULL,
                        person_email TEXT  NOT NULL,
                        person_full_name TEXT
                        );
                    """)

            # cursor.execute("""
            #         ALTER TABLE orders
            #         ADD CONSTRAINT fk_orders_rooms FOREIGN KEY (room_id) REFERENCES rooms(id);
            #         """)
            self.__connection.commit()
            DatabaseHelper.__is_db_created = True
            print(f'Database initialized successfully')
        else:
            print('Database already initialized')

    def __del__(self):
        self.__connection.close()

    def get_free_rooms(self, start_time: str, end_time: str) -> list[str]:
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(f"""
                select * from rooms r 
                where r.id not in 
                    (
                        SELECT R.id FROM rooms AS R LEFT JOIN orders AS O ON R.id = O.room_id
                        WHERE O.start_time
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS')
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                            OR O.end_time
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS')
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                        group by R.id
                    )
                    """)
        a = self.__cursor.fetchall()
        self.__connection.commit()
        return a

    def check_room_is_free(self, room_number: int, start_time: str, end_time: str):
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(f"""
                SELECT R.id FROM rooms AS R LEFT JOIN orders AS O ON R.id = O.room_id
                        WHERE R.room_number = {room_number} and O.start_time 
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS')
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                            OR O.end_time
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS')
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                        group by R.id
                    """)
        a = self.__cursor.fetchone()
        self.__connection.commit()
        return True if a is None else False

    def get_ordered_data(self, room_number: int, start_time: str, end_time: str):
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(f"""
                SELECT O.* FROM rooms AS R LEFT JOIN orders AS O ON R.id = O.room_id
                        WHERE R.room_number = {room_number} and O.start_time 
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS') 
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                            OR O.end_time 
                            between to_timestamp('{start_time}', 'YYYY-MM-DD HH24:MI:SS') 
                            and to_timestamp('{end_time}', 'YYYY-MM-DD HH24:MI:SS')
                    """)
        a = self.__cursor.fetchone()
        self.__connection.commit()
        return a

    def get_all_orders(self):
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(f"""
                        SELECT room_id, start_time, end_time, person_full_name, person_email FROM orders 
                            """)
        a = self.__cursor.fetchall()
        self.__connection.commit()
        return a

    def book_room(self, **room):
        self.__cursor = self.__connection.cursor()
        if self.check_room_is_free(room['room_id'], room['start_time'], room['end_time']):
            self.__cursor.execute(f"""
                INSERT INTO orders(room_id, start_time, end_time, person_full_name, person_email)
                    VALUES(
                        '{room['room_id']}',
                        '{room['start_time']}',
                        '{room['end_time']}',
                        '{room['full_name']}',
                        '{room['e_mail']}'
                        )
                """)
            # To send e-mail user must provide valid email address and password!
            # utils.instant_email(room['e_mail'])
            print('Room successfully booked')
        else:
            print("Please, enter valid date and time for booking!")
            _, room_id, s_time, e_time, mail, full_name = self.get_ordered_data(
                room['room_id'],
                room['start_time'],
                room['end_time']
            )
            print(f"The room number {room_id} is booked by {full_name} from {s_time} to {e_time}")
            print('Try again!')
        self.__connection.commit()

    def get_connection(self):
        self.__connection = psycopg.connect(
            host=self.HOSTNAME,
            dbname=self.DATABASE,
            user=self.USERNAME,
            password=self.PASSWORD,
            port=self.PORT)
