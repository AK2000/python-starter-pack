# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 22:38:37 2018

@author: alokk
"""
# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]
nodeCircle = [3]
nodeCircle2 = [6,10]
turnCounter = 0
index = 0

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

def get_third_stance(stance1, stance2):
    if (stance1 == "Rock" and stance2 == "Paper") or (stance2 == "Rock" and stance1 == "Paper"):
        return "Scissors"
    if (stance1 == "Rock" and stance2 == "Scissors") or (stance2 == "Rock" and stance1 == "Scissors"):
        return "Paper"
    if (stance1 == "Scissors" and stance2 == "Paper") or (stance2 == "Scissors" and stance1 == "Paper"):
        return "Rock"

def get_back(node1, node2, numTurns, me):
    paths = game.shortest_paths(node1, node2)
    minNumTurns = me.movement_counter-me.speed + (len(paths[0]) * (7-me.speed))
    return numTurns > minNumTurns
    
# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game
    me = game.get_self()
    turnCounter = turnCounter + 1  
    
    if me.location == me.destination: # check if we have moved this turn
        if game.has_monster(me.location) and  not game.get_monster(me.location).dead:
            destination_node = me.location
        else:
            if (not get_back(me.location, 0, game.get_monster(0).respawn_counter-1, me)):
                paths = game.shortest_paths(me.location, 0)
                destination_node = paths[0][0]
            else:
                if(turnCounter < 115):
                    paths = game.shortest_paths(me.location, nodeCircle[index%len(nodeCircle)])
                else:
                    paths = game.shortest_paths(me.location, nodeCircle2[index%len(nodeCircle2)])
                destination_node = paths[0][0]
                index+=1
    else:
        destination_node = me.destination
    
    #chosen_stance = "Paper"
    if game.has_monster(me.location) and not game.get_monster(me.location).dead:
        # if there's a monster at my location, choose the stance that damages that monster
        chosen_stance = get_winning_stance(game.get_monster(me.location).stance)
    else:
        # otherwise, pick a random stance
        chosen_stance = stances[random.randint(0, 2)]
        
    # if(game.get_opponent().location == me.location):
    #     chosen_stance = get_winning_stance(game.get_opponent().stance)
    

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)

    
