import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = 'https://api.themoviedb.org/3/movie/{}?api_key=078c2117f16d4448d892a2d1a9f46f0f&language=en-US'.format(movie_id)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "No poster found for this movie."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies =pd.DataFrame(movie_dict)



similarity = pickle.load(open('similarity.pkl','rb'))


def recommend(movie):

    index = movies[movies['title'] == movie].index[0]
    distance = similarity[index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])

    recommend_movie =[]
    recommend_poster  = []
    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster



st.title('Movie Recommender system')
selected_movie = st.selectbox(
    "Select your movie",
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    print(recommended_movie_posters)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            if idx < len(recommended_movie_names):
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx])


