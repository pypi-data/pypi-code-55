###################################
# Import your DialogueFlow object
###################################
import sys
sys.path.append(".")

from baby import baby as component
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
        ["ok","ok","ok", "ok"],
        ["ok", "ok", "ok", "yes", "two and a half"],
        ["ok", "ok", "ok", "no"],
        ["what do you mean you have a family", "sure", "what does your family focus on about you", "thats tough", "sure"],
        ["you arent real", "sure", "ok", "can you have a baby", "do you want a baby", "i see"],
        ["do you like children", "ok", "so who is your family", "who are your parents", "ok"],
        ["i just had a baby too", "thanks its been alright", "i will try", "ok"],
        ["my wife just had a baby too", "ok", "ok", "ok"],
        ["my sister has a newborn too", "yeah", "yes", "do you have kids", "gotcha", "he is five"],
        ["i am trying to have a baby now too", "do you want kids", "can you have kids", "who is your family", "sure"]
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
