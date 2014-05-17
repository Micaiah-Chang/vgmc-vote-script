How to start tallying:

Copy and paste the gamefaqs source code into new_info.html. 

Open up alts.txt and write the main, alt pairs as "Main<TAB>Alt". 

Then run

python parser.py new_info.html

The program will run and update all the text files in ./users

If this fails, make sure you 
1) have a users subfolder 
2) Pasted into new_info.txt

If you want to change something for a user, open up their file and change the trackname / link there


How to update the Tally Sheet:

Simply run 

python nomcheck.py

The following files get updated:

nominations.txt
tally.txt
upload.tsv

nominations.txt has everyone's nominations in one spot.

tally.txt has all of the tracks/games tallyed according to the number 
of total nominations and unique users.

upload.tsv is what you upload to google docs.

To upload:

Open up a new or existing spreadsheet, then File->Import->Change Import action to Replace Current Sheet
And upload.sv in the uploaded file.

Remember to lock/unlock the first rows if you want to format the rows! 
View -> Freeze Rows

To correct errors or typoes: 

Please COPY the correct spelling and do a find and replace in 
the user's text file.

i.e.

Let's say I have 'FF7' instead of 'Final Fantasy 7' You'd copy 'Final Fantasy 7'
Open up ToukaOone.txt and replace all examples of FF7 with Final Fantasy 7.

Common Error message interpretations:

Long string of 'Undefined Behavior':
The formatting is screwed up inside the user.txt
Please make sure that everything is in the format

Game
Track
Link
BLANK LINE

Usually this happens when a blank line accidentally gets deleted. 
If you wish to delete a link or something write down GAME MISSING or LINK MISSING
in its place.

If it says ./users does not exist, make sure you create a 'users' subfolder 
before running parse_things.py
