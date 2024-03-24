"""
This is a ONE TIME RUN file used to take the full IMdB database files (names.tsv, principals.tsv, ratings.tsv,
titles.tsv) and filter them to only contain movies and their corresponding actors (i.e. no series, shorts, etc.)
Each function will create a new, filtered file. Due to the sheer size of the original files (>4GB of plain text),
it's probably unwise to run this on a weak system. The new files will be titles_filtered.tsv, actors_filtered.tsv,
principals_filtered.tsv and ratings_filtered.tsv.
"""
import csv
import operator
import os


def filter_by_movie(read_file: str, write_file: str) -> str:
    """
    Takes a full imdb titles tsv file and returns a file which only contains movies (removes shorts, series, etc.)
    Also removes all movie attributes that aren't relevant to us. Returns the new files name.
    """
    with open(read_file, 'r', encoding="utf8") as titles, open(write_file, 'wt', encoding="utf8", newline='') as movies:
        title_reader = csv.reader(titles, delimiter="\t")
        movie_writer = csv.writer(movies, delimiter="\t")

        for line in title_reader:
            if line[1] == "movie":
                movie_writer.writerow([line[0], line[2], line[5], line[7], line[8]])

        titles.close()
        movies.close()

    return write_file


def filter_ratings(read_ratings_file: str, read_movies_file: str, write_file: str) -> str:
    """
    Takes an imdb ratings tsv file and a filtered movies file and returns a ratings file which only contains the
    rating of the movies. Returns the name of file it wrote to.
    """
    with (open(read_ratings_file, 'r', encoding="utf8") as ratings,
          open(read_movies_file, 'r', encoding="utf8") as movies,
          open(write_file, 'wt', encoding="utf8", newline='') as write):
        ratings_reader = csv.reader(ratings, delimiter='\t')
        movie_reader = csv.reader(movies, delimiter='\t')
        writer = csv.writer(write, delimiter='\t')
        movie_ids = set()

        for line in movie_reader:
            movie_ids.add(line[0])

        for line in ratings_reader:
            if line[0] in movie_ids:
                line_truncated = [line[0], line[1]]
                writer.writerow(line_truncated)

        ratings.close()
        movies.close()
        write.close()
    return write_file


def filter_principals(read_principals_file: str, read_movies_file: str, write_principals_file: str) -> str:
    """
    Filters the principals to only contain movies. Return file name.
    """
    with (open(read_principals_file, 'r', encoding="utf8") as principals,
          open(read_movies_file, 'r', encoding="utf8") as movies,
          open(write_principals_file, 'wt', encoding="utf8", newline='') as write_principals):
        principals_reader = csv.reader(principals, delimiter='\t')
        movie_reader = csv.reader(movies, delimiter='\t')
        principals_writer = csv.writer(write_principals, delimiter='\t')
        movies_set = set()

        for line in movie_reader:
            movies_set.add(line[0])

        for line in principals_reader:
            if line[0] in movies_set:
                principals_writer.writerow([line[0], line[2]])

        principals.close()
        movies.close()
        write_principals.close()

    return write_principals_file


def filter_actors(read_actors_file: str, read_principals_file: str, write_actors_file: str) -> str:
    """
    Given a pre-filtered principals tsv file, creates a file of all actors that appear in this principals file.
    return file name.
    """
    with (open(read_actors_file, 'r', encoding="utf8") as actors,
         open(read_principals_file, 'r', encoding="utf8") as principals,
         open(write_actors_file, 'wt', encoding="utf8", newline='') as write_actors):
        actors_reader = csv.reader(actors, delimiter='\t')
        principals_reader = csv.reader(principals, delimiter='\t')
        actor_writer = csv.writer(write_actors, delimiter='\t')
        actors_set = set()

        for line in principals_reader:
            actors_set.add(line[1])

        for line in actors_reader:
            if line[0] in actors_set:
                actor_writer.writerow([line[0], line[1], line[2], line[3]])

        actors.close()
        principals.close()
        write_actors.close()

    return write_actors_file


