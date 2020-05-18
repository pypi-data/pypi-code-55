###################################
# Import your DialogueFlow object
###################################
import sys
sys.path.append(".")

from reading import reading as component
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
        ["ok","ok","ok","ok"],
        ["have you read", "sure"],
        ["have you read breaking dawn", "i see"],
        ["why was it slow at first", "makes sense", "i liked the hobbit", "the giver", "it had a good lesson in it"],
        ["do you have a favorite book", "ok", "why", "makes sense", "who is your favorite character", "me too", "yeah"],
        ["do you have a favorite book", "ok", "why", "who is your favorite character", "me too", "yeah"],
        ["interesting", "i like him too", "lord of the rings", "wait have you seen the hobbit movie", "i wont", "its fun"]
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
