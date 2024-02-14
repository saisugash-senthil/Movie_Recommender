import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os

def fetch_poster(movie_id, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=286f68097bd452ef9842c97fa7cc4c85&language=en-US')
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        except requests.exceptions.RequestException as e:
            retries += 1
            st.warning(f"Failed to fetch data (retry {retries}/{max_retries}). Retrying in {2 ** retries} seconds...")
            time.sleep(2 ** retries)
    st.error("Max retries reached. Unable to fetch data.")
    return None
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters
file_name = "movie_dict.pkl"
file_path = os.path.join(script_directory, file_name)
with open(file_path, 'rb') as file:
movies = pd.DataFrame(movies_dict)
script_directory = os.path.dirname(os.path.abspath(__file__))
similarity_path = os.path.join(script_directory, "similarity.pkl")
similarity = pickle.load(open(similarity_path, 'rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
'Which movie do you want to select?',
movies['title'].values)
if st.button('Check for recommendations'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5= st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

