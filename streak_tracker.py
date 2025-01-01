# STREAK TRACKER

import os
import csv
import datetime
import time
from random import randrange


FILE = 'streak.csv'
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

months = ["Unknown",
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]


greetings = ["Howdy",
             "Yo",
             "Yoooooooooo,",
             "My man,",
             "Hi",
             "Hello",
             "G'day",
             "Good day",
             "Hey",
             "Greetings",
             "Fancy seeing you here",
             "Ayyye",
             "'Sup",
             "Wassup"]


small_talk = ["Did you see the game last night?",
              "How are you today?",
              "Hope you're having a wonderful day.",
              "Have a great day!",
              "How's your day been so far?",
              "Have a good one!",
              "Living the dream?",
              "How are you?",
              "How are ya?",
              "I trust you're well.",
              "Are you vibing, son?",
              "Good to see you!",
              "How about this weather, huh?",
              "How's your crypto today?",
              "Kicking goals as usual?",
              "Done anything cool today?",
              "You look cute today.",
              "See any funny cat videos today? No? Okay :/",
              "Are you a Zoe or a Zelda today?",
              "I've run out of small talk so just pretend I said something cool here, mmmk?"]


SQUARE = '▩'
CGREEN  = '\33[32m'
CRED    = '\033[91m'
CBOLD   = '\33[1m'

CEND    = '\033[0m'


def get_user():
    if os.environ.get('USER'):
        return os.environ.get('USER')
    elif os.environ.get('USERNAME'):
        return os.environ.get('USERNAME')
    else:
        return "USER"


def get_last_row_and_lines():
    last_line = [None, None, None, None]
    line_count = 0
    with open(FILE, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            last_line = row
            line_count += 1
    if line_count == 0:
        last_line = [None, None, yesterday, None]
    return last_line, line_count


# Work out last streak break
def update_last_streak_break(today_row):
    streak_continued = str(today_row[0])
    if streak_continued == "False":
        last_streak_break = today
    else: 
        last_streak_break = today_row[2]
    return [streak_continued, today, last_streak_break, None]


def append_list_as_row(list_of_elem):
    f = open(FILE, 'a+')
    writer = csv.writer(f)
    writer.writerows([list_of_elem])


# Print out the squares
def print_squares(lines):
    print()
    with open(FILE, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        squares = ' '
        for row in datareader:
            if count == 7:
                print()
                count = 0
                squares = ' '

            if row[1][8:] == "01":
                month = int(row[1][5:7])
                if month == 0:
                    month = 12
                count = 0
                squares = ' '
                time.sleep(3/lines)
                print('\n\n == ' + months[month] + ' ==\n')

            if row[0] == "True":
                squares += CGREEN + SQUARE + CEND + ' '
            else:
                squares += CRED + SQUARE + CEND + ' '
            print(squares, end="\r"),
            count += 1
            time.sleep(3/lines)
    print('\n')


def get_streak_length(today_row):
    streak_break_string = str(today_row[2])
    today_string = str(today_row[1])
    streak_length = datetime.datetime.strptime(today_string, "%Y-%m-%d") - datetime.datetime.strptime(streak_break_string, "%Y-%m-%d")
    return streak_length.days


# Print streak length
def print_streak_length(today_row):
    streak_length_int = get_streak_length(today_row)
    streak_break_string = str(today_row[2])
    print("Your current streak is " + str(streak_length_int), end="")
    if streak_length_int == 1:
        print(" day", end='')
    else:
        print(" days", end='')
    if streak_length_int > 0:
        print(", and it started on " + pretty_date(streak_break_string) + ".\n")
    else:
        print(". Don't let today's slip-up become a habit.")
        time.sleep(4)
        print("\n\nTomorrow is a new day and a new opportunity for you to keep improving.\n\n")
        time.sleep(2)
    time.sleep(2)


def pretty_date(ugly_date):
    day = ugly_date[8:]
    month = int(ugly_date[5:7])
    month = months[month]
    year = ugly_date[:4]

    if day[0] != "1":
        if day[1] == "1":
            day += "st"
        elif day[1] == "2":
            day += "nd"
        elif day[1] == "3":
            day += "rd"
        else:
            day += "th"
    if day[0] == "0":
        day = day[1:]

    return "the " + day + " of " + month + ", " + year


# How many times you've broke your streak
def count_streak_breaks():
    count = 0
    with open(FILE, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] == "False":
                count += 1
    return count


def print_longest_streak():
    longest_streak = get_longest_streak()
    print("Your longest streak so far is " + str(longest_streak) + " day", end='')
    if longest_streak == 1:
        print('.\n')
    else:
        print('s.\n')


def print_percentages(streak_breaks, lines):
    percentage = (float(streak_breaks) / lines) * 100
    if percentage > 0:
        time.sleep(2)
        print("You've broken your streak " + str(round(percentage)) + "% of the time.\n")   
    time.sleep(2) 
    if percentage == 100:
        print("Bruh, are you even trying?\n")
    elif percentage < 50 and percentage > 20:
        print("You're still under fifty percent, let's try to get it even lower!")
    elif percentage > 20:
        print("You're doing really well. Try to get it under 20%!!")
    else:
        print(CBOLD + "I'm proud of you." + CEND)
    print('\n')
    time.sleep(2)


def print_streak_breaks(streak_breaks):
    if streak_breaks == 0:
        print("You've never broken your streak.\n")
    else:
        print("In that time you've broken your streak " + str(streak_breaks) + " time", end='')
        if streak_breaks == 1:
            print('.\n')
        else:
            print('s.\n')


def print_stats(lines, streak_breaks):
    print_streak_length(today_row)
    print("You've been tracking your progress with this script for " + str(lines), end='')
    if lines == 1:
        print(" day.\n")
    else:
        print(" days.\n")
    time.sleep(2)
    print_streak_breaks(streak_breaks)
    print_longest_streak()
    print_percentages(streak_breaks, lines)


def append_today_if_necessary(last_row, today_row, lines):
    f = open(FILE, 'a+')
    if last_row[1] != today_row[1].strftime('%Y-%m-%d'):
        today_row[0] = (input('\nDid you keep your streak today? Y/N\n').capitalize() == 'Y')
        today_row = update_last_streak_break(today_row)
        today_row[3] = get_streak_length(today_row)
        append_list_as_row(today_row)
        lines += 1
    else:
        print("\n\nYou've already tracked your progress today, but I'll still show you your streak ;)\n")
    f.close()
    return lines, today_row


def get_longest_streak():
    with open(FILE, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        longest = 0 
        for row in datareader:
            if int(row[3]) > int(longest):
                longest = row[3]
    return longest


# MAIN

print("\n\n" + greetings[randrange(0,len(greetings))] + " " + get_user().capitalize() + ". " + small_talk[randrange(0,len(small_talk))])
time.sleep(2)
f = open(FILE, 'a+')
last_row, lines = get_last_row_and_lines()
today_row = [False, today, last_row[2], None]
lines, today_row = append_today_if_necessary(last_row, today_row, lines)
print_squares(lines)
print_stats(lines, count_streak_breaks())