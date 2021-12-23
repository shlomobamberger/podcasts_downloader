import feedparser
import requests
import os
import re


def title_and_posts_from_rss(rss_file):
    news_feed = feedparser.parse(rss_file)
    return {'title': news_feed.channel.title, 'posts': news_feed.entries}


def data_from_post(post):
    return {'link': post.enclosures[0].href, 'title': post.title}


def remove_spacial_char(text):
    return re.sub('\W+', ' ', text)


def main():
    rss_link = ''
    if not rss_link:
        rss_link = input("please enter rss link: ")
    rss_file = requests.get(rss_link).content
    all_post_data = title_and_posts_from_rss(rss_file)
    title = remove_spacial_char(all_post_data["title"])
    posts = all_post_data["posts"]
    print('Starts with a download of ', len(posts), 'episodes from the podcast ' + title)
    if not os.path.exists(title):
        os.makedirs(title)
        print("A new folder " + title + "  has been created")
    for post in posts:
        episode = data_from_post(post)
        file_path = title + '\\' + remove_spacial_char(episode['title']) + '.mp3'
        if not os.path.exists(file_path):
            mp3 = requests.get(episode['link'])
            with open(file_path, 'wb') as f:
                f.write(mp3.content)
        print(f"There are {len(posts) - posts.index(post) - 1} episodes left out of {len(posts)}")
    print('DONE!')


main()
