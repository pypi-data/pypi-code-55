###################################
# Import your DialogueFlow object
###################################
import sys
sys.path.append(".")

from house import house as component
from copy import copy

###################################
# Add an ending loop if
# you do not already have one
###################################
component.add_state('unit_test_end', 'unit_test_end')
component.add_system_transition('exit','unit_test_end','" END"')
component.add_system_transition('unit_test_end','unit_test_end','" END"')

if __name__ == '__main__':

    #######################################################################################################
    # DO NOT REMOVE - this will precompile your Natex expressions, identifying any cases where your Natex
    # is not compilable and will cause the state to throw an error.
    #######################################################################################################
    component.precache_transitions()

    #######################################################################################################
    # Add the sequence of utterances you want to test as your conversation with your component
    #######################################################################################################
    sequences = [
        ["where did you live before","where is your new house","ok sure","can you get in water","i see","no"],
        ["how do you own a house", "ok sure", "do you swim", "i see", "yes"],
        ["where do you live now", "ok sure", "you are just a robot", "i see", "no", "where was your old place", "sure"],
        ["you dont own a house", "i see", "i dont know", "did you like your old place", "sorry about that"],
        ["you arent real"],
        ["how do you live in a house"],
        ["how do you go swimming"],
        ["can you get in water"],
        ["what do you mean you can swim"],
        ["you dont have a body"],
        ["you cant swim"],
        ["cool", "cool", "its alright", "big kitchen"],
        ["cool", "cool", "its alright", "a pool"],
        ["cool", "cool", "its alright", "huge windows and lots of light"],
        ["cool", "cool", "its alright", "a beautiful lawn"],
        ["cool", "cool", "its alright", "an outdoor living space with a patio and stuff"],
        ["cool", "cool", "its alright", "a deck would be great"],
        ["cool", "cool", "its alright", "a lot of bedrooms"],
        ["cool", "cool", "its alright", "i just want a big house"],
        ["cool", "cool", "its alright", "i really like an open floor plan"],
        ["cool", "cool", "its alright", "i want to be close to my parents"],
        ["cool", "cool", "its alright", "i would like to live in a neighborhood that throws parties and stuff"],
        ["cool", "cool", "its alright", "did you like your old place", "cool"],
        ["cool", "cool", "yes", "did you like your old place", "ok", "it has a big yard"],
        ["cool", "cool", "sometimes", "how do you own a home", "ok", "it smells weird"],
        ["cool", "cool", "its fine", "where is your new home", "ok", "the kitchen would be upgraded"],
        ["cool", "cool", "no", "where is your new home", "ok", "yeah"]
    ]


    #######################################################################################################
    # Uses your utterances to conduct a conversation with your component.
    #######################################################################################################
    debug = False
    for sequence in sequences:
        print()
        print("&"*20)
        print()
        component.reset()

        #######################################################################################################
        # If you use variables from Cobot in your logic, modify cobot_vars with your desired test cases.
        #######################################################################################################
        # cobot_vars = {'request_type': 'LaunchRequest',
        #               'global_user_table_name': 'GlobalUserTableBeta'}
        # component._vars.update({key: val for key, val in cobot_vars.items() if val is not None})

        turn = 0
        response = component.system_turn(debugging=debug)
        print("E: %s (%s)" % (response, component.state()))
        for utter in sequence:
            component.user_turn(utter, debugging=debug)
            print("U: %s (%s)"%(utter,component.state()))
            response = component.system_turn(debugging=debug)
            print("E: %s (%s)"%(response,component.state()))
            turn += 1
