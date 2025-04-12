
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c287db735c798ff2107fbcee26566e53&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_poster_by_title(title):
    response = requests.get(
        f'https://api.themoviedb.org/3/search/movie?api_key=c287db735c798ff2107fbcee26566e53&query={title}'
    )
    data = response.json()
    if data['results']:
        return "https://image.tmdb.org/t/p/w500/" + data['results'][0]['poster_path']
    return "https://via.placeholder.com/500"

def recommend(movies):
    movies_index = moviess[moviess['title'] == movies].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # Check for the existence of 'movie_id'
        if 'movie_id' in moviess.columns:
            movie_id = moviess.iloc[i[0]]['movie_id']
            poster = fetch_poster(movie_id)
        else:
            # Fallback to fetching poster by title
            title = moviess.iloc[i[0]]['title']
            poster = fetch_poster_by_title(title)

        recommended_movies.append(moviess.iloc[i[0]]['title'])
        recommended_movies_posters.append(poster)

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
moviess = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', moviess['title'].values)

if st.button('Recommend'):
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

