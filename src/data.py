import csv

import pandas as pd
import requests
import langdetect
import string

KEY = "AIzaSyDecu1mbmmplo6jYpEE1PyJ2AGhCSghyfw"
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
    """ Generate documents and put them in the data/videos.csv file. """

    # Define documents & categories csv file
    categories = pd.read_csv('../data/categories.csv')
    videos = open('../data/videos.csv', 'w')
    videos.write("id,category_id,published_at,channel_id,title,description\n")
    # TODO: Delete i
    i = 0
    # From the available categories search fetch the top documents
    for index, category in categories.iterrows():
        # TODO: Delete i
        if i < 2:
            category_id = int(category["id"])
            res = session.get("https://www.googleapis.com/youtube/v3/search", params={
                "part": "snippet",
                "maxResults": 5,
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
                title = video["snippet"]["title"]
                print("Inserting video {} to documents.csv ...".format(video_id))
                videos.write('{},{},{},{},"{}"\n'.format(video_id, category_id, published_at, channel_id, title))
            # TODO: Delete i
            i += 1
    # Success
    return True


def generate_comments():
    """ Generate comments e.g. fetch commentthreads from a video and save it in comments.csv. """

    # Define documents csv file
    videos = pd.read_csv("../data/videos.csv")
    file = open('../data/comments.csv', 'w')
    comments = csv.writer(file)
    comments.writerow(["video_id", "index", "content"])

    # Itterate through documents
    for index, video in videos.iterrows():

        video_id = video["id"]

        # Fetch comment thread of this video
        res = session.get("https://www.googleapis.com/youtube/v3/commentThreads", params={
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 10,
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


# Generate_videos() & generate_comments() worden niet langer gebruikt en heb ik volledig samen genomen in generate_data
def generate_data():
    """ Generate videos with comments and put them in the data/videos.csv file. """

    # Define data_videos, data_comments & categories csv file
    categories = pd.read_csv('../data/categories.csv')
    videos_file = open('../data/videos.csv', 'w')
    videos_file.write("id,category_id,published_at,channel_id,title\n")
    comments_file = csv.writer(open('../data/comments.csv', 'w'))
    comments_file.writerow(["category_id", "video_id", "content"])
    nr_of_videos = 20
    # TODO: Delete i
    i = 0
    # From the available categories search fetch the top videos
    for index, category in categories.iterrows():
        # TODO: Delete i
        if i < 2:
            # remaining number of videos we want of a category (initialisation > after comment check it can change)
            remaining_nr_of_videos = nr_of_videos
            # query houdt bij welke videos al geselecteerd zijn geweest zodat ze niet opnieuw in de lijst kunnen zitten
            # we moeten minstens 1 positief ding hebben in onze query om het te laten werken (dus eender welke klinker)
            q = 'a|e|i|o|u '
            # omdat q niet altijd werkt nog eens een extra check:
            recieved_titles = []
            category_id = int(category["id"])
            while remaining_nr_of_videos > 0:  # blijf zoeken naar videos tot het goede # voor deze category is behaald

                # Fetch remaining amount of video's
                res = session.get("https://www.googleapis.com/youtube/v3/search", params={
                    "part": "snippet",
                    "maxResults": nr_of_videos,
                    "order": "relevance",
                    "relevanceLanguage": "en",
                    "videoCategoryId": category_id,
                    "q": q,
                    "type": "video",
                    "key": KEY
                }).json()

                # loop over the retrieved videos
                for video in res["items"]:
                    video_id = video["id"]["videoId"]
                    channel_id = video["snippet"]["channelId"]
                    published_at = video["snippet"]["publishedAt"]
                    title = video["snippet"]["title"]
                    if title not in recieved_titles:
                        recieved_titles.append(title)
                        # delete words with less than 4 characters
                        title.replace('|', ' ')
                        important_words_title = [x for x in title.split() if len(x) > 5]
                        for word in important_words_title:
                            important_word = ''.join([x for x in word if x.isalnum()])
                            # Add title with - to query so this video will be excluded in the next search
                            q += '-"' + important_word + '" '

                        if langdetect.detect(title) == "en":
                            # Fetch comment thread of this video
                            res2 = session.get("https://www.googleapis.com/youtube/v3/commentThreads", params={
                                "part": "id,snippet",
                                "videoId": video_id,
                                "maxResults": 100,
                                "textFormat": "plainText",
                                "order": "relevance",
                                "key": KEY
                            }).json()

                            # Check if video has comments
                            if "items" not in res2:
                                print("NO COMMENTS")
                                continue

                            else:  # video has comments... check how many
                                # check if there are enough comments (min 90 van de 100 gevraagde)
                                if len(res2["items"]) > 90:
                                    # if enough comments, video is accepted
                                    print("Inserting video {} to videos.csv with {} comments...".format(video_id, len(
                                        res2["items"])))
                                    videos_file.write(
                                        '{},{},{},{},"{}"\n'.format(video_id, category_id, published_at, channel_id, title))

                                    # Iterate over all comments
                                    for index_, comment in enumerate(res2["items"]):
                                        content = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                                        # Check if comment is long enough and is in english
                                        # if len(content.split()) > 5 and langdetect.detect(content) == "en":
                                        # This comment is accepted
                                        # print("write comment")
                                        comments_file.writerow([category_id, video_id, content])

                                    remaining_nr_of_videos -= 1
                                    if remaining_nr_of_videos == 0: break

                                else:
                                    print("NOT ENOUGH COMMENTS")
                        else:
                            print("NOT ENGLISH")

            # TODO: Delete i
            i += 1
    # Success
    return True
