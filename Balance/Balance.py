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
    
    else:
        # Send welcome message, if user exists
        bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name} {message.from_user.last_name}')
    
    # Close connection with database
    conn.close()
    
# Manual for our user
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text='/income and data - Add info about incomes in database, ex: /income 1000\n/expense and data - Add info about expenses in database, ex: /expense 1000\n/showincomes - Show options with incomes\n/showexpenses - Show options with expenses\n/incomessum - Show options for sum of incomes\n/averageincomes - Show options for average sum of incomes\n/countincomes - SHow options for count of incomes\n/expensessum - Show options for sum of expenses\n/averageexpenses - Show options for average sum of expenses\n/countexpenses - Show options for count of expenses')
                         
# Function for add information about user's income
@bot.message_handler(commands=['income'])
def income(message):
    
    # Connect to database
    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    
    # Make variables consists from date and info about user's income
    income_data = message.text[8::]
    date = datetime.date.today()
    
    # Create table of incomes if not exists
    cursor.execute('CREATE TABLE IF NOT EXISTS INCOME(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    
    # Add main information in table
    cursor.execute('INSERT INTO INCOME(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (message.chat.id, income_data, date))
    conn.commit()
    
    # Close connection with database
    conn.close()
    
# Function for add information about user's expenses
@bot.message_handler(commands=['expense'])
def expense(message):
    
    # Connect to database
    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    
    # Create table of expenses if not exists
    cursor.execute('CREATE TABLE IF NOT EXISTS EXPENSE(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    
    # Make variables consists from date and info about user's expense
    expense_data = message.text[9::]
    date = datetime.date.today()
    
    # Add main information in database
    cursor.execute('INSERT INTO EXPENSE(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (message.chat.id, expense_data, date))
    conn.commit()
    
    # Close connection with database
    conn.close()

cmd_income = 'income'
cmd_expense = 'expense'
cmd_income_sum = 'sum_income'
cmd_expense_sum = 'sum_expense'
cmd_income_avg = 'avg_income'
cmd_expense_avg = 'avg_expense'
cmd_income_count = 'count_income'
cmd_expense_count = 'count_expense'


# Make buttons for navigate in incomes table
@bot.message_handler(commands=['showincomes'])
def show_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Total incomes', callback_data=f'{cmd_income};all;0'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 12 months', callback_data=f'{cmd_income};all;12'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 6 months', callback_data=f'{cmd_income};all;6'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 3 months', callback_data=f'{cmd_income};all;3'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 1 month', callback_data=f'{cmd_income};all;1'))
    
    # Reply our markup in chat
    bot.send_message(
        message.chat.id,
        text='Period options',
        reply_markup=markup
    )


# Make buttons for navigate in expenses table
@bot.message_handler(commands=['showexpenses'])
def show_expenses(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Total expenses', callback_data=f'{cmd_expense};all;0'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 12 months', callback_data=f'{cmd_expense};all;12'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 6 months', callback_data=f'{cmd_expense};all;6'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 3 months', callback_data=f'{cmd_expense};all;3'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 1 month', callback_data=f'{cmd_expense};all;1'))
    
    # Reply our markup in chat
    bot.send_message(
        message.chat.id,
        text='Period options',
        reply_markup=markup
    )


# Make buttons for send info about total sum of income in different period
@bot.message_handler(commands=['incomessum'])
def incomes_sum(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Sum of incomes', callback_data=f'{cmd_income_sum};sum;0'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 12 months', callback_data=f'{cmd_income_sum};sum;12'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 6 months', callback_data=f'{cmd_income_sum};sum;6'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 3 months', callback_data=f'{cmd_income_sum};sum;3'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 1 month', callback_data=f'{cmd_income_sum};sum;1'))
    
    # Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Options for sum',
        reply_markup=markup
    )    


# Make buttons for send info about average sum of incomes in different period
@bot.message_handler(commands=['averageincomes'])
def incomes_average(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes', callback_data=f'{cmd_income_avg};avg;0'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 12 months', callback_data=f'{cmd_income_avg};avg;12'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 6 months', callback_data=f'{cmd_income_avg};avg;6'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 3 months', callback_data=f'{cmd_income_avg};avg;3'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 1 month', callback_data=f'{cmd_income_avg};avg;1'))
    
    # Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Average options',
        reply_markup=markup
    )


# Make buttons for send info about count of incomes in defferent period
@bot.message_handler(commands=['countincomes'])
def count_of_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Count of incomes', callback_data=f'{cmd_income_count};count;0'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 12 months', callback_data=f'{cmd_income_count};count;12'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 6 months', callback_data=f'{cmd_income_count};count;6'))
    markup.add(types.InlineKeyboardButton(text='Coumt of incomes for 3 months', callback_data=f'{cmd_income_count};count;3'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 1 month', callback_data=f'{cmd_income_count};count;1'))
    
    # Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Count options',
        reply_markup=markup
    )    


# Make buttons for send info about sum of expenses in defferent period
@bot.message_handler(commands=['expensessum'])
def incomes_sum(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Sum of expenses', callback_data=f'{cmd_expense_sum};sum;0'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 12 months', callback_data=f'{cmd_expense_sum};sum;12'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 6 months', callback_data=f'{cmd_expense_sum};sum;6'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 3 months', callback_data=f'{cmd_expense_sum};sum;3'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 1 month', callback_data=f'{cmd_expense_sum};sum;1'))
    
    # Reply markup in database
    bot.send_message(
        message.chat.id,
        text='Options for sum',
        reply_markup=markup
    )    


# Make buttons for send info about average sum of expenses in different period
@bot.message_handler(commands=['averageexpenses'])
def incomes_average(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses', callback_data=f'{cmd_expense_avg};avg;0'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 12 months', callback_data=f'{cmd_expense_avg};avg;12'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 6 months', callback_data=f'{cmd_expense_avg};avg;6'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 3 months', callback_data=f'{cmd_expense_avg};avg;3'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 1 month', callback_data=f'{cmd_expense_avg};avg;1'))
    
    # Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Average options',
        reply_markup=markup
    )


# Make buttons for send info about count of expenses in different period
@bot.message_handler(commands=['countexpenses'])
def count_of_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Count of expenses', callback_data=f'{cmd_expense_count};count;0'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 12 months', callback_data=f'{cmd_expense_count};count;12'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 6 months', callback_data=f'{cmd_expense_count};count;6'))
    markup.add(types.InlineKeyboardButton(text='Coumt of expenses for 3 months', callback_data=f'{cmd_expense_count};count;3'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 1 month', callback_data=f'{cmd_expense_count};count;1'))
    bot.send_message(
        message.chat.id,
        text='Count options',
        reply_markup=markup
    )


def get_single_value(user, table_name: str, operation: str, interval: int):
    if operation == 'avg':
        func = 'AVG'
    elif operation == 'sum':
        func = 'SUM'
    elif operation == 'count':
        func = 'COUNT'
    else:
        raise Exception('Not supported function')
    if int(interval) > 0:
        filter = f'AND "DATE" BETWEEN DATETIME("now", "-{interval} month") AND DATETIME("now", "localtime") ORDER BY "DATE"'
    else:
        filter = ''

    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {func}(TOTAL) FROM {table_name} WHERE USER_ID = {user} {filter}')
    data = cursor.fetchone()[0]
    conn.close()
    return data


def get_total_value(user, table_name: str, interval: int):
    if int(interval) > 0:
        filter = f'AND "DATE" BETWEEN DATETIME("now", "-{interval} month") AND DATETIME("now", "localtime") ORDER BY "DATE"'
    else:
        filter = ''
    conn = sqlite3.connect('Balance/Balance.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE USER_ID = {user} {filter}')
    data = cursor.fetchall()
    conn.close()
    return data


# Make actions when user tap on button
@bot.callback_query_handler(func=lambda call: True)
def callback_options(call):

    # Make a variable of user's id
    user = call.message.chat.id

    if call.data.startswith(cmd_income) or call.data.startswith(cmd_expense):
        cmd_parms = call.data.split(';')
        if len(cmd_parms) < 4:

            # Select full info from our table
            data = get_total_value(user, cmd_parms[0].upper(), cmd_parms[2])

            # Send messages consist's from info about incomes (id, total sum, date of add in database)
            for income in data:
                bot.send_message(
                    call.message.chat.id,
                    text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
                )

    elif call.data.startswith(cmd_income_sum) or call.data.startswith(cmd_income_count) or call.data.startswith(cmd_income_avg):
        cmd_parms = call.data.split(';')
        if len(cmd_parms) < 4:
            data = get_single_value(user, 'INCOME', cmd_parms[1], cmd_parms[2])
            if cmd_parms[2] == '0':
                tail = ''
            else:
                tail = f'for {cmd_parms[2]} months'

            bot.send_message(
                call.message.chat.id,
                text=f'{cmd_parms[1].title()} of incomes {tail}: {data}'
                )

    elif call.data.startswith(cmd_expense_avg) or call.data.startswith(cmd_expense_sum) or call.data.startswith(cmd_expense_count):
        cmd_parms = call.data.split(';')
        if len(cmd_parms) < 4:

            data = get_single_value(user, 'EXPENSE', cmd_parms[1], cmd_parms[2])
            if cmd_parms[2] == '0':
                tail = ''
            else:
                tail = f'for {cmd_parms[2]} months'

            bot.send_message(
                call.message.chat.id,
                text=f'{cmd_parms[1].title()} of expenses {tail}: {data}'
                )


if __name__ == '__main__':
    bot.infinity_polling()
