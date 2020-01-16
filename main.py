import requests
import string
import json
from vk_api import VkApi
from vk_api import VkUpload
import praw
import time
from datetime import timezone
from datetime import datetime
import os
import urllib.request

with open("vk_data.json", "r") as read_file1:
        vk_data = json.load(read_file1)
with open("reddit_data.json", "r") as read_file2:
        reddit_data = json.load(read_file2)

class vk_class:
    login = vk_data["login"]
    password = vk_data["password"]
    access_token = vk_data["access_token"]
    owner_id = vk_data["owner_id"]
    session = VkApi(login=login,
                    password=password,
                    token=access_token)

class reddit_class:
    client_id = reddit_data["client_id"]
    client_secret = reddit_data["client_secret"]
    password = reddit_data["password"]
    user_agent = reddit_data["user_agent"]
    username = reddit_data["username"]
    subreddit = reddit_data["subreddit"]
    limit = reddit_data["limit"]
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         user_agent=user_agent,
                         username=username)

def reddit_parse(subreddit, vk):
    unix = int(time.time()) + 3600
    for sub in subreddit.hot(limit=reddit_class.limit):
        try:
            os.remove("img.jpg")
        except:
            pass
        post_title = sub.title
        try:
            img = img_load(sub)
        except:
            continue
        print(f'{post_title}')
        try:
            post_pic = vk_img_load(img); print('Got server for picture...', end=' ')
        except:
            continue
        print(post_pic)
        time.sleep(3)
        try:
            vk_post(vk, vk_class.owner_id, post_title, post_pic, unix)
        except:
            print('Couldnt load an image to vk')
            continue
        print(f'{img} -> Successfully loaded to vk')
        unix += 2 * 60 * 60

def img_load(sub):
    resource = urllib.request.urlopen(sub.url)
    out = open("img.jpg", 'wb')
    out.write(resource.read())
    out.close()
    img = 'img.jpg'
    return img

def vk_img_load(img):
    upload = VkUpload(vk_class.session)
    photos = [f'{img}']
    photo_list = upload.photo_wall(photos)
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
    return attachment

def vk_post(vk, owner_id, post_title, post_pic, unix):
    vk.wall.post(owner_id=owner_id,
                 from_group = 1,
                 message = post_title,
                 attachments = post_pic,
                 publish_date = int(unix))
    time.sleep(1)

def main():
    vk = vk_class.session.get_api()
    reddit = reddit_class.reddit
    reddit.read_only = False
    subreddit = reddit.subreddit(reddit_class.subreddit)
    while True:
        reddit_parse(subreddit, vk)
        print("Posted!")
        for sleep in range(26*12):
            time.sleep(290)
            print("im awake im alive")

if __name__ == "__main__":
    main()

read_file1.close()
read_file2.close()