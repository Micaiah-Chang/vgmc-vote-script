"""Parses each individual user file into a gigantic final document
IMPORTANT: READ THIS:
NOMINATION FORMAT IS AS FOLLOWS:

(++/--) Game | Track | Link

I REPEAT THIS IS HOW THE NOMINATION FORMAT IS.


To Do:

DONE:
Determine how noms should be formatted.

URGENT:
Detect and disallow retirees (Ban list)

Secondary:
Header file to the main user file that will allow me
to update noms in a linear scan, instead of O(n^2) time.


Nice to have:
Error checking.


TO-DO:
Refactor this file.
Start with write_to_nom_file
"""

#from sys import
import os
from collections import defaultdict
import math

MAX_NOMS = 20
SAME_GAME_MAX = 2
MAX_DOUBLES = 5

class Nominations(object):
    '''Class which collects all nominations with track and link.
    Only grabs the track with the best link and tracks.'''

    def __init__(self):
        self.noms = []



    def populate(self, game, track, link):
        '''Adds tracks according to a master list.
        Makes sure to return stuff if they're doing things'''

        if compare_entries_in_nom(game, track, self.noms):
            return
        elif game == 'GAME MISSING':
            for element in self.noms:
                if track.lower() == element[1].lower():
                    return element
            self.noms.append((game, track, link))
        elif link == 'LINK MISSING':
            for element in self.noms:
                if game.lower() == element[0].lower() \
                        and track.lower() == element[1].lower():
                    return element
            self.noms.append((game, track, link))
            return
        else:
            self.noms.append((game, track, link))
            return

def compare_entries_in_nom(game, track, nomination_list):
    '''Helper Function for checking that the games and the
    tracks match w/o considering links'''
    return ((game.lower(), track.lower()) in \
                [tuple(y.lower() for y in x if 2 > x.index(y)) \
                     for x in nomination_list])


class User(object):
    """Implements a user with tracks, games and nominations """
    def __init__(self, name):
        self.noms = {}
        self.name = name
        self.doubles = 0

    def nom_check(self, game, track, link):
        '''Parses the start of the nomination then sends it off to the
        right method '''
        if game.startswith('+'):
            self.add_nom(game, track, link)
        elif game.startswith('-'):
            self.remove_nom(game, track, link)
        else:
            if track.lstrip('#').isdigit() is True:
                return False
            print('Undefined behavior for', self.name, 'and track', track)
            return False
        return True

    def add_nom(self, game, track, link):
        '''Adds a nomination, throwing an error message if noms are full.
        Should have the following functionality in future:
        LUXURY FEATURE: Checking for mistyped track names and stuff'''


        double = False
        if game.startswith('++') and self.doubles < 0:
            try:
                double_value = self.noms.get((game, track))[1]
                if double_value == True:
                    return
            except TypeError:
                pass
            double = True
            self.doubles += 1
        elif game.startswith('++') and self.doubles == MAX_DOUBLES:
            print('User,', self.name, 'has too many doubles! Dropping double for', track)
            return False
        else:
            pass

        game = game.lstrip('+ ')
        # Above Code checks for doubles

        tracks_from_same_game = 0
        for key in self.noms.keys():
            existing_game = key[0]
            if existing_game == game and track != key[1]:
                tracks_from_same_game += 1
                if tracks_from_same_game == SAME_GAME_MAX:
                    print("Too many tracks from this game!")
                    print("Dropping", track, "in", game, "for", self.name)
                    return False
        # Above Code Checks for less than two tracks from the same game.

        if ((game, track) in self.noms and double == False
             and self.doubles < MAX_DOUBLES):
            double = True
            self.doubles += 1

        if track == '':
            return False
        elif ((game, track) in self.noms) and \
                (self.noms[(game, track)][1] == True) and (double == False):
            self.doubles -= 1

            try:
                game, track, link = NOMINATIONS.populate(game, track, link)
            except TypeError:
                pass
            self.noms[(game, track)] = (link, double)
            # If the track exists and is doubled, denom it.
            # And try to update the nominations table

        elif len(self.noms) < MAX_NOMS or (double == True):
            try:
                game, track, link = NOMINATIONS.populate(game, track, link)
            except TypeError:
                pass
            self.noms[(game, track)] = (link, double)
            # If there are less than max nominations and less than max doubles,
            # Update the user nominations and nominations table
        else:
            print('Nominations full for', self.name, 'discarding', track)
            return False
        # Catch All
        return True


    def remove_nom(self, game, track, link):
        '''Checks to see if a nomination exists
        and deletes if it does.
        Also checks to see if the double flag has been tripped.
        Otherwise informs what user doesn't have it
        and continues'''
        
        flag = False
        if game.startswith('--'):
            flag = True
        # Sets flag for there being a double denom
            
        game = game.lstrip('- ')

        if (game, track) in self.noms:
            if self.noms[(game, track)][1] == True and (flag == False):
                self.doubles -= 1
                self.noms[(game, track)] = (link, flag)
            elif self.noms[(game, track)][1] == True and (flag == True):
                self.doubles -= 1
                del self.noms[(game, track)]
                # Gets rid of double of it exists
                
            else:
                del self.noms[(game, track)]

            # if self.name == "azuarc":
            #     print self.doubles

            return True
        else:
            print('Error!', track, 'does not exist as a track for', self.name)
            return False



        
