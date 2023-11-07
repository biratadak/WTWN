import requests
import streamlit as sl
import pandas as pd
import ast
import pickle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

no_of_features = 50
no_of_recommendations = 5

movies = pd.read_csv('../../pycharmProjects/WTWN/movie names.csv')
crew = pd.read_csv('../../pycharmProjects/WTWN/crew names.csv')
crew.rename(columns={'movie_id': 'id'}, inplace=True)
movies = movies.merge(crew, on="id")
movies.drop(
    columns={"budget", "homepage", "overview", "popularity", "revenue", "runtime", "status", "tagline", "title_x",
             "title_y", "vote_average", "vote_count", "spoken_languages"}, inplace=True)
movies.dropna(inplace=True)
movies.isnull().sum()



def getDetails(obj):
    data = []
    for i in ast.literal_eval(obj):
        data.append(i["name"])
    return data


def getDirector(obj):
    director = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            director.append(i["name"])
    return director


def getProducer(obj):
    producer = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Producer":
            producer.append(i["name"])
    return producer


def getEditor(obj):
    editor = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Editor":
            editor.append(i["name"])
    return editor


def stemer(s):
    ps = PorterStemmer()
    temp_lst = []
    for i in s.split():
        temp_lst.append(ps.stem(i))
    return temp_lst


movies.loc[:, "genres"] = movies.loc[:, "genres"].apply(getDetails)
movies.loc[:, "keywords"] = movies.loc[:, "keywords"].apply(getDetails)
movies.loc[:, "production_companies"] = movies.loc[:, "production_companies"].apply(getDetails)
movies.loc[:, "production_countries"] = movies.loc[:, "production_countries"].apply(getDetails)
movies.loc[:, "cast"] = movies.loc[:, "cast"].apply(getDetails)
movies.loc[:, "directors"] = movies.loc[:, "crew"].apply(getDirector)
movies.loc[:, "producers"] = movies.loc[:, "crew"].apply(getProducer)
movies.loc[:, "editors"] = movies.loc[:, "crew"].apply(getEditor)
movies.drop(columns="crew", inplace=True)
movies.loc[:, "genres"] = movies.loc[:, "genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "keywords"] = movies.loc[:, "keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "production_companies"] = movies.loc[:, "production_companies"].apply(
    lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "production_countries"] = movies.loc[:, "production_countries"].apply(
    lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "cast"] = movies.loc[:, "cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "directors"] = movies.loc[:, "directors"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "producers"] = movies.loc[:, "producers"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "editors"] = movies.loc[:, "editors"].apply(lambda x: [i.replace(" ", "") for i in x])
movies.loc[:, "release_date"] = movies.loc[:, "release_date"].apply(lambda x: [str(int(x[0:4]) // 100)])
movies.loc[:, 'tags'] = movies.loc[:, "genres"] + movies.loc[:, "keywords"] + movies.loc[:,
                                                                              "production_companies"] + movies.loc[:,
                                                                                                        "production_countries"] + movies.loc[
                                                                                                                                  :,
                                                                                                                                  "release_date"] + movies.loc[
                                                                                                                                                    :,
                                                                                                                                                    "cast"] + movies.loc[
                                                                                                                                                              :,
                                                                                                                                                              "directors"] + movies.loc[
                                                                                                                                                                             :,
                                                                                                                                                                             "producers"] + movies.loc[
                                                                                                                                                                                            :,
                                                                                                                                                                                            "editors"]
training_df = movies.loc[:, ["id", "original_title", "tags"]]
training_df.loc[:, "tags"] = training_df.loc[:, "tags"].apply(lambda x: " ".join(x))
training_df.loc[:, 'tags'] = training_df.loc[:, 'tags'].apply(lambda x: x.lower())
training_df.loc[:, "tags"] = training_df.loc[:, "tags"].apply(stemer).apply(lambda x: " ".join(x))

vectorizer = CountVectorizer(max_features=no_of_features, stop_words='english')
vectors = vectorizer.fit_transform(training_df["tags"])
similarity_matrix = cosine_similarity(vectors)





pickle.dump(training_df, open('training_df.pkl', 'wb'))
pickle.dump(similarity_matrix, open('similarity_matrix.pkl', 'wb'))