The Blue Alliance youtube playlist splitter
====================

--------------------------

This is a script which will, given a youtube url and TBA event code, automatically upload videos to the corresponding 
page on [The Blue Alliance](http://thebluealliance.com). The script is only meant to function for videos with 
consistently formatted titles.

This repo doesn't include any code to actually get user inputs. Those are left unimplemented in tba_abstraction.py for
someone more familiar than me with TBA to write.

Important integration information
=========================

----------------

Login info
---------

In order to submit videos to TheBlueAlliance through a google account (which you might want to do when testing), you 
need to create a file called "login_info", placed in the same directory as the other files. Remember to add this to 
your .gitignore! The contents should be as follows:


    [google_login]
    email = your_email@gmail.com
    password = your_password

Concerning client_secrets.json and main.py-oauth.json
-----------------

These files only exist to allow the script to interact with TBA via OAuth, which should be stripped out during 
integration anyways. These are supposed to be secret, but I'm leaving them in because the worst someone could do with
the information in these files is use up my monthly request quota on Google App Engine. Please don't do that :(

The other reason is that since I started this project a while back, Google changed their appengine.google.com website,
and now I have no clue how to download/update a new main.py-oauth2.json file.

To integrate this into TBA
----------

All code not inside a function in tba_abstraction.py can be deleted.All the functions in tba_abstraction.py should be 
rewritten to retrieve user input (return values are hardcoded as-is) from the website. The script should function 
without any further modifications as long as the functions are rewritten to spec. 

login_info, client_secrets.json, and main.py-oauth2.json can also be deleted, since the script (presumably) wont have to
interact with TBA via an OAuth google login.


Usage
=========================

----------------------

What links does this program accept?
---------------------------
Valid links are

* User pages, such as youtube.com/user/IndianaRobotics
* Channels, such as youtube.com/channel/UC6107grRI4m0o2-emgoDnAA
* Playlists, such as youtube.com/playlist?list=PLYiUuSMDgbv-4ccz1Bfph7rQlU1IyywTa

The script uses regex to extract relevant info so it doesn't matter whether there are other things prepended or
appended to the url, like "www"s or random arguments. Try to give it nice links anyways.
 
How does this script know how to extract match info?
----------------------------
All relevant match (match type and match numbers) should be in the title. Users must input "user-friendly" regular 
expressions for each match type, which are then transformed into an *actual* regular expression. Here are the rules for
constructing the user-friendly regex

"~" denotes a match number, as in "Qualification Match **4**" or "Semifinals 2 Match **3**" There should always be one
in each title format.

"^" denotes an elimination match id, as in "Quarterfinals **3** Match 2" or "Semifinals **1** Match 1".
These should only appear in non-finals elimination matches, and were not used at all in 2015.

"&" denotes a generic number- these should be used for any number not described by the two symbols above

EXAMPLES

Let's say we have some videos from an imaginary competition

* Titles for qualification match videos are formatted like "Imaginary Competition 3-13-2015: Qualification Match 32".
The corresponding regex the user should enter is "Imaginary Competition &-&-&: Qualification Match ~" (without quotes)

* Titles for semifinal matches are formatted like "Imaginary Competition: Semifinal 2 Match 1". The corresponding regex
is "Imaginary Competition: Semifinal ^ Match ~" (without quotes)

Inputs should be as specific as possible.