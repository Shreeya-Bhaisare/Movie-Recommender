import pandas as pd
import streamlit as st
import pickle
import requests

# Define a placeholder image URL
PLACEHOLDER_IMAGE_URL = "https://via.placeholder.com/500x750?text=No+Poster+Available"

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d4cd2c42d11081b7090d20a4f626f82d&language=en-US".format(movie_id)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return PLACEHOLDER_IMAGE_URL  # Return placeholder image URL if no poster path
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return PLACEHOLDER_IMAGE_URL  # Return placeholder image URL on request failure

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # to get index of the movie
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies_list
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
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