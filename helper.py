
import os
from collections import Counter

import emoji
import numpy as np
import pandas as pd
from PIL import Image
from scipy.ndimage import gaussian_gradient_magnitude
from urlextract import URLExtract
from wordcloud import WordCloud, ImageColorGenerator

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 1).reset_index().rename(
        columns={'user': 'Most Vaila Person', 'count': 'contributed to chat'})
    return x,df

def create_wordcloud(selected_user,df):

    # filter user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group notifications & media
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # remove stopwords

    # combine all messages into text
    text = temp['message'].str.cat(sep=" ")

    # --------- PARROT IMAGE MASK PART ---------
    d = os.getcwd()

    parrot_color = np.array(Image.open(os.path.join(d, "parrot.png")))
    parrot_color = parrot_color[::3, ::3]

    parrot_mask = parrot_color.copy()
    parrot_mask[parrot_mask.sum(axis=2) == 0] = 255

    edges = np.mean(
        [gaussian_gradient_magnitude(parrot_color[:, :, i] / 255., 2) for i in range(3)],
        axis=0
    )
    parrot_mask[edges > .08] = 255

    # create wordcloud with mask
    wc = WordCloud(
        max_words=2000,
        mask=parrot_mask,
        max_font_size=40,
        random_state=42,
        relative_scaling=0,
        background_color="white"
    )

    wc.generate(text)

    # color from image
    image_colors = ImageColorGenerator(parrot_color)
    wc = wc.recolor(color_func=image_colors)

    return wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

