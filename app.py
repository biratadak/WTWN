import random
import string

import requests
import streamlit as sl
import pickle

training_df = pickle.load(open('training_df.pkl', 'rb'))
similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))


def fetch_posters(id_no):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=e0035eec8b740ca0eb379c23708822a4".format(id_no)).json()
    return "https://image.tmdb.org/t/p/w500/" + response['poster_path']


def get_movies(movie):
    movie_index = [i for i in training_df[training_df["original_title"] == movie].index]
    similarity = similarity_matrix[[i for i in movie_index][0]]
    movie_dict = {}
    for i in ((sorted(list(enumerate(similarity)), key=lambda x: x[1], reverse=True))[1:no_of_recommendations + 1]):
        movie_dict.update({(training_df[training_df.index == i[0]]["id"].values[0]): (
            training_df[training_df.index == i[0]]["original_title"].values[0])})
    return movie_dict


sl.title("WHAT TO WATCH NOW")
sl.subheader("GET YOUR FAV MOVIE HERE")

x = sl.slider('How many movies to suggest?', 2, 5)


def autocolumn(i):
    temp1 = []
    for x in range(i):
        temp1.append(random.choice(string.ascii_uppercase) + str(x))
    if i == 2:
        temp1[0:1] = sl.columns(2)
        with temp1[0]:
            sl.markdown("🎬")
        with temp1[1]:
            sl.markdown("🍿")

    elif i == 3:
        temp1[0:2] = sl.columns(3)
        with temp1[0]:
            sl.markdown("🎬")
        with temp1[1]:
            sl.markdown("🍿")
        with temp1[2]:
            sl.markdown("🎥")
    elif i == 4:
        temp1[0:3] = sl.columns(4)
        with temp1[0]:
            sl.markdown("🎬")
        with temp1[1]:
            sl.markdown("🍿")
        with temp1[2]:
            sl.markdown("🎥")
        with temp1[3]:
            sl.markdown("📀")
    elif i == 5:
        temp1[0:4] = sl.columns(5)
        with temp1[0]:
            sl.markdown("🎬")
        with temp1[1]:
            sl.markdown("🍿")
        with temp1[2]:
            sl.markdown("🎥")
        with temp1[3]:
            sl.markdown("📀")
        with temp1[4]:
            sl.markdown("🎞")


autocolumn(x)
no_of_recommendations = x

option = sl.selectbox(
    "Write down the movie name"
    , training_df["original_title"])
recommendations = get_movies(option).items()

if sl.button('Get Recommendations'):
    for i in recommendations:
        sl.write(i[1])
        sl.image(fetch_posters(i[0]), width=333)
