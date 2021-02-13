import random
import database

from string import digits

MENU_LOGIN = """
1. Create an account
2. Log into account
0. Exit"""
MENU_USER = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""


class Card:

    def __init__(self):
        self.card_number = ''.join(Card.__generate_card_number())
        self.pin = ''.join(random.choices(digits, k=4))
        self.balance = 0.0

    @staticmethod
    def __generate_card_number():
        card_num_digits = random.choices(digits, k=9)
        card_number = list('400000')
        card_number.extend(card_num_digits)
        sum_ = Card.__luhn_sum(card_number)
        last_digit = 10 - sum_ % 10
        if last_digit == 10:
            last_digit = 0
        card_number.append(str(last_digit))
        return card_number

    @staticmethod
    def __luhn_sum(number):
        def get_double_digit(digit):
            double_digit = int(digit) * 2
            return double_digit if double_digit <= 9 else double_digit - 9
        sum_ = 0
        for i, digit in enumerate(number, 1):
            sum_ += int(digit) if i % 2 == 0 else get_double_digit(digit)
        return sum_

    @staticmethod
    def luhn_check(number):
        return True if Card.__luhn_sum(number) % 10 == 0 else False


conn = database.connect()
database.create_table(conn)
loop = 1
while loop == 1:
    print(MENU_LOGIN)
    choice = input()
    print()
    if choice == '1':
        new_card = Card()
        database.add_card(conn, new_card.card_number, new_card.pin)
        print("Your card has been created")
        print("Your card number:")
        print(new_card.card_number)
        print("Your card PIN:")
        print(new_card.pin)
    elif choice == '2':
        print("Enter your card number:")
        user_card_number = input()
        print("Enter your PIN")
        user_pin = input()
        if not database.check_card_pin(conn, user_card_number, user_pin):
            print("Wrong card number or PIN!")
            continue
        print("You have successfully logged in!")
        while True:
            print(MENU_USER)
            choice = input()
            print()
            if choice == '1':
                print("Balance:", database.get_balance(conn, user_card_number)[0])
            elif choice == '2':
                income = int(input("Enter income: "))
                database.add_income(conn, income, user_card_number)
                print("Income was added!")
            elif choice == '3':
                print('Transfer')
                receiver_card_number = input("Enter card number: ")
                if not Card.luhn_check(list(receiver_card_number)):
                    print('Probably you made a mistake in the card number. Please try again!')
                    continue
                elif not database.check_card_existance(conn, receiver_card_number):
                    print("Such a card does not exist.")
                    continue
                transfer_amount = int(input("Enter how much money you want to transfer: "))
                if database.get_balance(conn, user_card_number)[0] - transfer_amount < 0:
                    print("Not enough money!")
                    continue
                database.add_income(conn, -transfer_amount, user_card_number)
                database.add_income(conn, transfer_amount, receiver_card_number)
                print('Success!')
            elif choice == '4':
                database.close_account(conn, user_card_number)
                print("The account has been closed!")
                break
            elif choice == '5':
                del user_card_number
                del user_pin
                break
            elif choice == '0':
                loop = 0
                break
            else:
                print("Unknown command")
    elif choice == '0':
        loop = 0
    elif choice == 'show cards':
        print(database.get_all_cards(conn))
    else:
        print("Unknown command")
conn.close()
print("Bye!")
