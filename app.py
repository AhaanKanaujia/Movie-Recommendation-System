import streamlit as st
import pickle
import pandas as pd
import requests

#Function for getting movie posters
def get_movie_poster(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    if data['poster_path'] != None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return None

#Function for getting movie overviews
def get_movie_overview(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    if data['overview'] != None:
        return "Brief Overview: " + data['overview']
    else:
        return None

#Function for getting movie genres
def get_movie_genres(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    subdata = data['genres']
    names = []
    for i in subdata:
        names.append(i['name'])
    final = ""
    for i in names:
        final += i + ", "
    return "Genres: " + final[:-2]

#Function for getting recommended movie score
def get_movie_score(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    if data['vote_average'] != None:
        return str(data['vote_average'])
    else:
        return None

#Function for getting movie release date
def get_movie_release_date(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    if data['release_date'] != None:
        return data['release_date']
    else:
        return None

#Function for getting movie cast
def get_movie_cast(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    subdata = data['cast']
    names = []
    for i in subdata:
        names.append(i['name'])
    final = ""
    count = 0
    for i in names:
        if count<8:
            final += i + ", "
            count += 1
    return "Cast: " + final[:-2]

#Function for getting movie crew
def get_movie_crew(id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}/credits?api_key=fcd453a130ee7969c7222cdb301689f2&language=en-US".format(id))
    data = response.json()
    subdata = data['crew']
    jobs, names = [], []
    for i in subdata:
        if i['job'] == 'Director' or 'Producer' or 'Writer':
            names.append(i['name'])
            jobs.append(i['job'])
    final = ""
    count = 0
    for i in names:
        if count<3:
            final += jobs[count]+ ": " + i+", "
            count += 1
    return final[:-2]

#Function for making movie recommendations
def recommend_movies(movie):
    
    index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    #Recommended movie details list, poster, cast, crew, and overview
    recommend_movies = []
    recommend_movies_posters = []
    recommend_movies_overview = []
    recommend_movies_genres = []
    recommend_movies_cast = []
    recommend_movies_crew = []
    recommend_movie_scores = []
    recommend_movie_release_date = []
    #List out the 25 most similar movies along with all other details
    for i in movie_list[1:11]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append((movies.iloc[i[0]].title))
        recommend_movies_posters.append(get_movie_poster(movie_id))
        recommend_movies_overview.append(get_movie_overview(movie_id))
        recommend_movies_genres.append(get_movie_genres(movie_id))
        recommend_movies_cast.append(get_movie_cast(movie_id))
        recommend_movies_crew.append(get_movie_crew(movie_id))
        recommend_movie_scores.append(get_movie_score(movie_id))
        recommend_movie_release_date.append(get_movie_release_date(movie_id))
    #Return list of all movie details
    return recommend_movies, recommend_movies_posters, recommend_movies_overview, recommend_movies_genres, recommend_movies_cast, recommend_movies_crew, recommend_movie_scores, recommend_movie_release_date

#Import list of movies
movies_list = pickle.load(open('movies_list.pkl', 'rb'))
#Convert movie list into dataframe
movies = pd.DataFrame(movies_list)
#Load binary files contaning recommended movies based on all parametres 
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie = st.selectbox('Select your Movie!', movies['title'].values)

if st.button('Recommend Similar Movies'):
    recommended_movie_names,recommended_movie_posters, recommended_movie_overview, recommended_movie_genres, recommended_movie_cast, recommended_movie_crew, recommended_movie_score, recommend_movie_release_date = recommend_movies(selected_movie)
    for i in range(9):
        col1, col2 = st.columns(2)
        with col1:
            st.header(str(i+1)+". "+recommended_movie_names[i])
            st.subheader("Audience Score: "+ str(recommended_movie_score[i]))
            st.subheader("Released On: "+recommend_movie_release_date[i])
            st.image(recommended_movie_posters[i])
        with col2:
            st.subheader((recommended_movie_crew[i]))
            st.subheader(recommended_movie_overview[i])
            st.subheader(recommended_movie_genres[i])
            st.subheader(recommended_movie_cast[i])
