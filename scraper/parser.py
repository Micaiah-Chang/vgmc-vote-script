'''This file reads from new_info.txt or asks for some file
and then populates a new text list with all the users in the topic.

TO DOs
URGENT:
Change nominations in that user file
Actually test this using a text file with random people in it.

Secondary:
Ensure that the user file is robust to changes.
Have an 'alias list' where everyone's alts can be recorded. 

Nice to have:
Eliminate duplicate names / 'Correct' a file or song name

'''

from sys import argv
from collections import defaultdict
import os
import re
# import string

# NOTE: Currently the nominations are in format game | track | link

def is_message_header(atoms):
    '''Takes a line and determines if it is a message header
    or not.'''

    if len(atoms) < 12:
        return False
    
    re_post_number = re.compile("#\d+")
    has_post_number = (re_post_number.match(atoms[0])) is not None

    has_quote = atoms[-1] == "quote"
    has_message_detail = (atoms[-4] == "message" and
                            atoms[-3] == "detail")
        
    return has_post_number and has_quote and has_message_detail

def is_valid_nom(atoms):
    '''Checks to see if the line is a valid nomiation'''
    contains_separator = ('|' in atoms)
    header = is_message_header(atoms)
    return contains_separator and not header

def read_file(filename):
    '''Reads the files line by line,
    Parses things the following way:
    Checks to see if POSTED is next line, indicates username.
    When the countdown is 0, it has reached the postnumber line'''
    users = defaultdict(list)
    post_number = ''
    previous = ''
    
    countdown = -1 # At -1 so it never hits 0 when decremented.
    
    
    with open(filename) as input_file:
        current = input_file.readline()
        while current != '':
            if previous != '':
                moderator_catch = previous
            atoms = current.split()
            
            if is_message_header(atoms):
                current_user = atoms[2]
                if current_user == "(Moderator)":
                    current_user = moderator_catch.split('\n')[0]
                    # this is broken
                    # may not need this anymore if
                    # it doesn't break on moderators   
                users[current_user] 
                post_number = atoms[0][1:]   # remove the hashtag

            # In order, checks that it's a Nomination
            # it's not the message header
            # and it's not in a quote
            
            if is_valid_nom(atoms):
                game, track, link = nomination(current, current_user)
                users[current_user].append((game, 
                                            track, 
                                            link, 
                                            post_number))
                
            current = input_file.readline()
    return users, post_number

        
def nomination(line, user):
    '''Parsing each legal line as a nomination.'''
    item = [element.strip() for element in line.split("|") if element != '']
    # Split up the nomination into three parts:
    # game, track, link

    
    game, track, link = '', 'TRACK MISSING', 'LINK MISSING'
    if len(item) == 3:
        game, track, link = item[:3]
    elif len(item) == 2:
        game, track = item[:2]
    elif len(item) == 1:
        game = item[0]
        print "WARNING!", user, " hasn't submitted a track!"


    return game, track, link

def write_to_file(users):
    '''Writes the user dict to all the files '''
    for element in users:
        if not os.path.exists('./users/'+ element +'.txt'):
            txt_file = open('./users/'+ element +'.txt', 'w')
        else:
            # txt_file = open('./users/'+ element +'.txt', 'w')
            # Change to a when time for real thing
            txt_file = open('./users/'+ element +'.txt', 'a')


        for item in users[element]:
            for entry in item:
                if not entry.isdigit():
                    txt_file.write(entry+"\n")

            txt_file.write("\n")
            detect_abnormality(users, element, item)
            
#    txt_file.close()
    
    return None

def detect_abnormality(users, element, item):
    '''Reports irregularities in nominations '''
    user_things = [part for part in item]
    if "TRACK MISSING" in user_things:
        print "Post number", item[3], "from", element, "is missing a track!"
    elif "LINK MISSING" in user_things:
        print "Post number", item[3], "from", element, "is missing a link."
    elif users[element] == []:
        print element, "has made no nominations in post no.", item[3]
    else:
        pass
            
def alias():
    '''Detects track names or alts via
some preset configuration file '''
    pass

if __name__ == "__main__":
    if len(argv) > 1:
        SCRIPT, FILENAME = argv[0], argv[1]
    else:
        print "File? Default: new_info.txt"
        FILENAME = raw_input('--> ')
        if FILENAME == 'prompt' or FILENAME == '':
            FILENAME = 'new_info.txt'
 
    ALL_USERS, LAST_POST = read_file(FILENAME)
    if os.path.exists('last_updated.txt'):
        with open('last_updated.txt') as f:
            LAST_UPDATED = f.read()
            if LAST_POST == LAST_UPDATED:
                print "Whoops! Looks like you tried to update twice in a row!"
                print "Failing gracefully so you don't write twice."
                raise SystemExit
    write_to_file(ALL_USERS)

    with open('last_updated.txt', 'w') as UPDATE:
        UPDATE.write(str(LAST_POST))
        print "File updating until post", LAST_POST, "in the topic."

    raise SystemExit
