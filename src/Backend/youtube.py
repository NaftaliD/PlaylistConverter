from googleapiclient.discovery import build
import json

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

api_key = data['youtube']['api_key']

youtube = build('youtube', 'v3', developerKey=api_key)  # public accses aproch, no user auth required

youtube.close()
