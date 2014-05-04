How to start tallying:

Copy and paste all the relevant posts you want to tally into new_info.txt
(Note: Don't copy the first rule post. The program will think your
examples are legit noms)

Then run

python parser.py 

The program will run and update all the text files in ./users

If this fails, make sure you 
1) have a users subfolder 
2) Pasted into new_info.txt

If you want to change something for a user, open up their file and change the trackname / link there

This is what you need to do as the topic progresses. 

If you've forgotten what the last post you updated until was, go to
'last_updated.txt' and that will have the the most recent post.

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
