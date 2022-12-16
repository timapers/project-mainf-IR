import csv

import pandas as pd
import requests
import langdetect
import string

KEY = "AIzaSyAYafi968hIvH33mgtHGG26_GlLymPwDnA"
session = requests.session()
# Constants
NR_OF_VIDEOS = 50
MAX_NR_OF_COMMENTS = 100
MIN_NR_OF_COMMENTS = 90


def generate_categories():
    """ Generate categories and put them in the data/categories.csv file. """

    # Define categories csv file
    categories = open('../data/categories.csv', 'w')
    categories.write("id,title\n")

    # Get most interesting categories and their names (after 30 you have movies and subcategories of movie genres)
    for id in range(30):
        res = session.get("https://www.googleapis.com/youtube/v3/videoCategories", params={
            "part": "snippet",
            "id": id,
            "key": KEY
        }).json()
        if not res["items"]: continue
        print("Inserting category {} to categories.csv ...".format(id))
        categories.write("{},{}\n".format(id, res["items"][0]["snippet"]["title"]))

    # Success
    return True


def generate_data():
    """ Generate videos with comments and put them in the data/videos.csv & data/comments.csv file. """

    # Define videos, comments & categories csv file
    categories = pd.read_csv('../data/categories.csv')
    videos_file = csv.writer(open('../data/videos.csv', 'a'))
    comments_file = csv.writer(open('../data/comments.csv', 'a'))

    # From the available categories search fetch the top videos
    for index, category in categories.iterrows():
        category_id = int(category["id"])
        # Check to see if a video is already been checked and if we already have enough videos
        received_titles, nr_accepted_videos = get_received_videos(category_id)

        if nr_accepted_videos == NR_OF_VIDEOS:  # we already have enough videos for this category
            print("CATEGORY {} ALREADY HAS ENOUGH VIDEOS".format(category_id))
            continue

        # remaining number of videos we want of a category (initialisation)
        remaining_nr_of_videos = NR_OF_VIDEOS - nr_accepted_videos
        # query tries to filter out the videos that are already checked (initialisation)
        q = initialise_query(received_titles)

        while remaining_nr_of_videos > 0:  # keep searching for videos until NR_OF_VIDEOS is found per category

            # Fetch remaining amount of video's
            res = session.get("https://www.googleapis.com/youtube/v3/search", params={
                "part": "snippet",
                "maxResults": NR_OF_VIDEOS,
                "order": "relevance",
                "relevanceLanguage": "en",
                "videoCategoryId": category_id,
                "q": q,
                "type": "video",
                "key": KEY
            }).json()

            # loop over the retrieved videos
            if not res["items"]:
                print("NO VIDEOS")
                continue
            for video in res["items"]:
                video_id = video["id"]["videoId"]
                channel_id = video["snippet"]["channelId"]
                published_at = video["snippet"]["publishedAt"]
                title = video["snippet"]["title"]
                if title not in received_titles:
                    received_titles.append(title)
                    q = title_to_query(title, q)
                    try:
                        language = langdetect.detect(str(title))
                    except:
                        continue
                    if language == "en":
                        # Fetch comment thread of this video
                        res2 = session.get("https://www.googleapis.com/youtube/v3/commentThreads", params={
                            "part": "id,snippet",
                            "videoId": video_id,
                            "maxResults": MAX_NR_OF_COMMENTS,
                            "textFormat": "plainText",
                            "order": "relevance",
                            "key": KEY
                        }).json()

                        # Check if video has comments
                        if "items" not in res2:
                            print("NO COMMENTS")
                            videos_file.writerow([video_id, category_id, published_at, channel_id, title, False])
                            continue

                        else:  # video has comments
                            # check if there are enough comments
                            if len(res2["items"]) > MIN_NR_OF_COMMENTS:
                                # if enough comments, video is accepted
                                print("Inserting video {} to videos.csv with {} comments...".format(video_id, len(
                                    res2["items"])))
                                videos_file.writerow([video_id, category_id, published_at, channel_id, title, True])

                                # Iterate over all comments
                                for index_, comment in enumerate(res2["items"]):
                                    content = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                                    comments_file.writerow([category_id, video_id, content])

                                remaining_nr_of_videos -= 1
                                if remaining_nr_of_videos == 0: break

                            else:
                                print("NOT ENOUGH COMMENTS")
                                videos_file.writerow([video_id, category_id, published_at, channel_id, title, False])
                    else:
                        print("NOT ENGLISH")
                        videos_file.writerow([video_id, category_id, published_at, channel_id, title, False])
    # Success
    return True


def initialize_files():
    videos_file = csv.writer(open('../data/videos.csv', 'w'))
    videos_file.writerow(["id", "category_id", "published_at", "channel_id", "title", "is_acceptable"])
    comments_file = csv.writer(open('../data/comments.csv', 'w'))
    comments_file.writerow(["category", "video_id", "content"])


def get_received_videos(category_id):
    """ Returns a list of titles of videos of a certain category that are already in videos.csv
    AND return number of accepted videos"""
    titles_of_videos = []
    nr_accepted_videos = 0
    # read file
    videos = pd.read_csv('../data/videos.csv')
    for index, video in videos.iterrows():
        if video["category_id"] == category_id:
            titles_of_videos.append(video["title"])
            if video["is_acceptable"]:
                nr_accepted_videos += 1

    return titles_of_videos, nr_accepted_videos


def initialise_query(received_titles):
    # query has to contain something positive so I chose any vowel
    q = 'a|e|i|o|u '
    for received_title in received_titles:
        q = title_to_query(received_title, q)
    return q


def title_to_query(title, q):
    # replace | with space because otherwise some words are put together
    title.replace('|', ' ')
    # delete words with less than 6 characters
    important_word_title = max(title.split(), key=len)
    important_word = ''.join([x for x in important_word_title if x.isalnum()])
    # Add title with - to query so this video will be excluded in the next search
    q += '-"' + important_word + '" '
    return q
