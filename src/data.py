import csv

import pandas as pd
import requests
import langdetect

KEY = "AIzaSyDn3bGDD-JzznJg6MQ7WtQ1vFHJR5mZqPM"
session = requests.session()


def generate_categories():
    """ Generate categories and put them in the data/categories.csv file. """

    # Define categories csv file
    categories = open('../data/categories.csv', 'w')
    categories.write("id,title\n")

    # Get available categories and their names
    for id in range(100):
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


def generate_videos():
    """ Generate documents and put them in the data/documents.csv file. """

    # Define documents & categories csv file
    categories = pd.read_csv('../data/categories.csv')
    videos = open('../data/videos.csv', 'a')
    videos.write("id,category_id,published_at,channel_id,title,description\n")

    # From the available categories search fetch the top documents
    for index, category in categories.iterrows():
        category_id = int(category["id"])
        res = session.get("https://www.googleapis.com/youtube/v3/search", params={
            "part": "snippet",
            "maxResults": 50,
            "order": "relevance",
            "relevanceLanguage": "en",
            "videoCategoryId": category_id,
            "type": "video",
            "key": KEY
        }).json()
        for video in res["items"]:
            video_id = video["id"]["videoId"]
            channel_id = video["snippet"]["channelId"]
            published_at = video["snippet"]["publishedAt"]
            print("Inserting video {} to documents.csv ...".format(video_id))
            videos.write('{},{},{},{}\n'.format(video_id, category_id, channel_id, published_at))

    # Success
    return True


def generate_comments():
    """ Generate comments e.g. fetch commentthreads from a video and save it in comments.csv. """

    # Define documents csv file
    videos = pd.read_csv("../data/videos.csv")
    file = open('../data/comments.csv', 'w')
    comments = csv.writer(file)
    comments.writerow(["video_id","index","content"])

    # Itterate through documents
    for index, video in videos.iterrows():

        video_id = video["id"]

        # Fetch comment thread of this video
        res = session.get("https://www.googleapis.com/youtube/v3/commentThreads", params={
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "textFormat": "plainText",
            "order": "relevance",
            "key": KEY
        }).json()
        if "items" not in res: continue

        # Generate a document for this video
        print("Writing all comments from video {} to document {}.txt ...".format(video_id, video_id))

        # Iterate over all comments and put them in the document
        for index, comment in enumerate(res["items"]):
           content = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
           if len(content.split()) > 5 and langdetect.detect(content) == "en":
               comments.writerow([video_id, index, str(content)])

    # Close the document
    file.close()

    # Success
    return True