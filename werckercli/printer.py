# -*- coding: UTF-8 -*-
#!/usr/bin/python

import datetime
import re

# from clint.textui import puts, colored
from werckercli.cli import term, puts


def store_highest_length(list_lengths, row, props=None):

    if props:
        values_list = props
    else:
        values_list = row

    # print row, props

    for i in range(len(values_list)):

        if props:
            try:
                value = str(row[props[i]])
            except KeyError:
                value = '─'
        else:
            value = str(row[i])

        length = len(value) + 1

        if length > list_lengths[i]:
            list_lengths[i] = length

    # lines, columns = get_terminal_size()

    # total_length = sum(list_lengths)
    # print total_length


def print_line(list_lengths, row, props=None):

    line = u"│ "

    if props:
        values_list = props
    else:
        values_list = row

    for i in range(len(values_list)):
        if i > 0:
            line += u"│ "

        if props:
            try:
                value = str(row[props[i]])
            except KeyError:
                value = u'-'
            value = value
        else:
            value = row[i]

        value = value.encode("utf-8")

        value = value.ljust(list_lengths[i])
        if value.startswith(u"passed "):
            value = term.green(value)
        elif value.startswith(u"failed "):
            value = term.red(value)

        line += value

    line += u"│"

    puts(line)


def print_hr(lengths, first=False):

    line = u""
    length = len(lengths)
    for i in range(length):

        value = lengths[i]

        if i == 0:
            if first:
                line += u"┌─"
            else:
                line += u"├─"
        else:
            if first:
                line += u"┬─"
            else:
                line += u"┼─"

        line += value * u"─"
        if i == length - 1:
            if first:
                line += u"┐"
            else:
                line += u"┤"
    puts(line)


def format_date(dateString):
    return (datetime.datetime(
        *map(int,
             re.split('[^\d]', dateString)[:-1]
             )
    )).strftime("%x %X")


def print_progress(percentage, prefix="progress", add_percentage=True):

    bar_width = term.width - len(prefix) - 3

    if add_percentage:
        bar_width -= 6
    per_percent = bar_width/100.0

    filled = int(per_percent * percentage)

    bar = prefix + u" ["
    bar += term.black_on_white + (u"-" * filled) + term.normal + ((bar_width - filled) * u".")
    bar += u"]"

    if add_percentage:
        bar += " {percentage:3.1f}%".format(percentage=percentage)

    puts(bar)
