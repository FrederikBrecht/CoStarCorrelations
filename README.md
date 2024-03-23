# CoStarCorrelations
By Katelynn Bai, Frederik Brecht, Jordan Shao
## Problem Description and Research Question
Our team has decided to analyze the domain of movies and actors. A specific challenge filmmakers and directors face when creating a movie is casting. With all the drama and politics surrounding actors and actresses nowadays, it's probably a daunting task to find a set of performers which don't just fit the script, but also work well together. Our project will try to answer the question **which actors and actresses, when starring together in a movie, produce the best possible (critically evaluated) film? Additionally, when given a specific actor or actress, which actors and actresses do they best work with according to movie reviews?** Nowadays, a lot of good performing pairs or groups are described as having a certain 'chemistry' which makes them work together seamlessly to portray the characters we know and love in movies. With our approach to modelling connections between actors, actresses and movies based on critical reception, we are essentially trying to remove some of the mystique from the 'chemistry' between actors and find objective correlations. 
This isn't just interesting from a casting perspective, but may also be fun for the viewers, since they can find correlations between their favorite actors and actresses and other performances, as well as connections to movies. This may make the Friday-evening movie night choice easier, or kick start an appreciation for film not just as a form of entertainment but as an art form. 
## Computational Plan
The domain we have in mind is all actors and movies (not including TV shows) listed in the IMDb non-commerical database. IMDb offers data sets as tsv files which are updated daily and can be freely downloaded. The non-commercial database doesn't offer the full scope of the website, but it's as close to a comprehensive movie and actor dataset as one can access freely, and since IMDb are a pretty widely accepted accumulator of review scores, we can utilize those for calculations.

First of all we will create movie and actor classes, which store data on actors and movies. The most relevant metric here will be the IMDb score of the movies, since we base most of our calculations around these, but we'll also include birth and death year as well as movies they've played in for actors. For movies, we'll include the rating, original title, release year, runtime, genres, directors, writers and actors/actresses.

The way we will represent and organize this data using graphs is by creating vertices of the type 'actor' or 'movie'. The neighboring vertices of a vertex have to be of the other type, meaning the neighbors of an actors vertex would be all the movies they have performed in, and the neighbors of a movie vertex would be all the actors who performed in the movie. Each vertex will also have a score, which in the case of an actor represents the average score of all their roles. For a movie, it'll simply be IMDb's cumulative review score. 

The IMDb non-commercial database separates the data into multiple different files. A daily version of these can be downloaded at the IMDb Non-Commercial Datasets website [1]. We fill be using the following:

- **name.basics.tsv** This file contains names, birth year, death year (if applicable) and most importantly a unique alphanumeric identifier code (and a few other data points we will ignore). The id is consistent throughout the rest of the database, which will allow us to link actors to movies. An excerpt of the file looks like this:

  ```
  nconst  primaryName  birthYear  deathYear  primaryProfession  knownForTitles 
  ... 
  nm0000150  Michael J. Fox  1961  \N  actor,producer,miscellaneous  tt0116365,tt0088763,tt0096874,tt0115369 
  nm0000151  Morgan Freeman  1937  \N  actor,producer,soundtrack	tt0405159,tt0097239,tt0114369,tt0468569 
  nm0000152  Richard Gere  1949  \N  actor,soundtrack,producer	tt0084434,tt0100405,tt0119395,tt0299658
  ...
  ```

- **title.basics.tsv**. This file contains name of a title, as well as original title, release date, runtime and genres and a unique identifier (and once again a few other parameters we will ignore). This file spans across short form films, tv episodes and series as well, but we will filter this by the titletype parameter to only include movies. Once again the unique id is important since it is persistent throughout the database. This would be an excerpt of the file:

  ```
  tconst  titleType  primaryTitle  originalTitle  isAdult  startYear  endYear  runtimeMinutes  genres 
  ... 
  tt0111161  movie  The Shawshank Redemption  The Shawshank Redemption  0  1994  \N  142  Drama 
  ... 
  tt4154796  movie  Avengers: Endgame  Avengers: Endgame  0  2019  \N  181  Action,Adventure,Drama 
  ... 
  ```

- **title.ratings.tsv**. This file stores all the ratings of content, according to their unique id (which corresponds to the ids in the title.basics.tsv file. Structure:

  ```
  tconst  averageRating  numVotes 
  ... 
  tt0111161  9.3  2864837 
  ... 
  tt4154796  8.4  1251966 
  ... 
  ```

- **title.principals.tsv**. This file contains the movie ids and correlates each to the people who worked on the movie (actors, directors, etc.). Utilizing this, we can create edges between actors and movies. Structure:

  ```
  tconst  ordering  nconst  category  job  characters
  ... 
  tt0111161  1  nm0000209  actor  \N  ["Andy Dufresne"]
  tt0111161  2  nm0000151  actor  \N  ["Ellis Boyd 'Red' Redding"]
  tt0111161  3  nm0348409  actor  \N  ["Warden Norton"]
  ...
  ```

The computations will first of all require evaluating the entire data set, matching movies, ratings and actors/ actresses and creating the appropriate graph. We will also have to calculate actors average scores based on this dataset. Then, we plan to implement a method which takes two or more actors and checks the average score between all movies they have co-starred in. Another method would allow the user to input one specific actor or actress, and return a list of the actors/ actresses this specific performer works best with. This would be our imaginary 'casting function', since it displays which actors work well together or which actors critics and the audience like to see together. Another function will allow the user to input two or more actors/actresses, and return the best movie these actors have made together. We could also expand on this function by implementing a parameter which takes the minimum amount of times these actors have worked together, to filter out any 'flukes' or 'one-hit wonders'. All of these functions will be implemented by traversing the graph and averaging/ accumulating/ finding connections between the actors/actresses and the movies and their corresponding scores. Simple options for the user could also be returning all the movies an actor/ actress has worked on, or returning a list of actors for a movie. 

In terms of an interface, the user will have the option to choose between the different functions we are going to implement (ideally through a GUI, utilizing networkx, tkinter and plotly), and input actors/ actresses (either one, two or more depending on the function) into a text field. Then after doing the computation, the user will receive a movie/ list of movies/ list of actors, with some additional information on each. 

We will utilize networkx since it can be used to visualize graphs. Specifically the draw_networkx and draw_networkx_labels methods may be helpful to represent a graph of actors and movies with all their attributes, like dates, runtime (for movies) or birth dates (for actors). We may also use tkinter to create a GUI, which a user can then interact with.

## References:
1. "IMDb Non-Commercial Datasets", IMDb Developer, (https://developer.imdb.com/non-commercial-datasets/)
2. Makhija, Khushal, "Graph Visualization using Python( Matplotlib , Networkx )", (https://www.youtube.com/watch?v=Z-KWnn4\_\_BM)
3. "Matplotlib 3.8.3 documentation", matplotlib,  (https://matplotlib.org/stable/index.html) 
4. "Software for Complex Networks", NetworkX, (https://networkx.org/documentation/stable/)
5. "Plotly Open Source Graphing Library for Python", Plotly Graphing Libraries, (https://plotly.com/python/)
