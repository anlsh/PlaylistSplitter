__author__ = 'anish'

import tba_abstraction as ta

from title_evaluator import TitleEvaluator

from youtube_session import get_youtube_session, videos

import re

'''
This is the part of the code which actually takes the youtube url and does fancy stuff with it
'''

'''
Regex conventions
~ denotes match number
^ denotes an elimination match id, if it exists
& denotes generic number (such as team names)
'''

if __name__ == "__main__":

    # Get parameters and such

    event_code = ta.get_event_code()

    evaluator = TitleEvaluator({'qm': ta.get_qm_expression(), 'qf': ta.get_qf_expression(),
                                'sf': ta.get_sf_expression(), 'f': ta.get_f_expression()})

    youtube_url = ta.get_youtube_url()

    start_date = ta.get_competition_start(event_code)

    # Loop through the playlist and submit videos to TBA

    video_list = []

    # Check if the given url is a user, channel, or playlist, and extract relevant information

    url_info = re.search(r"youtube\.com/(?P<type>user|channel|playlist)(?:\?list=)*/*(?P<id>.+)(?:&*/*)", youtube_url)

    # Initialize a youtube session

    ytapi_session = get_youtube_session()

    info = ""

    if not (url_info):
        raise RuntimeError("Malformed youtube url")

    if url_info.group("type") == "user":
        info = ytapi_session.channels().list(part="contentDetails", forUsername=url_info.group("id")).execute()

    elif url_info.group("type") == "channel":
        info = ytapi_session.channels().list(part="contentDetails", id=url_info.group("id")).execute()

    elif url_info.group("type") == "playlist":
        info = ytapi_session.playlists().list(part="contentDetails", id=url_info.group("id")).execute()

    uploads_id = info["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request_more = True

    for v in videos(ytapi_session, uploads_id):

        if not request_more:
            break

        for item in v["items"]:

            # Make sure the video was published before the event...

            if item["snippet"]["publishedAt"] < start_date:
                request_more = False
                break

            # And that it wasn't published more than a year after

            if not item["snippet"]["publishedAt"][:4] > start_date[:4]:

                match_code = evaluator.extract_match_id(item["snippet"]["title"])

                if match_code is not None:

                    ta.post_video(item["snippet"]["resourceId"]["videoId"], event_code, match_code)