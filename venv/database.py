import sqlite3

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS card_numbers(
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0); 
            """
INSERT_CARD = 'INSERT INTO card_numbers (number, pin) VALUES (?, ?);'
CHECK_CARD_PIN = 'SELECT * FROM card_numbers WHERE number = ? AND pin = ?;'
CHECK_CARD_EXISTANCE = 'SELECT * FROM card_numbers WHERE number = ?;'
GET_BALANCE = 'SELECT balance FROM card_numbers WHERE number = ?;'
GET_ALL_CARDS = 'SELECT * FROM card_numbers;'
ADD_INCOME = 'UPDATE card_numbers SET balance = balance + ? WHERE number = ?;'
CLOSE_ACCOUNT = 'DELETE FROM card_numbers WHERE number = ?;'

def connect():
    return sqlite3.connect('card_numbers.db')

def create_table(connection):
    connection.execute(CREATE_TABLE)
    connection.commit()

def add_card(connection, number, pin):
    connection.execute(INSERT_CARD, (number, pin))
    connection.commit()

def check_card_pin(connection, number, pin):
    return 0 if connection.execute(CHECK_CARD_PIN, (number, pin)).fetchone() == None else 1

def check_card_existance(connection, number):
    return 0 if connection.execute(CHECK_CARD_EXISTANCE, (number, )).fetchone() == None else 1

def get_balance(connection, number) :
    return connection.execute(GET_BALANCE, (number, )).fetchone()

def get_all_cards(connection):
    return connection.execute(GET_ALL_CARDS).fetchall()

def add_income(connection, amount, number):
    connection.execute(ADD_INCOME, (amount, number))
    connection.commit()

def close_account(connection, number):
    connection.execute(CLOSE_ACCOUNT, (number, ))
    connection.commit()