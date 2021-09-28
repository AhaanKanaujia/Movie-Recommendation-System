# Movie-Recommendation-System

This is a content based movie recommendation system that utilizes machine learning to suggest similar movies based on user input. 
The website employs the Bag-of-Words machine learning model uses cosine similarity to analyze the similarity between 2 strings of text.
The website uses a 5000 movie database and a TMDB API to pull movie details for displaying and comparing movie data. After running the model,
the top 10 most similar movies are displayed along with its movie poster, audience score, release date, cast, crew, genres, and a brief overview. 
The website is hosted online on the Heroku platform with the URL https://movies-rec-system-ahaank.herokuapp.com/. 

How the Website Works:

Concept: 

Every movie in the database is assigned a piece of text, called tags, which is created by combining the cast, crew, genre, overview, and synopsis text of movie.
Next, a bag of words is created, which include all the words present in all the tags assigned to all 5000 movies. Next, we compare every movie's tags
with the bag of words and create a vector of 0's and 1's depending on if a word in a movie's tags is found in the bag of words. And finally, we compare vectors
of 2 movies to create a list of the most similar movies, which are displayed on the website by utilizing a TMDB API.

Example:

Avatar: ["sci-fi", "action", "samworthington"], John Wick: ["action", "keanureeves"], Inception: ["adventure", "thriller", "leonardodicaprio"]

Thus, the bag of words created: ["sci-fi", "action", "samworthington", "keanureeves", "adventure", "thriller", "leonardodicaprio"] of 7 words.

Now, every movie can be assigned a vector in 7 dimensions depending on if a word from the bag of words appears in the tags of the movies.

As such, Avatar is assigned a vector: [1, 1, 1, 0, 0, 0, 0, 0] since "sci-fi", "action", and "samworthington" is present in the tags of the movies.

Similarly, John Wick is assigned the vector: [0, 0, 0, 1, 1, 0, 0, 0] and Inception is assigned the vector: [0, 0, 0, 1, 1, 0, 0, 0].

And finally, to compare the movies, we use cosine similarity to find the angle between the two vectors in 7 dimensions. The lesser the angle is between
two vectors, the more similar they are. So, a 2 movies with an angle of difference of 10 degrees is more similar than 2 movies with an angle 140 degrees.
As such, a list is created and the top 10 movies from the list are displayed.

Front-End:

The python framework, Streamlit is used to display the movies. The data regarding the movies, movie poster, audience score, release date, 
cast, crew, genres and a brief overview, are pulled from a public TMDB(The Movie Database) API and displayed on the website. 
