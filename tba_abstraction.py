__author__ = 'anish'

"""
This file is an abstraction to interact with the TBA. Presumably most of the functions in here can be rewritten when
this project is actually integrated into TBA
"""

import ast
import re
import requests

from configparser import ConfigParser

# Create a requests session and log into google with it

config = ConfigParser()
config.read("login_info")

session = requests.Session()
google_accounts_url = 'http://accounts.google.com'
authentication_url = 'https://accounts.google.com/ServiceLoginAuth'

r = session.get(google_accounts_url)
galx = r.cookies['GALX']

session.headers['User-Agent'] = 'Ubuntu 12.04'

payload = {'GALX': galx,
           'continue': 'https://www.google.com/?gws_rd=ssl',
           'Email': config.get("google_login", "email"),
           'Passwd': config.get("google_login", "password")
}

r = session.post(authentication_url, data=payload)

if r.url == authentication_url:

    print("Failed to retrieve an authenticated session")
    exit(1)

# Check if logged in to TheBlueAlliance
# The URL is just a dummy which will redirect you to AppEngine sign in if you need to authenticate
test_request = session.request(url="http://www.thebluealliance.com/suggest/match/video?"
                        "match_key=2015iri_qm2", method="GET")

# If redirected to AppEngine sign-in, then choose user 0 (which is the only one guaranteed to exist,"
# and authenticate the TBA login

if "appengine.google.com" in test_request.url:

    # Pulls any text preceded by ['name="state"' following by an unlimited amount of whitespace] and followed by
    # a quotation mark
    pull_id = '(?<=name="state")(?:\s*value=")(.*)(?=")'

    id = re.search(pull_id, test_request.text).group(1)

    headers_ = {"origin": "https://appengine.google.com",
                "referer": test_request.url}

    data_ = {"authuser": 0,
             "state": id,
             "submit_true": "Allow"}

    r = session.request(url="https://appengine.google.com/_ah/conflogin", method="POST",
                        headers=headers_, data=data_)

    # If at first you don't succeed, exit with an error and give up

    if "appengine.google.com" in session.request(url="http://www.thebluealliance.com/suggest/match/video?"
                        "match_key=2015iri_qm2", method="GET").url:

        print("Failed to authenticate with TheBlueAlliance through AppEngine, exiting...")
        exit(2)


def get_youtube_url():

    """
    Gets a youtube url from the user, which can be a named user page, a channel, or a playlist
    :return:
    """

    return "youtube.com/user/IndianaRobotics"


def get_competition_start(event_code):

    """
    Gets start date of a competition
    :param event_code: The TBA event code
    :return: The start ISO date as a string
    """

    event_info = session.request(url="http://thebluealliance.com/api/v2/event/"+event_code,
                                       headers={"X-TBA-App-Id": "1124-Anish_Moorthy:vod_scraper:v0.1"}, method="GET")

    return ast.literal_eval(event_info.text.replace("null", "None").
                              replace("true", "True").replace("false", "False"))["start_date"]


def post_video(youtube_video_id, event_code, match_code):
    """
    Sets / posts a video of the match to TBA
    :param youtube_url: Youtube url of the video
    :param event_code: TBA event code
    :param match_code: Match code
    :return:
    """

    post_url = "http://www.thebluealliance.com/suggest/match/video?match_key=" + \
    event_code + "_" + match_code

    youtube_url = "http://www.youtube.com/watch?v=" + youtube_video_id

    headers_ = {"referer": post_url,
                "Host": "www.thebluealliance.com",
                "Origin": "http://thebluealliance.com",
                "Connection": "keep-alive"
                }

    payload = {"match_key": event_code + "_" + match_code,
               "youtube_url": youtube_url}


    session.request(url="http://thebluealliance.com/suggest/match/video", method="POST",
                    headers=headers_, data=payload)


def get_event_code():
    """
    Gets an event code from the user
    :return: the event code as a string
    """
    return "2015iri"


def get_qm_expression():

    """
    Gets a qualifying match simplified regex from the user
    :return: The simplified regex as a string
    """

    return "Indiana Robotics Invitational Q~"


def get_qf_expression():

    """
    Gets a quarterfinal match simplified regex from the user
    :return: The simplified regex as a string
    """

    return "Indiana Robotics Invitational QF~"


def get_sf_expression():

    """
    Gets a semifinal match simplified regex from the user
    :return: The simplified regex as a string
    """
    return "Indiana Robotics Invitational SF~"


def get_f_expression():

    """
    Gets a finals match simplified regex from the user
    :return: The simplified regex as a string
    """

    return "Indiana Robotics Invitational F~"