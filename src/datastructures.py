"""
Movie and Actor classes as well as a Graph datastructure (with Vertices).
"""
from typing import Any
import csv


class Actor:
    """An actor is a data type that stores the various information about an actor/actress
    such as id, name, rating, birth year and death year. Death year will be represented as
    -1 if the person is still alive.

    Instance Attributes:
        - db_id: The id of the actor/actress.
        - name: The name of the actor/actress.
        - birth_year: Year of birth of the actor/actress
        - death_year: Year of death of the actor/actress, -1 if the person is still alive
        - rating: The rating of the actor/actress

        Representation Invariants:
        - item != ''
        - name != ''
        - 1 <= self.rating <= 10
    """
    db_id: str
    name: str
    birth_year: int
    death_year: int
    rating: float

    def __init__(self, db_id: str, name: str, birth_year: int, death_year: int, rating: float = 0.0) -> None:
        """Initialize a new actor/actress with the given information.

        Preconditions:
            - item != ''
            - name != ''
        """
        self.db_id = db_id
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year
        self.rating = rating


class Movie:
    r"""
    A movie is a data type that stores the various information about a movie, including its id, name, release year,
    runtime, genre, director, writers, and the rating. It is important to note that in the original data set \N
    represents not applicable or missing info, but due to python limitations it will be represented as N in this case.

    Instance Attributes:
    - db_id: The id of the movie.
    - name: The title of the movie.
    - release_year: Year of release of the movie.
    - runtime: The runtime of the movie.
    - genre: The genre of the movie.
    - director: The director of the movie.
    - writers: The writers of the movie.
    - rating: The rating of the movie.

    Representation Invariants:
    - self.db_id != ''
    - 1 <= self.rating <= 10
    """
    db_id: str
    name: str
    release_year: int
    runtime: str
    genre: str
    director: str
    writers: set[str] | str
    rating: float

    def __init__(self, db_id: str, name: str, release_year: int, runtime: str,
                 genre: str, director: str = "", writers: set[str] | str = "", rating: float = 0) -> None:
        """Initialize a new movie with the given information.

        Preconditions:
            - item != ''
        """
        self.db_id = db_id
        self.name = name
        self.release_year = release_year
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writers = writers
        self.rating = rating


class _Vertex:
    """A vertex in a book review graph, used to represent a movie or an actor/actress.

    Each vertex item is either a movie or an actor

    Instance Attributes:
        - item: The actor or the movie.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - item is not None
    """
    item: Any
    neighbours: set

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item .

        This vertex is initialized with no neighbours.

        Preconditions:
            - item is not None
        """
        self.item = item
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def __contains__(self, item: Any) -> bool:
        return item in self._vertices

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        The id of the person or movie will correspond to the actor or movie class in the dictionary.

        Preconditions:
            - item is not None
        """
        if item.db_id not in self._vertices:
            self._vertices[item.db_id] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: any = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', Movie, Actor}
        """

        if kind != '':
            return {v.item for v in self._vertices.values() if type(v) == kind}
        else:
            return set(self._vertices.keys())

    def evaluate_all_actor_ratings(self) -> None:
        """
        initiate all the actors' rating by taking the average of the ratings of the movies they are adjacent to.
        """
        # TODO

    def evaluate_collaborative_performance(self, actors: list[str]) -> float:
        """
        actors is a list of the ids of the actors being evaluated.

        This method returns the average score of the movies that all members of the list particpated in.

        If there is no movie that all members of the list participated in, return -1
        """
        # TODO

    def find_best_movie_together(self, actors: list[str]) -> str:
        """
        acotrs is a list of the ids of the actors being evaluated.

        This method returns the id of the movie that has the highest rating that contains all actors in the list.

        If there is no movie that all members of the list participated in, return /N
        """
        # TODO

    def find_casting_team(self, actor: str, number_of_actors: int, min_num_collab) -> list[str]:
        """
        This method returns a list of actors who have collaborated with the actor variable, sorted in descending order
        of their average collaborative performance.

        actor is the id of the actor being found casting team for.

        number of actors refers to the length of the final returned list. The length will be equal or shorter than
        this vairable

        min num collab refers to the minimum amount of movies two actors has to collaborated in for that actor to be
        considered
        """
        # TODO

    def _load_actors(self, names_file: str) -> None:
        """
        Helper function which takes the file name of a names.tsv file and creates all actor vertices within the given
        graph
        """
        with open(names_file, 'r', encoding="utf8") as names:
            names_reader = csv.reader(names, delimiter="\t")
            next(names_reader)
            for line in names_reader:
                death_year = -1
                birth_year = -1
                if line[3] != '\\N':
                    death_year = int(line[3])
                if line[2] != '\\N':
                    birth_year = int(line[2])

                self.add_vertex(Actor(line[0], line[1], birth_year, death_year))

    def _load_movies(self, titles_file: str, ratings_file: str) -> None:
        """
        Helper function which takes the file name of a title.basics.tsv file and a title.ratings.tsv file and creates all
        movie vertices within the given graph.
        """
        with open(titles_file, 'r', encoding="utf8") as titles, open(ratings_file, 'r', encoding="utf8") as ratings:
            titles_reader = csv.reader(titles, delimiter="\t")
            ratings_reader = csv.reader(ratings, delimiter="\t")
            next(titles_reader)
            next(ratings_reader)
            movies = {}
            for line in titles_reader:
                release = 0
                if line[2] != '\\N':
                    release = int(line[2])
                movies[line[0]] = Movie(line[0], line[1], release, line[3], line[4])
            for line in ratings_reader:
                if line[0] in movies:
                    movies[line[0]].rating = float(line[1])
                    self.add_vertex(movies[line[0]])

    def _load_principals(self, principal_file: str) -> None:
        """
        Helper function which takes the file name of a principal tsv file and creates the edges in the graph
        corresponding to the principals.
        """
        with open(principal_file, 'r', encoding="utf8") as principals:
            principal_reader = csv.reader(principals, delimiter='\t')
            for line in principal_reader:
                if line[0] in self and line[1] in self:
                    self.add_edge(line[0], line[1])

    def load_movie_graph(self, actors: str, titles: str, ratings: str, principals: str) -> None:
        """
        Loads actors, movies with corresponding ratings as well as the edges between actors and movies into the graph,
        based on the files which are given.
        """
        self._load_actors(actors)
        self._load_movies(titles, ratings)
        self._load_principals(principals)
