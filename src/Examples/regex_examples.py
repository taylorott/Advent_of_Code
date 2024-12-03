#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.abspath(inspect.getfile(inspect.currentframe()))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh


path = currentdir

#                   REGEX GUIDE
#
#           \d     whole numbers( 0-9 )(single digit)  
#                  \d = 7,  \d\d = 77
#                   
#           \w     alphanumeric character                       
#                  \w\w\w\w  = geek
#                    \w\w\w != geek
#
#            *     0 or more characters
#                  s*  = _,s,ss,sss,ssss…..
#
#            +     1 or more characters
#                  s+ = s,ss,sss,ssss…..
#
#            ?     0 or 1 character
#                  s?  = _ or s
#
#           {m}    occurs “m” times
#                  sd{3} = sddd
#
#          {m,n}   min “m” and max “n” times
#                  sd{2,3}=sdd or sddd
#
#           \W     symbols 
#                  \W = %
# 
# [a-z] or [0-9]   character set
#                  geek[sy]  = geeky
#                  geek[sy] != geeki
#
#           .      matches any character except a newline
#                  
#           ^      matches pattern only at start of the string
#
#           $      matches pattern only at end of the string
#
#           |      used to specify multiple patterns
#
#                  a|b = a     a|b = b     a|b != c
#
#           \      used to escape special characters
#
#           Examples include:  \'   \(   \)   \[   \]
#
#        [^...]    matches any single character not in brackets
#
#         (...)    matches whatever regular expression is inside the parentheses
#
#
#                   CONSTRUCTING A REGEX
#           my_regex = r'type up your regex here'
#                
#                   USING A REGEX
#           match_iter =  re.finditer(my_regex,str_in)  Returns a iterator of MATCH objects
#
#           for my_match in match_iter:
#               my_match.group()  generates string of the entire match
#               my_match.group(n)  generates string of whatever is contained in
#                                  the nth parentheses of the match
#
#           match_list = re.findall(my_regex,str_in) Returns a list of matches (list of list)
#           for my_match in match_list:
#               print(my_match)     my_match[n] is the string of whatever is contained in
#                                               in the nth parentheses of the match 

def example01():
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.


    required_keys = ['byr','iyr','eyr','hgt','hcl','ecl','pid']
    regex_dict = {  'byr':r'\d{4}',
                    'iyr':r'\d{4}',
                    'eyr':r'\d{4}',
                    'hgt':r'\d*(cm|in)',
                    'hcl':r'#([0-9]|[a-f]){6}',
                    'ecl':r'amb|blu|brn|gry|grn|hzl|oth',
                    'pid':r'\d{9}'}

    for key in regex_dict:
        regex_dict[key]=re.compile(regex_dict[key])

    data = bh.parse_split_by_emptylines(path,fname)

    num_valid = 0

    for item in data:
        data_dict = bh.convert_strings_to_dict(item)

        is_valid = True
        for key in required_keys:
            if not key in data_dict:
                is_valid = False
                break

            val = data_dict[key]

            m = regex_dict[key].match(val)
            
            if m is None:
                is_valid = False
                break

            if not(m.start()==0 and m.end() == len(val)):
                is_valid = False
                break

            if key=='byr' and (int(val)<1920 or 2002<int(val)):
                is_valid = False
                break

            if key=='iyr' and (int(val)<2010 or 2020<int(val)):
                is_valid = False
                break
                
            if key=='eyr' and (int(val)<2020 or 2030<int(val)):
                is_valid = False
                break

            if key=='hgt':
                if val[-2:]=='cm' and (int(val[0:-2])<150 or 193<int(val[0:-2]) ):
                    is_valid = False
                    break
                if val[-2:]=='in' and (int(val[0:-2])<59 or 76<int(val[0:-2]) ):
                    is_valid = False
                    break
                
        if is_valid:
            num_valid+=1

    print(num_valid)


if __name__ == '__main__':
    example01()
    

