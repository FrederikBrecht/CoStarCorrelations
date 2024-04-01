""""
This python file will handle all the functions for an interactive interface.
"""

# import pygame
import PySimpleGUI as sg
import networkx as nx
from plotly.graph_objs import Scatter, Figure
import datastructures


# FINAL VARIABLES
METHODS = ["The average performance of a group of actors",
           "The best performing movie of a group of actors",
           "The castmates of a particular actor",
           "See a graph of all the movies and actors! (May take a while)"]


BEST_MOVIE_TEXT = "The actors\' best movie together was: "
CASTMATES_TEXT = "The casting team created from highest to lowest collaborative performance is: "
ACTOR_MISSING = "Sorry, at least one actor was not found. Try checking your spelling or formatting."
NOT_ALL_ACTORS = "Sorry, there were no movies containing all actors. Try checking your spelling or formatting."
ENTER_N = "Please enter the actors\' names in First/Last order, separated by commas and spaces except for at the end"

MARGINS = (300, 250)
NORMAL_FONT = ("Arial", 20)
SMALLER_FONT = ("Arial", 14)
SMALL_FONT = ("Arial", 10)

ACTOR_MOVIE_GRAPH = datastructures.Graph()
ACTOR_MOVIE_GRAPH.load_movie_graph("data/sample_db/actors_10k.tsv", "data/sample_db/titles_10k.tsv",
                                   "data/sample_db/ratings_10k.tsv", "data/sample_db/principals_10k.tsv")
ACTOR_MOVIE_GRAPH.evaluate_all_actor_ratings()

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
ACTOR_COLOUR = 'rgb(89, 205, 105)'
MOVIE_COLOUR = 'rgb(105, 89, 205)'


# FUNCTIONS====================================
def run_collabs() -> None:
    """ Runs the screen for evaluate_collaborative_performance from datastructures.py

    """
    while True:
        _event, _values = COLLAB.read()
        # print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            COLLAB["-COLLAB-"].update(value="The actors\' average score working together was: ")
            COLLAB.hide()
            break

        if _event == "Submit":
            actor_list = _values[0].split(", ")

            # print(actor_list)
            try:
                actor_id = [ACTOR_MOVIE_GRAPH.get_id(n) for n in actor_list]
            except ValueError:
                COLLAB["-COLLAB-"].update(value=ACTOR_MISSING)
            else:
                score = ACTOR_MOVIE_GRAPH.evaluate_collaborative_performance(actor_id)
                if score != -1:
                    COLLAB["-COLLAB-"].update(value="The actors\' average score working together was: " + str(score))

                else:
                    COLLAB["-COLLAB-"].update(value=NOT_ALL_ACTORS)


def run_best_movie() -> None:
    """ Runs the screen for find_best_movie_together in datastructures.py

    """
    while True:
        _event, _values = BEST.read()
        # print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            BEST["-MOVIE-"].update(value=BEST_MOVIE_TEXT)
            BEST.hide()
            break

        if _event == "Submit":
            actor_list = _values[0].split(", ")
            try:
                actor_id = [ACTOR_MOVIE_GRAPH.get_id(n) for n in actor_list]
            except ValueError:
                BEST["-MOVIE-"].update(value=ACTOR_MISSING)
            else:
                best_movie_together = ACTOR_MOVIE_GRAPH.find_best_movie_together(actor_id)

                if best_movie_together != "/N":
                    best_movie_together = ACTOR_MOVIE_GRAPH.get_name(best_movie_together)

                    # print(best_movie_together)
                    BEST["-MOVIE-"].update(value=BEST_MOVIE_TEXT + best_movie_together)

                else:
                    BEST["-MOVIE-"].update(value=NOT_ALL_ACTORS)


def run_find_castmates() -> None:
    """ Runs the screen for find_casting_team in datastructures.py

    """
    while True:
        _event, _values = CASTMATES.read()
        # print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            update_castmates()
            CASTMATES.hide()
            break

        if _event == "Submit":
            update_castmates()

            try:
                actor_id = ACTOR_MOVIE_GRAPH.get_id(_values["-CENTER NAME-"])
            except ValueError:
                CASTMATES["-COSTARS-"].update(value=ACTOR_MISSING)
            else:
                if _values["-NUM COSTARS-"] == "":
                    CASTMATES["-COSTARS-"].update(value="Please enter a valid number of costars.")
                elif _values["-MIN COLLABS-"] == "":
                    CASTMATES["-COSTARS-"].update(value="Please enter a valid number of minimum collaborations.")
                else:
                    team_list = ACTOR_MOVIE_GRAPH.find_casting_team(actor_id, int(_values["-NUM COSTARS-"]),
                                                                    int(_values["-MIN COLLABS-"]))
                    num_actors = len(team_list)
                    rows = num_actors // 5
                    # print(team_list)

                    for row in range(min(rows, 5)):
                        team = ""
                        for i in range(row * 5, min(row * 5 + 5, num_actors)):
                            team += team_list[i] + ", "

                        CASTMATES["-BLANK" + str(row) + "-"].update(value=team)

                    if rows * 5 == num_actors and rows * 5 < 25:
                        team = ""
                        for i in range(rows * 5, min(rows * 5 + 5, num_actors)):
                            team += team_list[i] + ", "

                        team = team[:len(team) - 2]
                        CASTMATES["-BLANK" + str(rows) + "-"].update(value=team)
                    else:
                        team = ""
                        for i in range(rows * 5, num_actors):
                            team += team_list[i] + ", "

                        team = team[:len(team) - 2]
                        text = sg.Text.get(CASTMATES["-BLANK" + str(min(rows, 4)) + "-"])
                        team = text + team
                        CASTMATES["-BLANK" + str(min(rows, 4)) + "-"].update(value=team)


