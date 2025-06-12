
import streamlit as st
import pickle
import requests

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "d4e0c696a9d339b8dc2227902cee5ad5"

def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url)
        data = response.json()
        poster_path = data['results'][0]['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    except:
        return "https://via.placeholder.com/150x220.png?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_titles = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movie_titles.append(title)
        recommended_movie_posters.append(fetch_poster(title))
    return recommended_movie_titles, recommended_movie_posters


st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie to get recommendations", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    st.subheader("Top 5 Recommendations:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], caption=names[i], use_container_width=True)