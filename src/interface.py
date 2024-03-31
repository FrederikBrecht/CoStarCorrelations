""""
This python file will handle all the functions for an interactive interface.
"""

import pygame
import PySimpleGUI as sg
import datastructures
from data import db_filter
import networkx as nx
from plotly.graph_objs import Scatter, Figure


# FINAL VARIABLES
methods = ["The average performance of a group of actors",
           "The best performing movie of a group of actors",
           "All the castmates of a particular actor"]

margins = (500, 350)
normal_font = ("Arial", 20)


# FUNCTIONS====================================


def run_collabs() -> None:
    """ Runs the screen for evaluate_collaborative_performance from datastructures.py

    """

    while True:
        _event, _values = collab.read()
        print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            collab["-COLLAB-"].update(value="The actors\' average score working together was: ")
            collab.hide()
            break

        if _event == "Submit":
            actor_list = _values[0].split(", ")
            actor_id = []

            # TODO: CANT USE THIS CUZ CANT GET ACTOR IDS FROM NAME
            # score = temp.evaluate_collaborative_performance(actor_id)
            score = 1

            if score != -1:
                collab["-COLLAB-"].update(value="The actors\' average score working together was: " + str(score))

            else:
                collab["-COLLAB-"].update(value="Sorry, there were no movies containing all actors." +
                                                " Try checking your spelling or formatting.")


def run_best_movie() -> None:
    """ Runs the screen for find_best_movie_together in datastructures.py

    """
    while True:
        _event, _values = best.read()
        print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            best["-MOVIE-"].update(value="The actors\' best movie together was: ")
            best.hide()
            break

        if _event == "Submit":
            # actor_list = _values[0].split(", ")
            # actor_id = []

            # best_movie_together = temp.find_best_movie_together(actor_id)
            best_movie_together = "Big Hero 6"

            if best_movie_together != "/N":
                best["-MOVIE-"].update(value="The actors\' best movie together was: " + best_movie_together)

            else:
                best["-MOVIE-"].update(value="Sorry, there were no movies containing all actors." +
                                             " Try checking your spelling or formatting.")


def run_find_castmates() -> None:
    """ Runs the screen for find_casting_team in datastructures.py

    """
    while True:
        _event, _values = castmates.read()
        print(_event, _values)

        if _event == sg.WIN_CLOSED or _event == "Cancel":
            castmates["-COSTARS-"].update(value="The actors casting team created is: ")
            castmates.hide()
            break

        if _event == "Submit":

            # team_list = temp.find_casting_team(values["-CENTER NAME-"], values["-NUM COSTARS-"],
            # values["-MIN COLLABS-"])
            team_list = ["Ayumu Murase", "Kaito Ishikawa", "Shu Uchida"]
            team = ""
            for i in team_list:
                team += i + ", "
            team = team[:len(team)-2]

            castmates["-COSTARS-"].update(value="The casting team created is: " + team, )


# LAYOUTS============================================
home_layout = [[sg.Text('Welcome to Costar Correlations!', font=("Arial", 30), key="-TITLE-")],
               [sg.Text('What would you like to find out?', font=normal_font, )],
               [sg.Combo(methods, font=("Arial", 15),
                         enable_events=True, readonly=False, key="-METHODS-")],
               [sg.Button('Cancel', key="-CANCEL-")],  # sg.Button("Submit", key="-SUBMIT-"),
               [sg.Text("Note: If your clicks aren\'t registering, try holding your mouse down!", font=normal_font, )]
               ]

collab_layout = [[sg.Text("Please enter the actors\' names in First/Last order, separated by commas and spaces" +
                          " except for at the end",
                          font=normal_font)],
                 [sg.InputText()],
                 [sg.Button("Submit"), sg.Button('Cancel')],
                 [sg.Text("The actors\' average score working together was: ", key="-COLLAB-", font=normal_font)]

                 ]

best_layout = [[sg.Text("Please enter the actors\' names in First/Last order, separated by commas and spaces" +
                        " except for at the end",
                        font=normal_font)],
               [sg.InputText()],
               [sg.Button("Submit"), sg.Button('Cancel')],
               [sg.Text("The actors\' best movie together was: ", key="-MOVIE-", font=normal_font)]
               ]

castmates_layout = [[sg.Text("Please enter the actors's name: ", font=normal_font)],
                    [sg.InputText(key="-CENTER NAME-", font=normal_font)],

                    [sg.Text("Please enter the number of costars you would like: ", font=normal_font)],
                    [sg.InputText(key="-NUM COSTARS-", font=normal_font)],

                    [sg.Text("Please enter the minimum number of collaborations with the actor: ",
                             font=normal_font)], [sg.InputText(key="-MIN COLLABS-", font=normal_font)],


                    [sg.Button("Submit"), sg.Button('Cancel')],

                    [sg.Text("The casting team created is: ", key="-COSTARS-", auto_size_text=True,
                             justification="left")]
                    ]


# WINDOWS=======================================
window = sg.Window('Costar Correlations', home_layout, margins=margins)
collab = sg.Window("Collaboration Rating", collab_layout, margins=margins)
best = sg.Window("Best Movie Together", best_layout, margins=margins)
castmates = sg.Window("Finding Castmates!", castmates_layout, margins=margins)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == "-CANCEL-":  # if user closes window or clicks cancel
        break

    # Runs the given method
    if values[event] == "The average performance of a group of actors":
        if collab.is_hidden():
            collab.un_hide()
        window.hide()

        run_collabs()
        window.un_hide()

    if values[event] == "The best performing movie of a group of actors":
        if best.is_hidden():
            best.un_hide()
        window.hide()

        run_best_movie()
        window.un_hide()

    if values[event] == "All the castmates of a particular actor":
        if castmates.is_hidden():
            castmates.un_hide()
        window.hide()

        run_find_castmates()
        window.un_hide()


window.close()

# https://www.youtube.com/watch?v=yOZ3po-BV1Q