def filter_ratings_10k(read_ratings_file: str, read_movies_file: str,
                       write_ratings_file: str) -> set[str]:
    """
    Given a movies tsv file, and a ratings file, create two filtered files which only contains the top
    10 000 movies by rating. Return the set of top 10k movies.
    """
    top_movies = []
    top_movies_set = set()
    with (open(read_movies_file, 'r', encoding="utf8") as movies,
          open(read_ratings_file, 'r', encoding="utf8") as ratings,
          open(write_ratings_file, 'wt', encoding="utf8", newline='') as write_ratings):
        movie_reader = csv.reader(movies, delimiter='\t')
        ratings_reader = csv.reader(ratings, delimiter='\t')
        ratings_writer = csv.writer(write_ratings, delimiter='\t')
        next(ratings_reader)

        for line in movie_reader:
            if line[1] == "movie":
                top_movies_set.add(line[0])

        for line in ratings_reader:
            if line[0] in top_movies_set:
                top_movies.append([line[0], line[1]])

        top_movies.sort(key=operator.itemgetter(1), reverse=True)
        top_movies = top_movies[:10000]
        top_movies_set = {title[0] for title in top_movies}

        for movie in top_movies:
            ratings_writer.writerow(movie)

        movies.close()
        ratings.close()
        write_ratings.close()
    return top_movies_set


def filter_movies_by_set(movies_set: set[str], read_movies_file: str, write_movies_file: str) -> None:
    """
    Given a titles tsv file and a set of movie ids, create a file at specificied location with only the movies
    corresponding to the movie ids.
    """
    with (open(read_movies_file, 'r', encoding="utf8") as movies,
         open(write_movies_file, 'wt', encoding="utf8", newline='') as write_movies):
        movie_reader = csv.reader(movies, delimiter='\t')
        movie_writer = csv.writer(write_movies, delimiter='\t')

        for line in movie_reader:
            if line[0] in movies_set:
                movie_writer.writerow([line[0], line[2], line[5], line[7], line[8]])

        movies.close()
        write_movies.close()


def filter_movies_only(movies_file: str, ratings_file: str, principals_file: str, actors_file: str) -> None:
    """
    Creates filtered versions of all files, containing only movies.
    """
    if not os.path.exists('/movies_only'):
        os.mkdir('movies_only')
    filter_by_movie(movies_file, 'movies_only/titles_filtered.tsv')
    filter_ratings(ratings_file, 'movies_only/titles_filtered.tsv', 'movies_only/ratings_filtered.tsv')
    filter_principals(principals_file, 'movies_only/titles_filtered.tsv', 'movies_only/principals_filtered.tsv')
    filter_actors(actors_file, 'movies_only/principals_filtered.tsv', 'movies_only/actors_filtered.tsv')


def filter_10k_rated(movies_file: str, ratings_file: str, principals_file: str, actors_file: str) -> None:
    """
    Creates filtered versions of all files, containing only the top 10 000 highest rated movies.
    """
    if not os.path.exists('/sample_db'):
        os.mkdir('sample_db')
    movies_set = filter_ratings_10k(ratings_file, movies_file, 'sample_db/ratings_10k.tsv')
    filter_movies_by_set(movies_set, movies_file, 'sample_db/titles_10k.tsv')
    filter_principals(principals_file, 'sample_db/titles_10k.tsv', 'sample_db/principals_10k.tsv')
    filter_actors(actors_file, 'sample_db/principals_10k.tsv', 'sample_db/actors_10k.tsv')


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        "forbidden-io-functions": ["print"],
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'operator', 'os'],
        'max-nested-blocks': 4
    })
    filter_movies_only('full_db/titles.tsv', 'full_db/ratings.tsv',
                       'full_db/principals.tsv', 'full_db/names.tsv')
    filter_10k_rated('full_db/titles.tsv', 'full_db/ratings.tsv',
                     'full_db/principals.tsv', 'full_db/names.tsv')
