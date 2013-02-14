#!/usr/bin/python
# -*- coding: UTF-8 -*-

from clint.textui import puts, colored


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


def print_line(list_lengths, row, props=None):

    line = "│ "

    if props:
        values_list = props
    else:
        values_list = row

    for i in range(len(values_list)):
        if i > 0:
            line += "│ "

        if props:
            try:
                value = row[props[i]]
            except KeyError:
                value = '-'
            value = str(value)
        else:
            value = str(row[i])

        value = value.ljust(list_lengths[i])
        if value.startswith("passed "):
            value = colored.green(value)
        elif value.startswith("failed "):
            value = colored.red(value)

        line += value

    line += "│"

    puts(line)


def print_hr(lengths, first=False):

    line = ""
    length = len(lengths)
    for i in range(length):

        value = lengths[i]

        if i == 0:
            if first:
                line += "┌─"
            else:
                line += "├─"
        else:
            if first:
                line += "┬─"
            else:
                line += "┼─"

        line += value * "─"
        if i == length - 1:
            if first:
                line += "┐"
            else:
                line += "┤"
        # ((sum(lengths) + (len(lengths) * 3) - 1) * "─") + "|"
    puts(line)