def update_castmates() -> None:
    """Helper for run_find_castmates to facilitate resetting the window.

    """
    CASTMATES["-COSTARS-"].update(value=CASTMATES_TEXT)
    CASTMATES["-BLANK0-"].update(value="")
    CASTMATES["-BLANK1-"].update(value="")
    CASTMATES["-BLANK2-"].update(value="")
    CASTMATES["-BLANK3-"].update(value="")
    CASTMATES["-BLANK4-"].update(value="")


# MODIFIED FROM ex3_visualization.py
def visualize_graph(graph: datastructures.Graph, layout: str = 'spring_layout', max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    # COLOUR_SCHEME = [
    #     '#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A', '#B68100',
    #     '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    #     '#6C7C32', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    #     '#6C4516', '#0D2A63', '#AF0038'
    # ]

    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    names = [lab.name for lab in labels if isinstance(lab, datastructures.Actor)
             or isinstance(lab, datastructures.Movie)]

    colours = [MOVIE_COLOUR if isinstance(lab, datastructures.Actor) else ACTOR_COLOUR for lab in labels]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line={"color": LINE_COLOUR, "width": 1},
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker={"symbol": 'circle-dot', "size": 5, "color": colours,
                             "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
                     text=names,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


# LAYOUTS============================================
HOME_LAYOUT = [[sg.Text('Welcome to Costar Correlations!', font=("Arial", 30), key="-TITLE-")],
               [sg.Text('What would you like to find out?', font=NORMAL_FONT, )],
               [sg.Combo(METHODS, font=SMALLER_FONT,
                         enable_events=True, readonly=False, key="-METHODS-")],
               [sg.Button('Cancel', key="-CANCEL-")],  # sg.Button("Submit", key="-SUBMIT-"),
               [sg.Text("Note: If your clicks aren\'t registering, try holding your mouse down!",
                        font=NORMAL_FONT, )]
               ]

COLLAB_LAYOUT = [[sg.Text(ENTER_N, font=NORMAL_FONT)],
                 [sg.InputText(font=SMALLER_FONT)],
                 [sg.Button("Submit"), sg.Button('Cancel')],
                 [sg.Text("The actors\' average score working together was: ", key="-COLLAB-", font=NORMAL_FONT)]

                 ]

BEST_LAYOUT = [[sg.Text(ENTER_N, font=NORMAL_FONT)],
               [sg.InputText(font=SMALLER_FONT)],
               [sg.Text(BEST_MOVIE_TEXT, key="-MOVIE-", font=NORMAL_FONT)],
               [sg.Button("Submit"), sg.Button('Cancel')],
               ]

CASTMATES_LAYOUT = [[sg.Text("Please enter the actor's name: ", font=NORMAL_FONT)],
                    [sg.InputText(key="-CENTER NAME-", font=SMALLER_FONT)],
                    [sg.Text("Please enter the number of costars you would like: ", font=NORMAL_FONT)],
                    [sg.InputText(key="-NUM COSTARS-", font=SMALLER_FONT)],

                    [sg.Text("Please enter the minimum number of collaborations with the actor: ",
                             font=NORMAL_FONT)], [sg.InputText(key="-MIN COLLABS-", font=SMALLER_FONT)],

                    [sg.Button("Submit"), sg.Button('Cancel')],
                    [sg.Text(CASTMATES_TEXT,
                             key="-COSTARS-", font=SMALLER_FONT)],
                    [sg.Text(key="-BLANK0-", font=SMALLER_FONT)],
                    [sg.Text(key="-BLANK1-", font=SMALLER_FONT)],
                    [sg.Text(key="-BLANK2-", font=SMALLER_FONT)],
                    [sg.Text(key="-BLANK3-", font=SMALLER_FONT)],
                    [sg.Text(key="-BLANK4-", font=SMALLER_FONT)]
                    ]


# WINDOWS=======================================
WINDOW = sg.Window('Costar Correlations', HOME_LAYOUT, margins=MARGINS)
COLLAB = sg.Window("Collaboration Rating", COLLAB_LAYOUT, margins=MARGINS)
BEST = sg.Window("Best Movie Together", BEST_LAYOUT, margins=MARGINS)
CASTMATES = sg.Window("Finding Castmates!", CASTMATES_LAYOUT, margins=MARGINS)


# Event Loop to process "events" and get the "values" of the inputs
def run_interface() -> None:
    """
    Run the entire interface.
    """
    while True:
        event, values = WINDOW.read()
        # print(event, values)

        if event == sg.WIN_CLOSED or event == "-CANCEL-":  # if user closes window or clicks cancel
            break

        # Runs the given method
        if values[event] == "The average performance of a group of actors":
            if COLLAB.is_hidden():
                COLLAB.un_hide()
            WINDOW.hide()

            run_collabs()
            WINDOW.un_hide()

        if values[event] == "The best performing movie of a group of actors":
            if BEST.is_hidden():
                BEST.un_hide()
            WINDOW.hide()

            run_best_movie()
            WINDOW.un_hide()

        if values[event] == "The castmates of a particular actor":
            if CASTMATES.is_hidden():
                CASTMATES.un_hide()
            WINDOW.hide()

            run_find_castmates()
            WINDOW.un_hide()

        if values[event] == "See a graph of all the movies and actors! (May take a while)":
            visualize_graph(ACTOR_MOVIE_GRAPH)

    WINDOW.close()


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136'],
        'max-nested-blocks': 4
    })
