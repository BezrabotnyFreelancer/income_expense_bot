#Import libraries 
import datetime
import telebot
from telebot import types
import sqlite3
import db_methods
from db_methods import Scope, Budgets
from enum import Enum


#Our token
token = '5586466061:AAF9ElE5pbYeQnPCSQ6D4EnBbtuubuE26Rw'
bot = telebot.TeleBot(token)


# Actions when user write start command
@bot.message_handler(commands=['start'])
def start(message):
    db_methods.validate_member(message.chat.id, message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name} {message.from_user.last_name}')


dir_income = 'income'
dir_expense = 'expense'
dir_show_income = 'showincomes'
dir_show_expense = 'showexpenses'
dir_sum_income = 'incomessum'
dir_avg_income = 'averageincomes'
dir_count_income = 'countincomes'
dir_sum_expense = 'expensesum'
dir_avg_expense = 'averageexpenses'
dir_count_expense = 'countexpenses'

dirs = {
    dir_show_income: ('Period options', Budgets.INCOME, Scope.ALL),
    dir_show_expense: ('Period options', Budgets.EXPENSE, Scope.ALL),
    dir_sum_income: ('Options for sum', Budgets.INCOME, Scope.SUM),
    dir_sum_expense: ('Options for sum', Budgets.EXPENSE, Scope.SUM),
    dir_avg_income: ('Options for average', Budgets.INCOME, Scope.AVG),
    dir_avg_expense: ('Options for average', Budgets.EXPENSE, Scope.AVG),
    dir_count_income: ('Options for count', Budgets.INCOME, Scope.COUNT),
    dir_count_expense: ('Options for count', Budgets.EXPENSE, Scope.COUNT)
}


# Manual for our user
@bot.message_handler(commands=['help'])
def help(message):
    text = f'/{dir_income} and data - Add info about incomes in database, ex: /{dir_income} 1000\n' \
           f'/{dir_expense} and data - Add info about expenses in database, ex: /{dir_expense} 1000\n' \
           f'/{dir_show_income} - Show options with incomes\n' \
           f'/{dir_show_expense} - Show options with expenses\n' \
           f'/{dir_sum_income} - Show options for sum of incomes\n' \
           f'/{dir_avg_income} - Show options for average sum of incomes\n' \
           f'/{dir_count_income} - SHow options for count of incomes\n' \
           f'/{dir_sum_expense} - Show options for sum of expenses\n' \
           f'/{dir_avg_expense} - Show options for average sum of expenses\n' \
           f'/{dir_count_expense} - Show options for count of expenses'

    bot.send_message(message.chat.id, text=text)


def validate_data(parm):
    try:
        data = int(parm)
        return data
    except ValueError:
        raise Exception('Incorrect value type')


# Function for add information about user's income
@bot.message_handler(commands=[dir_income])
def income(message):
    data = validate_data(message.text[8::])
    db_methods.insert_data(Budgets.INCOME, data, message.chat.id)


# Function for add information about user's expenses
@bot.message_handler(commands=[dir_expense])
def expense(message):
    data = validate_data((message.text[9::]))
    db_methods.insert_data(Budgets.EXPENSE, data, message.chat.id)


def create_markup(table: Budgets, kind: Scope):
    markup = types.InlineKeyboardMarkup()
    period_list = [0, 12, 6, 3, 1]

    for period in period_list:
        if period == 0:
            text = f'Total {"" if kind == Scope.ALL else kind.name.lower() + " of"} {table.name.lower()}s'
        else:
            text = f'{table.name.title() + "s" if kind == Scope.ALL else kind.name.title() + " of " + table.name.lower()} for {period} months'
        markup.add(types.InlineKeyboardButton(text=text, callback_data=f'{table.name};{kind.name};{period}'))
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


# Make actions when user tap on button
@bot.callback_query_handler(func=lambda call: True)
def callback_options(call):

    # Make a variable of user's id
    user = call.message.chat.id

    if call.data.startswith(Budgets.INCOME.name) or call.data.startswith(Budgets.EXPENSE.name):
        cmd_parms = call.data.split(';')
        data = db_methods.get_data(user, Budgets[cmd_parms[0]], Scope[cmd_parms[1]], cmd_parms[2])
        tail = '' if cmd_parms[2] == '0' else f'for {cmd_parms[2]} months'
        if type(data) == int or type(data) == float:
            text = f'{cmd_parms[1].title()} of {cmd_parms[0].lower()} {tail}: {data}'
            bot.send_message(
                call.message.chat.id,
                text=text
            )
        else:
            for value in data:
                text = f'ID: {value[0]} - Total: {value[3]}, date: {value[2]}'
                bot.send_message(
                    call.message.chat.id,
                    text=text
                )


if __name__ == '__main__':
    bot.infinity_polling()
