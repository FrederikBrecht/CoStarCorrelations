"""
Functions responsible for taking the tsv files from the IMdB database and parsing them to match the classes
and datastructures provided in datastructures.py
"""
from datastructures import Graph, Movie, Actor

def load_movie_graph() -> Graph:

    """Return a movie graph corresponding to the given datasets.

    The movie graph stores all the information from the files as follows:
    Create one vertex for each movie, and one vertex for every actor/actress in the datasets.
    Edges represent an actor/actress' participation in the movie (that is, there is an edge between an
    actor/actress and a movie they have performed in).

    The vertices of the 'actor' kind should contain an actor class.
    The vertices of the 'movie' kind should contain a movie class.

    Use the "kind" _Vertex attribute to differentiate between the two vertex types.

    Note: In this graph, each edge only represents the actor/actress' particpation in a movie
    """
