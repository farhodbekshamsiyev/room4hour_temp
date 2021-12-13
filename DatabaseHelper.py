import sqlite3


class InitDatabase:
    __connection = ''
    __is_db_created = False

    def __init__(self) -> None:
        if not self.__is_db_created:
            self.__connection = sqlite3.connect('data.db')
            with self.__connection:
                cursor = self.__connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rooms
                    (id INTEGER PRIMARY KEY,
                    room_number INTEGER)
                    """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders
                    (id INTEGER PRIMARY KEY,
                    room_id INTEGER,
                    start_time VARCHAR(23),
                    end_time VARCHAR(23),
                    person_full_name VARCHAR(50),
                    person_email VARCHAR(50),
                    )
                    """)

                self.__connection.commit()
                InitDatabase.__is_db_created = True
                print(f'Database \"orders\" initialized successfully')
        else:
            self.__connection = sqlite3.connect('data.db')
            print('Database already initialized')

    def get_all_rooms(self) -> list[str]:
        with self.__connection:
            cursor = self.__connection.cursor()
            cursor.execute("""
                    SELECT * FROM orders
                    """)
            a = cursor.fetchall()
            self.__connection.commit()
        return a

    def get_rooms_by_no(self, room_num: int) -> list[str]:
        with self.__connection:
            cursor = self.__connection.cursor()
            cursor.execute(f"""
                    SELECT * FROM orders
                    WHERE room_number = {room_num}
                    """)
            a = cursor.fetchall()
            self.__connection.commit()
        return a

    def book_room(self, **room):
        with self.__connection:
            cursor = self.__connection.cursor()
            cursor.execute(f"""
                    INSERT INTO orders(room_number, start_time, end_time, person_id)
                        VALUES(
                            '{room['room_number']}', 
                            '{room['start_time']}', 
                            '{room['end_time']}', 
                            '{room['person_id']}'
                            )
                    """)
            self.__connection.commit()
