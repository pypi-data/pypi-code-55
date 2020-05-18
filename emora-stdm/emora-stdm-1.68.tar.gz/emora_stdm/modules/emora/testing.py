###################################
# Import your DialogueFlow object
###################################
from competition import competition as component
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
    opening = []
    sequences = [
        ["sure","sure"],
        ["are you a competitive person","i see","sure"],
        ["do you want to win the competition", "ok", "sure"],
        ["what is the goal of the competition", "makes sense", "sure"],
        ["what are you competing for", "ok", "sure"],
        ["what happens if you win", "ok", "sure"],
        ["what do you get if you win", "ok", "sure"],
        ["what is the prize", "ok", "sure"],
        ["is there a reward for winning", "ok", "sure"],
        ["who are you competing against", "ok", "sure"],
        ["who else is in the competition", "ok", "sure"],
        ["are you recording your conversations", "ok", "sure"],
        ["are you a part of the fbi", "ok", "sure"],
        ["what place are you in", "ok", "who judges you"],
        ["how are you doing in the competition", "who judges you", "sure"],
        ["ok","are you going to win","i see"],
        ["yeah","what is the competition for","sure"]
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
        # component.controller()._vars.update({key: val for key, val in cobot_vars.items() if val is not None})

        turn = 0
        new_seq = copy(opening)
        new_seq.extend(sequence)

        response = component.system_turn(debugging=debug)
        print("E: %s (%s)" % (response, component.state()))
        for utter in new_seq:
            component.user_turn(utter, debugging=debug)
            print("U: %s (%s)"%(utter,component.state()))
            response = component.system_turn(debugging=debug)
            print("E: %s (%s)" % (response, component.state()))
            turn += 1
