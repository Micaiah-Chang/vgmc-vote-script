'''This file reads from new_info.txt or asks for some file
and then populates a new text list with all the users in the topic.

Format for nominations are:

Game | Track | Link

HTML from 05/14/2014

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
from bs4 import BeautifulSoup, Tag
import subprocess
import glob

LAST_UPDATE_FILE = 'last_updated.txt'

def check_update():
    """Check to see what the last updated post was via.
    Return: last_updated => Int"""
    with open(LAST_UPDATE_FILE) as f_update:
        last_updated = f_update.read()

        is_new_topic = last_updated == '' or last_updated == "500"
        if is_new_topic:
            print "Starting a new topic! Specify which posts you wish to skip."
            last_updated = raw_input("Ignore first x posts (default: 2)\n")

            no_response = (last_updated == 'prompt' or last_updated == '')
            if no_response:
                last_updated = 2

    return int(last_updated)


def read_alts():
    """Read from alt.txt and construct dictionary of alt-main pairs
    Return: alt_dict => Dictionary[Alt -> Main]"""
    alt_dict = {}

    with open('alts.txt', 'r') as alt_file:
        for line in alt_file.readlines():
            temp = line.strip().split('\t')

            if len(temp) < 2:
                print "Misformatted line!"
                print line
                print "Skipping to next line."
                continue

            main_acc = temp[0]
            alt_acc = temp[1]
            alt_dict[alt_acc] = main_acc

    del alt_dict['Alt'] # get rid of the first line

    return alt_dict


def decide_input():
    '''Ask for an input file and decide how to parse based on that.
    Return: Filename => String'''
    if len(argv) > 1:
        _, filename = argv[0], argv[1]
    else:
        default = "new_info.html"
        print "File? Default: ", default
        filename = raw_input('--> ')

        if filename == 'prompt' or filename == '':
            filename = default

    return filename


def read_file(filename, extension, last_updated, alt_dict):
    '''Dispatch file parsing function
    depending on extension type.
    filename => String, extension => String, last_updated => int,
    alt_dict => Dictionary[Alt -> Main]'''

    if extension == ".txt":
        users, post_number = read_text_file(filename, alt_dict)
    elif extension == ".html":
        users, post_number = read_html_file(filename, alt_dict, last_updated)
    else:
        raise Exception

    return users, post_number


def read_html_file(filename, alt_dict, last_updated):
    ''' Procedure for reading html files.
    Reads the files by traversing the html tree.'''
    users = defaultdict(list)
    post_number = ''

    with open(filename) as f_doc:
        html_doc = f_doc.read()
        soup = BeautifulSoup(html_doc)

    post_iter = soup.find_all("tr", "top")

    # Find every post via its message header
    for header in post_iter:
        current_user, post_number = parse_html_header(header)

        # Ignore the post if we've seen it before on a previous run
        # Second part is an edge case for Topics beyond the first
        if int(post_number) <= last_updated and last_updated != 500:
            continue

        # Spot alts and write treat them as the same as their main
        if current_user in alt_dict:
            main_acc = alt_dict[current_user]
            print "Counting", current_user, "as", main_acc+"'s"+" alt"
            current_user = main_acc

        post_body = header.next_sibling
        post_body = remove_quotes(post_body)
        users = noms_from_post(users, current_user, post_body, post_number)

    return users, post_number


def parse_html_header(header):
    '''Find post number and username from message header.
    HTML from 05/14/2014'''
    for child in header.children:
        msg_txt = child.find("div").contents
        re_post_number = re.compile(r"#\d+")
        has_post_number = re_post_number.match(msg_txt[0])
        post_no = has_post_number.group()
        post_no = post_no[1:] # remove hashmark and convert to number

        user = child.find("a").contents[0].string
        user = user.strip()

    return user, post_no


def remove_quotes(post):
    '''Removes quoted messages from post'''
    for tag in post.descendants:
        if isinstance(tag, Tag) and not tag.blockquote is None:
            tag.blockquote.extract()

    return post


def noms_from_post(users, current_user, post_body, post_number):
    '''Obtains nomations from an html version of post'''
    for line in post_body.strings:
        atoms = line.split()
        if is_valid_nom(atoms):
            game, track, link = parse_nom(line, current_user)
            users[current_user].append((game, track, link, post_number))

    return users


def parse_nom(line, user):
    '''Parsing each legal line as a nomination.'''
    item = [element.strip() for element in line.split("|")]
    item = [element   for element in item if element != ""]
    # Split up the nomination into three parts: game, track, link

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
    '''Writes the user dict to all the files
    Users => Dictionary[Username -> Nomination], last_updated => Int'''

    # Iterates over every user's file
    for user in users:
        if not os.path.exists('./users/'+ user +'.txt'):
            txt_file = open('./users/'+ user +'.txt', 'w')
        else:
            txt_file = open('./users/'+ user +'.txt', 'a')

        # Writes each user's individual nom to their txt file
        for (game, track, link, post_number) in users[user]:
            try:
                entry = "\n".join([game, track, link])
                txt_file.write(entry+"\n")
            # Current program not compatible with unicode
            except UnicodeEncodeError:
                print "Failed on", user+"'s", "post."
                print "Check post number", post_number

            txt_file.write("\n")
            detect_abnormality(users, user, users[user])


def detect_abnormality(users, user, nomination):
    '''Reports irregularities in nominations.'''
    unpacked_noms = [part for part in nomination]

    if "TRACK MISSING" in unpacked_noms:
        print "Post number", nomination[3], "from", user, "is missing a track!"
    elif "LINK MISSING" in unpacked_noms:
        print "Post number", nomination[3], "from", user, "is missing a link."
    elif users[user] == []:
        print user, "has made no nominations in post no.", nomination[3]
    else:
        pass


def display_update(last_post):
    """Inform client of what the program has updated until.
    last_post => Str containing last updated post"""
    with open(LAST_UPDATE_FILE, 'w') as update:
        update.write(str(last_post))
        print "File updating until post", last_post, "in the topic."


def double_update_check(last_updated, last_post):
    """Compares the last post from before the program was run
    to after.
    last_updated => str from LAST_UPDATE_FILE from before program was run
    last_post => str showing what the latest post the program has parsed."""
    if int(last_updated) >= int(last_post) and int(last_updated) != 500:
        print "Whoops! Looks like you tried to update twice in a row!"
        print "Failing gracefully so you don't write twice."
        raise SystemExit
    else:
        print "Updating from", last_updated, "to", last_post


def is_txt_message_header(line):
    '''Takes a line and determines if it is a message header
    or not.'''

    if len(line) < 12:
        return False

    re_post_number = re.compile(r"#\d+")
    has_post_number = (re_post_number.match(line[0])) is not None

    has_quote = line[-1] == "quote"
    has_message_detail = (line[-4] == "message" and line[-3] == "detail")

    return has_post_number and has_quote and has_message_detail

def is_valid_nom(atoms):
    '''Checks to see if the line is a valid nomiation'''
    contains_separator = ('|' in atoms)
    header = is_txt_message_header(atoms)
    return contains_separator and not header





def read_text_file(filename, alt_dict):
    '''Procedure for reading text files.
    Reads the files line by line,
    Parses things the following way:
    Checks to see if POSTED is next line, indicates username.'''
    users = defaultdict(list)
    post_number = ''


    with open(filename) as input_file:
        current = input_file.readline()
        while current != '':
            atoms = current.split()

            if is_txt_message_header(atoms):
                current_user = atoms[2]
                users[current_user]
                post_number = atoms[0][1:]   # remove the hashtag

            # In order, checks that it's a Nomination
            # it's not the message header
            # and it's not in a quote
            if current_user in alt_dict:
                current_user = alt_dict[current_user]

            if is_valid_nom(atoms):
                game, track, link = parse_nom(current, current_user)
                users[current_user].append((game,
                                            track,
                                            link,
                                            post_number))

            current = input_file.readline()
    return users, post_number


def backup_files(last_updated):
    """Create a backup if there are text files """
    backup_name = "post"+str(last_updated)

    do_txt_files_exist = glob.glob("./users/*.txt")

    if do_txt_files_exist:
        try:
            subprocess.call("mkdir users/"+backup_name)
            subprocess.call("cp"+" users/*.txt "+"users/"+backup_name)
        except OSError:
            subprocess.call("rmdir users/"+backup_name)
            print "Failed to create new backup directory. Terminating write."
            print "Rerun script to continue"
            raise SystemExit
    else:
        print "Nothing to back up."


def main():
    """Main function, that performs setup, parsing and output
    to user text files."""
    # Set up
    last_updated = check_update()
    alt_dict = read_alts()
    filename = decide_input()
    _, extension = os.path.splitext(filename)

    # Parsing
    all_users, last_post = read_file(filename, extension,
                                     last_updated, alt_dict)

    # output
    double_update_check(last_updated, last_post)
    backup_files(last_updated)
    write_to_file(all_users)
    display_update(last_post)

    raise SystemExit

if __name__ == "__main__":
    main()
