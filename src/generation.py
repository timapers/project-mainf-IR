import requests

session = requests.session()

url = "https://www.googleapis.com/youtube/v3/commentThreads"
params = {
    "part": "snippet",
    "videoId": "u02ue6R7dMo",
    "maxResults": 100,
    "textFormat": "plainText",
    "order": "relevance",
    "key": "AIzaSyBRDRhcwwVsz9DNIudB5Z5knD1UMrNdbI0"
}

res = session.get(url, params=params)
res = res.json()
for comment in res["items"]:
    comment = comment["snippet"]["topLevelComment"]["snippet"]
    print(comment["authorDisplayName"], ":", comment["textOriginal"])
    print("--------------------")

for id in range(100):
    url = "https://www.googleapis.com/youtube/v3/videoCategories"
    params = {
        "part": "snippet",
        "id": id,
        "key": "AIzaSyBRDRhcwwVsz9DNIudB5Z5knD1UMrNdbI0"
    }
    res = session.get(url, params=params).json()
    if not res["items"]: continue
    print(id, res["items"][0]["snippet"]["title"])

exit(0)