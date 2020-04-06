import os
import sys
import argparse
from flask import Flask, request

print(dir(request))

#parser = argparse.ArgumentParser()
#parser.add_argument("input_string")
#args = parser.parse_args()

input_string = sys.argv[0]
print(input_string)
place_preposition = ['in', 'In', 'at', 'At', 'on', 'On', 'from', 'From', 'of', 'Of', 'to', 'To', 'across', 'Across']
exceptions_list = ["I", "President", "The", "This", "That", "Those", "These", "In", "On", "From", "At", "Of", "Nation", "For", "So", "All", "Even"]
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

print("\n\n")


def process_str(string):
    to_remove_chars = ".,;!?()[]\{\}/\\=&$#@"
    data = []
    new_string = ""
    for char in string:
        if not char in to_remove_chars:
            new_string += char
    s_list = new_string.split(" ")
    for index in range(0, len(s_list)):
       out_dict = {}
       if s_list[index][0].isupper() and s_list[index] not in exceptions_list:
            if s_list[index] in out_dict.keys():
                print(s_list[index] + " entry is repeated!")
            else:
                out_dict['name'] = s_list[index]
                out_dict['position'] = index
                out_dict['entity'] = 'unknown'
            data.append(out_dict)
    data = detect_person(data)
    data = detect_weekday(data)
    data = detect_place(s_list, data)
    data = detect_acronym(data)
    return detect_first_word(s_list, data)


def detect_person(data):
    for index in range(len(data)):
        new_dict = {}
        if index + 1 < len(data):
            if data[index]['position'] - data[index+1]['position'] == -1:
                new_dict['name'] = data[index]['name'] + " " + data[index+1]['name']
                new_dict['position'] = data[index]['position']
                new_dict['entity'] = 'person'
                data.append(new_dict)
                data.remove(data[index+1])
                data.remove(data[index])
    return data


def detect_place(s_list, data):
    for index in range(len(s_list)-1):
        if s_list[index] in place_preposition and s_list[index + 1][0].isupper():
            for item in data:
                 if item['entity'] == 'unknown':
                     if item['name'] == s_list[index + 1]:
                         item['entity'] = 'place'
    return data


def detect_weekday(data):
    for item in data:
        if item['entity'] == 'unknown' and item['name'] in week_days:
            item['entity'] = 'day'
    return data


def detect_first_word(s_string, data):
    if s_string[0] == data[0]['name']:
        data.remove(data[0])
    return data


def detect_acronym(data):
    for item in data:
        count = 0
        for char in item['name']:
            if char.isupper():
                count += 1
        if item['entity'] == 'unknown' and count >= 3:
            item['entity'] = 'acronym'
    return data


#print(process_str(args.input_string))
