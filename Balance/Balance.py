#Import libraries 
import datetime
import telebot
from telebot import types
import sqlite3

#Our token
token = '5586466061:AAF9ElE5pbYeQnPCSQ6D4EnBbtuubuE26Rw'
bot = telebot.TeleBot(token)


# Actions when user write start command
@bot.message_handler(commands=['start'])
def start(message):
    
    # Connect to our database
    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS MEMBER(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), FIRST_NAME VARCHAR(50), LAST_NAME VARCHAR(50))')
    conn.commit()
    
    # Select our user id for find hin in our table
    cursor.execute(f'SELECT USER_ID FROM MEMBER WHERE USER_ID = {message.chat.id}')
    
    if cursor.fetchone() is None:
        
        # Add user in table
        cursor.execute('INSERT INTO MEMBER (USER_ID, FIRST_NAME, LAST_NAME) VALUES (?,?,?)', (message.chat.id, message.from_user.first_name, message.from_user.last_name))
        conn.commit()
        
        # Send welcome message
    bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name} {message.from_user.last_name}')

    # Close connection with database
    conn.close()

cmd_income = 'income'
cmd_expense = 'expense'
dir_show_income = 'showincomes'
dir_show_expense = 'showexpenses'
dir_sum_income = 'incomessum'
dir_avg_income = 'averageincomes'
dir_count_income = 'countincomes'
dir_sum_expense = 'expensesum'
dir_avg_expense = 'averageexpenses'
dir_count_expense = 'countexpenses'

dirs = {
    dir_show_income: ('Period options', cmd_income, 'all'),
    dir_show_expense: ('Period options', cmd_expense, 'all'),
    dir_sum_income: ('Options for sum', cmd_income, 'sum'),
    dir_sum_expense: ('Options for sum', cmd_expense, 'sum'),
    dir_avg_income: ('Options for average', cmd_income, 'avg'),
    dir_avg_expense: ('Options for average', cmd_expense, 'avg'),
    dir_count_income: ('Options for count', cmd_income, 'count'),
    dir_count_expense: ('Options for count', cmd_expense, 'count')
}

# Manual for our user
@bot.message_handler(commands=['help'])
def help(message):
    text = f'/{cmd_income} and data - Add info about incomes in database, ex: /{cmd_income} 1000\n' \
           f'/{cmd_expense} and data - Add info about expenses in database, ex: /{cmd_expense} 1000\n' \
           f'/{dir_show_income} - Show options with incomes\n' \
           f'/{dir_show_expense} - Show options with expenses\n' \
           f'/{dir_sum_income} - Show options for sum of incomes\n' \
           f'/{dir_avg_income} - Show options for average sum of incomes\n' \
           f'/{dir_count_income} - SHow options for count of incomes\n' \
           f'/{dir_sum_expense} - Show options for sum of expenses\n' \
           f'/{dir_avg_expense} - Show options for average sum of expenses\n' \
           f'/{dir_count_expense} - Show options for count of expenses'

    bot.send_message(message.chat.id, text=text)


def insert_data(table_name, data, user):
    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    date = datetime.date.today()
    cursor.execute(f'INSERT INTO {table_name}(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (user, data, date))
    conn.commit()


# Function for add information about user's income
@bot.message_handler(commands=['income'])
def income(message):
    insert_data('INCOME', message.text[8::], message.chat.id)


# Function for add information about user's expenses
@bot.message_handler(commands=['expense'])
def expense(message):
    insert_data('EXPENSE', message.text[9::], message.chat.id)


def create_markup(table: str, kind: str,):
    markup = types.InlineKeyboardMarkup()
    period_list = [0, 12, 6, 3, 1]
    for period in period_list:
        if period == 0:
            text = f'Total {"" if kind == "all" else kind + " of"} {table}s'
        else:
            text = f'{table.title() + "s" if kind == "all" else kind.title() + " of " + table} for {period} months'
        markup.add(types.InlineKeyboardButton(text=text, callback_data=f'{table};{kind};{period}'))
    return markup

def send_message_to_bot(bot, message, cmd):
    parms = dirs[cmd]
    bot.send_message(message.chat.id, parms[0], reply_markup=create_markup(parms[1], parms[2]))

# Make buttons for navigate in incomes table
@bot.message_handler(commands=[dir_show_income])
def show_incomes(message):
    send_message_to_bot(bot, message, dir_show_income)


# Make buttons for navigate in expenses table
@bot.message_handler(commands=[dir_show_expense])
def show_expenses(message):
    send_message_to_bot(bot, message, dir_show_expense)


# Make buttons for send info about total sum of income in different period
@bot.message_handler(commands=[dir_sum_income])
def incomes_sum(message):
    send_message_to_bot(bot, message, dir_sum_income)


# Make buttons for send info about average sum of incomes in different period
@bot.message_handler(commands=[dir_avg_income])
def incomes_average(message):
    send_message_to_bot(bot, message, dir_avg_income)


# Make buttons for send info about count of incomes in defferent period
@bot.message_handler(commands=[dir_count_income])
def count_of_incomes(message):
     send_message_to_bot(bot, message, dir_count_income)


# Make buttons for send info about sum of expenses in defferent period
@bot.message_handler(commands=[dir_sum_expense])
def incomes_sum(message):
    send_message_to_bot(bot, message, dir_sum_expense)


# Make buttons for send info about average sum of expenses in different period
@bot.message_handler(commands=[dir_avg_expense])
def incomes_average(message):
    send_message_to_bot(bot, message, dir_avg_expense)


# Make buttons for send info about count of expenses in different period
@bot.message_handler(commands=[dir_count_expense])
def count_of_incomes(message):
    send_message_to_bot(bot, message, dir_count_expense)


def get_value(user, table_name: str, operation: str, interval: int):
    filter = f'AND "DATE" BETWEEN DATETIME("now", "-{interval} month") AND DATETIME("now", "localtime") ORDER BY "DATE"' if int(interval) > 0 else ''
    if operation == 'all':
        scope = '*'
    elif operation == 'avg':
        scope = 'AVG(TOTAL)'
    elif operation == 'sum':
        scope = 'SUM(TOTAL)'
    elif operation == 'count':
        scope = 'COUNT(TOTAL)'
    else:
        raise Exception('Not supported function')

    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {scope} FROM {table_name} WHERE USER_ID = {user} {filter}')
    data = round(cursor.fetchone()[0], 2) if operation != 'all' else cursor.fetchall()
    conn.close()
    return data


# Make actions when user tap on button
@bot.callback_query_handler(func=lambda call: True)
def callback_options(call):

    # Make a variable of user's id
    user = call.message.chat.id

    if call.data.startswith(cmd_income) or call.data.startswith(cmd_expense):
        cmd_parms = call.data.split(';')
        data = get_value(user, cmd_parms[0].upper(), cmd_parms[1], cmd_parms[2])
        tail = '' if cmd_parms[2] == '0' else f'for {cmd_parms[2]} months'
        if type(data) == int or type(data) == float:
            text = f'{cmd_parms[1].title()} of {cmd_parms[0]} {tail}: {data}'
            bot.send_message(
                call.message.chat.id,
                text=text
            )
        else:
            for value in data:
                text = f'ID: {value[0]} - Total: {value[2]}, date: {value[3]}'
                bot.send_message(
                    call.message.chat.id,
                    text=text
                )


if __name__ == '__main__':
    bot.infinity_polling()
