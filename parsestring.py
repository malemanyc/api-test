import os
import sys
import argparse
from flask import Flask, request

# Define lists to help identify entities
place_preposition = ['in', 'In', 'at', 'At', 'on', 'On', 'from', 'From', 'of', 'Of', 'to', 'To', 'across', 'Across']
exceptions_list = ["I", "President", "The", "This", "That", "Those", "These", "In", "On", "From", "At", "Of", "Nation", "For", "So", "All", "Even"]
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Check if string to parse has content
if len(sys.argv) > 1:
    input_string = str(sys.argv[1])
else:
    print([])


def process_str(string):
    """
    Takes ra string as input and returns json format containing all names
    detected in input and their entity if able to clasify.
    """
    to_remove_chars = ".,;!?()[]\{\}/\\=&$#@'"
    data = []
    # Clean inpus string from any special character
    new_string = ""
    empty = detect_empty_string(string)
    if empty:
        return []
    for char in string:
        if not char in to_remove_chars:
            new_string += char
    # Split input string by spaces 
    s_list = new_string.split(" ")
    for index in range(0, len(s_list)):
       out_dict = {}
       # Detect all words in input string that start by caps
       if s_list[index][0].isupper() and s_list[index] not in exceptions_list:
            if s_list[index] in out_dict.keys():
                print(s_list[index] + " entry is repeated!")
            # Create dictionary with base information
            else:
                out_dict['name'] = s_list[index]
                out_dict['position'] = index
                out_dict['entity'] = 'unknown' 
            data.append(out_dict)
    # Classify eac word selected into data list
    data = detect_person(data)
    data = detect_weekday(data)
    data = detect_place(s_list, data)
    data = detect_acronym(data)
    return detect_first_word(s_list, data)


def detect_empty_string(string):
    """
    Detect is input string is empty
    """
    if len(string) == 0:
        return True
    else:
        return False


def detect_person(data):
    """
    Rudimentary detection for a person's name.
    When 2 consecutive words start with capital letters, assume it is a person
    name and surname. Unite them into one only item in data. Label as 'person'
    """
    for index in range(len(data)):
        new_dict = {}
        if index + 1 < len(data):
            # Identify if  consecutive words
            if data[index]['position'] - data[index+1]['position'] == -1:
                # Create new dictionary item with composed name
                new_dict['name'] = data[index]['name'] + " " + data[index+1]['name']
                new_dict['position'] = data[index]['position']
                new_dict['entity'] = 'person'
                data.append(new_dict)
                # Remove old items
                data.remove(data[index+1])
                data.remove(data[index])
    return data


def detect_place(s_list, data):
    """
    Determine item is a place when it follows one of the 
    prepositions for place.
    """
    for index in range(len(s_list)-1):
        if s_list[index] in place_preposition and s_list[index + 1][0].isupper():
            for item in data:
                 if item['entity'] == 'unknown':
                     if item['name'] == s_list[index + 1]:
                         item['entity'] = 'place'
    return data


def detect_weekday(data):
    """
    Determine item is weekday when found in 
    week_day list.
    """
    for item in data:
        if item['entity'] == 'unknown' and item['name'] in week_days:
            item['entity'] = 'day'
    return data


def detect_first_word(s_string, data):
    """
    Determine first word, always capital letter, is or is not a name
    to include in the registry.
    """
    if s_string and data:
        if s_string[0] == data[0]['name']:
            data.remove(data[0])
        return data
    else:
        return []

def detect_acronym(data):
    """
    Detect is item is an acronym due to multiple characters
    being uppercase.
    """
    for item in data:
        count = 0
        for char in item['name']:
            if char.isupper():
                count += 1
        if item['entity'] == 'unknown' and count >= 3:
            item['entity'] = 'acronym'
    return data
