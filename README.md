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

# Our Program
Our first step was turning the four IMDb tsv files into a usable dataset. All of this is done in the ```db_filter.py``` file. First we filter out all tv series, short films, etc. We also filtered out all adult films to ensure this dataset stays family friendly. From there we also filter the ratings file, limit the actors to only contain movie actors, as well as getting rid of any non-actor principals. ```db_filter.py``` creates multiple different datasets from the four source files. One dataset contains all (non-adult film) movies in the IMDb database, as well as the corresponding actors, principals and ratings. Another dataset contains only the top 10 000 movies by rating (although each movie has to surpass a 100 review threshold). This is the dataset included as a sample. Due to size limitations, we haven't included the full IMDb database, and ```db\_filter.py``` won't actually be run when executing ```main.py```, since transforming the source data set takes a few minutes. Another option within ```db_filter.py``` is to create custom sized datasets which take the top n movies by rating. 

Our graph comes into play in the ```datastructures.py``` file. Here we defined classes for Actors and Movies containing the relevant information, as well as our movie_graph structure. First of all, the four filtered data files created in ```db_filter.py``` are read and loaded into a movie graph. Here, each actor is connected to the movies they've played in. Next, we have created a function which gets the average rating of an actor, based on the ratings of the movies they've played in. Here the graph is helpful since we can just fetch all the neighbor vertices to each actor and calculate an average.

Our main computational functions to analyze the dataset are ```evaluate_collaborative_performance```, \\
```find_best_movie_together``` and ```find_casting_team``` in the ```datastructures.py``` file:
    - ```evaluate_collaborative_performance```: This function takes one or more actors and evaluates the average score of all movies they have collaborated on. Once again the graph structure allows us to quickly find neighbors to both actors and evaluate their scores.
    - ```find_best_movie_together```: As the name implies, this function takes one or more actors and finds the highest rated movie they have collaborated on. Once again the graph allows us to first find all collaborations and pick out the highest rated movie.
    - ```find_casting_team```: This function takes an actor, as well as a certain amount of costars, and the minimum number of collaborations this actor has had with the costars. Based on these parameters, the function finds the highest rated collaborative group of cast members. This is meant as a sort of imaginary directors function, which builds a dream cast based on the IMDb scores. The graph allows us to quickly find costars and ratings and evaluate the 'perfect' cast built around one actor.

Our work comes together in the ```interface.py``` file. Here we've implemented a visual interface to use all these functions, using a library called PySimpleGUI [2], as well as plotly[3] and networkx[4] to visualize the graph. The interface consists of a drop down menu which allows the user to choose between the three functions we've explained previously, as well as getting a visualization of the graph. Here the user can create casts around their favorite actors, find the best movie in which multiple actors have collaborated, or find the average rating of multiple actors that have worked together.

# Running The Program
To run our project, first download the database files from the IMDb website linked in the references. Then use ```db_filter.py``` to get the desired dataset to be analyzed. When all required files are in one folder, simply run \texttt{main.py} (You may have to adjust the file names in interface.py if the names don't match)! In our actual interface, the dropdown menu should be pretty intuitive, but for testing purposes, here are some fun examples to test on each function: 
- **The average performance of a group of actors:**
  - Robert Downey Jr., Tom Holland, Mark Ruffalo
  - Rupert Grint, Emma Watson, Daniel Radcliffe
  - Elijah Wood, Ian McKellen, Orlando Bloom
- **the best performing movie by a group of actors:**
  - Adrien Brody, Willem Dafoe, Bill Murray
  - Christian Bale, Heath Ledger, Gary Oldman
  - Brad Pitt, Edward Norton
- **the castmates of a particular actor:**
  - Morgan Freeman, 5, 2
  - Robert De Niro, 3, 3
  - Tom Hanks, 5, 3
    
# Discussion
Overall, we would consider our project to be a success. We created an interactive way of finding correlations between actors, based on IMDb ratings. It's fun exploring who works best with whom, building imaginary casts and finding good movies based on your favorite actors. One issue we kept struggling with is finding the right scope of data. Movies with few reviews, adult films, and many other factors blurred the dataset and had to be dealt with first. For example, we noticed that getting rid of the minimum 100 review limit filled the graph with an estimated 80\% bollywood movies, many of which had only a handful reviews (which were all outstanding, and therefore prioritized). 

A limitation to our program is that one has to know the precise spelling of an actors name, and that more niche actors get pushed back in a filtered dataset. One issue was also finding a balance between a meaningful dataset and a feasible size. If the dataset was too small, there were no correlations, too large and it would take egregious amounts of RAM and compute time. Another thing we thought about was limiting a time frame, since the IMDb database goes all the way back to the start of the 20. century, and actors and movies this early on don't really connect to modern actors/ movies in any meaningful way. 

A next step would be incorporating tv series and short films as well, which isn't that big of a step, since it's only a question of filtering the dataset differently. Another idea would be grouping not just by collaborations, but by closely related movies or genres, which is a bit harder to do. We could also improve our interface with autocorrect, suggestions, etc., but that would take quite a while. Maybe swapping from tsv files to a rigid database structure would also improve the experience (since we could implement SQL query and such).

In summary, we feel like we achieved our goal overall, and although there are a few limitations, these don't hold back the capabilities of our project very much.


## References:
1. "IMDb Non-Commercial Datasets", IMDb Developer, https://developer.imdb.com/non-commercial-datasets/ 
2. "PySimpleGUI", PySimpleGUI, https://www.pysimplegui.com/ 
4. "Plotly Open Source Graphing Library for Python", Plotly Graphing Libraries, https://plotly.com/python/ 
3. "Software for Complex Networks", NetworkX, https://networkx.org/documentation/stable/ 