def read_users(folder):
    '''Looks through all the users in the subfile and acts on
    them '''
    all_users = []


    listing = os.listdir(folder)
    for infile in listing:
        if infile[-4:] == ".txt":
            with open(folder + infile) as text_file:
                name = infile.split('.')[0].strip()
                current_user = User(name)
                all_users.append(current_user)
                lines = [x.strip() for x in text_file.readlines()]
                pass_noms_to_user(current_user, lines)
            

    return all_users


def pass_noms_to_user(current_user, lines):
    '''Scans through the folder for every user text file and adds
    nomation to the user object
    Assumes at the user text is formatted
    in the following format
    Game Title
    Track
    Link
    <Blank Line>
    '''
    game, track, link = '', '', ''

    for index in range(len(lines)):
        if lines[index] == '='*10:
            break
        elif index % 4 == 0:
            game = lines[index].strip()
        elif index % 4 == 1:
            track = lines[index].strip()
        elif index % 4 == 2:
            link = lines[index].strip()
        elif index % 4 == 3:
            current_user.nom_check(game, track, link)
        else:
            pass


def write_to_nom_file(all_users, nom_file):
    '''Consolidates all the user's nominations to one megafile.
    Format:
    User

    Track
    Game
    Link

    ---
    '''

    for current_user in all_users:
        
        nom_file.write(current_user.name+'\n\n')

        double_noms = []
        single_noms = []

        for game, track in current_user.noms:
            link, double_flag = current_user.noms[(game, track)]
            nom_line = ' | '.join([game,track,link])

            if double_flag:
                double_noms.append(nom_line)
            else:
                single_noms.append(nom_line)

        if double_noms:
            nom_file.write("Doubles:"+'\n')
            for number, line in enumerate(double_noms):
                nom_file.write(str(number+1)+". "+line+'\n')

        if single_noms:
            nom_file.write("Singles:"+'\n')
            for number, line in enumerate(single_noms):
                nom_file.write(str(number+1)+". "+line+'\n')

        nom_file.write("---\n\n")
        
    nom_file.close()


def nominations_left(all_users):
    '''Counts the number of nominations a user has left'''
    nom_file = open('noms_left.txt', 'w')
    last_updated = open('last_updated.txt', 'r').read()
    nom_file.write("Updated up to post: "+last_updated+"\n")
    for current_user in all_users:
        noms_left = MAX_NOMS - len(current_user.noms)
        doubles_left = MAX_DOUBLES - current_user.doubles
        nom_file.write(current_user.name+'\n'+"User has "+
                       str(noms_left)+
                       " nominations and "+
                       str(doubles_left)+" doubles left.\n\n")


def consolidate(users, tally_file):
    '''Takes all the users then populates a nomination list with them.
    Desired format:
    Votes: #
    Game,Track,User

    NOTE: CURRENTLY ONLY HAS TRACK'''

    noms = defaultdict(float)
    for user in users:
        for element in user.noms:
            if user.noms[element][1] is True:
                noms[element] += 2
            else:
                noms[element] += 1
            noms[element] += 0.001 
            # This records the number of unique users

    noms = invert_dict(noms)
    
    for key in sorted(noms, reverse=True):
        num_of_users = math.trunc(1000*(key - math.floor(key)))
        num_of_votes = int(math.floor(key))
        num_of_doubles = int(num_of_votes - num_of_users)
        
        tally_file.write('Votes: ' + str(num_of_votes))
        tally_file.write(' Users: ' + str(num_of_users))
        tally_file.write(' Doubles: '+ str(num_of_doubles) + '\n')
        for item in noms[key]:
            for element in item:
                tally_file.write(element+' | ')
            tally_file.write('\n')
        tally_file.write('\n')

        

def invert_dict(dic):
    '''Inverts a dictionary, so that instead of Track -> Nominations
    It becomes Nominations -> Track'''
    inverted_dict = defaultdict(set)
    for tracks, nomination in dic.items():
        inverted_dict[nomination].add(tracks)
    return inverted_dict

def tsv_spreadsheet(all_users):
    '''Outputs in tsv format'''
    with open('upload.tsv', 'w') as upload:
        # Write the header
        upload.write('Game\tSong\tLink\t')
        number_of_users = len(all_users)
        for user_number in range(number_of_users):
            upload.write(all_users[user_number].name+'\t')
        upload.write('\n')

        # Starts tallying each song with each user

        for element in NOMINATIONS.noms:
            front = '\t'.join(element)
            upload.write(front+'\t')
            for user_number in range(number_of_users):
                current_user = all_users[user_number]
                lowered_noms = {tuple(map(str.lower, k)):v \
                                    for k, v in list(current_user.noms.items())}
                if (element[0].lower(), element[1].lower()) in lowered_noms:
                    if lowered_noms[(element[0].lower(), \
                                         element[1].lower())][1] == True:
                        upload.write('2')
                    else:
                        upload.write('1')
                else:
                    upload.write('0')
                upload.write('\t')
            upload.write('\n')

    


def main():
    '''Main function.
    Currently doesn't take text files as input.
    Should do so in the future?'''

    subfolder = './users/'
    all_users = read_users(subfolder)

    noms = open('nominations.txt', 'w')
    write_to_nom_file(all_users, noms)

    tally = open('tally.txt', 'w')
    consolidate(all_users, tally)
    tsv_spreadsheet(all_users)

    nominations_left(all_users)

#    print NOMINATIONS.noms

NOMINATIONS = Nominations()

if __name__ == '__main__':
    main()
