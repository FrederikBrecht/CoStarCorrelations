"""
Movie and Actor classes as well as a Graph datastructure (with Vertices).
"""
from typing import Any


class Actor:
    """An actor is a data type that stores the various information about an actor/actress
    such as id, name, rating, birth year and death year. Death year will be represented as
    -1 if the person is still alive.

    Instance Attributes:
        - item: The id of the actor/actress.
        - name: The name of the actor/actress.
        - birth_year: Year of birth of the actor/actress
        - death_year: Year of death of the actor/actress, -1 if the person is still alive
        - rating: The rating of the actor/actress

        Representation Invariants:
        - item != ''
        - name != ''
        - 1 <= self.rating <= 10
    """
    item: str
    name: str
    birth_year: int
    death_year: int
    rating: float

    def __init__(self, item: str, name: str, birth_year: int, death_year: int) -> None:
        """Initialize a new actor/actress with the given information.

        Preconditions:
            - item != ''
            - name != ''
        """
        self.item = item
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year


class Movie:
    """A movie is a data type that stores the various information about a movie,
    including its id, name, release year, runtime, genre, director writers, and the rating

    It is important to note that in the original data set \N represents not applicable or missing info,
    but due to python limitations, it will be represented as /N in this case.

    Instance Attributes:
        - item: The id of the movie.
        - name: The title of the movie.
        - release_year: Year of the release of the movie.
        - runtime: The runtime of the movie.
        - genre: The genre of the movie.
        - director: The director of the movie
        - writers: The writers of the movie
        - rating: The rating of the movie

        Representation Invariants:
        - item != ''
        - 1 <= self.rating <= 10
    """
    item: str
    name: str
    release_year: int
    runtime: str
    genre: str
    director: str
    writers: set[str]
    rating: float

    def __init__(self, item: str, name: str, release_year: int, runtime: str,
                 genre: str, director: str, writers: set[str], rating: float) -> None:
        """Initialize a new movie with the given information.

        Preconditions:
            - item != ''
        """
        self.item = item
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

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        The id of the person or movie will correspond to the actor or movie class in the dictionary.

        Preconditions:
            - item is not None
        """
        if item.item not in self._vertices:
            self._vertices[item.item] = _Vertex(item)

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
