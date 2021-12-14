# This is a sample Python script.
import datetime
import os

from DatabaseHelper import DatabaseHelper


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def show_menu():
    print('1 -> Book a room')
    print('2 -> Check room by number, whether it is booked')
    print('3 -> Show all orders')
    print('4 -> quit')


def run_app(data):
    quit_app = True
    while quit_app:
        show_menu()
        a = int(input('Please choose one option from menu! :  '))
        print('Please insert valid data!')
        if a == 1:
            room_number = int(input('Enter room number for booking : '))
            starttime = input('Enter valid starting time like a template \"2021-01-01 12:00:00\" : ')
            endtime = input('Enter valid ending time like a template \"2021-01-01 12:00:00\" : ')
            fullname = input('Enter your full name : ')
            email = input('Enter valid e-mail address like a template \"example@mail.com\" :  ')
            data.book_room(
                room_id=room_number,
                start_time=starttime,
                end_time=endtime,
                full_name=fullname,
                e_mail=email)
        elif a == 2:
            room_number = int(input('Enter room number for checking : '))
            starttime = input('Enter valid starting time like a template \"2021-01-01 12:00:00\" : ')
            endtime = input('Enter valid ending time like a template \"2021-01-01 12:00:00\" : ')
            if not data.check_room_is_free(room_number, starttime, endtime):
                _, room_id, s_time, e_time, mail, full_name = data.get_ordered_data(
                    room_number,
                    starttime,
                    endtime
                )
                print(f"The room number {room_id} is booked by {full_name} from {s_time} to {e_time}")
                print('Try again!')
        elif a == 3:
            orders = data.get_all_orders()
            for i, data in enumerate(orders):
                room_id, s_time, e_time, full_name, mail = data
                print(f"{i}) Room:{room_id}, Name: {full_name}, Start time:{s_time}, End time:{e_time}, E-mail: {mail}")
            print("--------------------------------endline--------------------------------")
        elif a == 4:
            quit_app = False
        else:
            print('Chooses again!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to \"Room booking app\"')
    db = DatabaseHelper()
    run_app(db)

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
