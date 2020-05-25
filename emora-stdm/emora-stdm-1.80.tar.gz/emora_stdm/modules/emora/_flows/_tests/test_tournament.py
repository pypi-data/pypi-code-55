###################################
# Import your DialogueFlow object
# (where "tournament" currently is)
###################################
import sys
sys.path.append(".")

from tournament import tournament as component
from copy import copy

###################################
# Add an ending loop if
# you do not already have one.
# Put your end state instead of "exit"
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
        ["thats cool", "sounds fun", "we watch movies"],
        ["sorry to hear that", "sounds fun", "we watch movies"],
        ["that sucks", "sounds fun", "we watch movies"],
        ["are you sad about losing", "i see", "sounds fun", "we watch movies"],
        ["do you get sad when you lose", "oh i would be so sad", "sounds fun", "we watch movies"],
        ["is it upsetting when you lose", "that makes sense", "sounds fun", "we watch movies"],
        ["was it disappointing to lose", "that is a good outlook", "sounds fun", "we watch movies"],
        ["how pissed off were you to lose", "really", "ok", "just relax and talk"],
        ["that sucks", "how long have you been playing basketball for", "ok", "sounds fun", "we watch movies"],
        ["that sucks", "do you play often", "ok", "sounds fun", "we watch movies"],
        ["that sucks", "are you any good at basketball", "ok", "sounds fun", "we watch movies"],
        ["that sucks", "sounds fun", "you are pretty good at basketball then", "ok", "we watch movies"],
        ["that sucks", "sounds fun", "ok", "do you like playing basketball", "ok", "we watch movies"],
        ["how far did you make it", "ok"],
        ["are you sad", "what position do you play", "got it", "sounds fun"],
        ["were you guys close to winning", "ok"],
        ["how close to the end did you make it", "ok"],
        ["where were you knocked out at", "ok"],
        ["did you think you were going to win", "ok"],
        ["do you like basketball", "ok"],
        ["did you guys lose in the finals or earlier", "ok"],
        ["what place did you make it to", "ok"],
        ["yeah taking a break is important", "that sounds fun how long have you been playing basketball","ok got it","i dont have any friends"],
        ["thats cool", "sounds fun", "i have never had a friend"],
        ["thats cool", "sounds fun", "i have no friends"],
        ["thats cool", "sounds fun", "no one wants to be friends with me"],
        ["thats cool", "sounds fun", "no one will be my friend"]
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
