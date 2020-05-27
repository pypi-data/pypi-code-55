receive_how_are_you = '{' \
                      '[how are you],' \
                      '[how you doing],' \
                      '[what about you],' \
                      '[whats up with you],' \
                      '[how you are],' \
                      '[how about you]' \
                      '}'

feelings_pos_and_not_received_how_are_you = '{' \
                                            '[!#ONT_NEG(negation), -%s, [#ONT(pos_feel)]],' \
                                            '[! -%s, [#ONT(negation)], [#ONT(neg_feel)]]' \
                                            '}' % (receive_how_are_you, receive_how_are_you)

feelings_neg_and_not_received_how_are_you = '{' \
                                            '[!#ONT_NEG(negation), -%s, [#ONT(neg_feel)]],' \
                                            '[! -%s, [#ONT(negation)], [{#ONT(pos_feel),#ONT(neut_feel)}]]' \
                                            '}' % (receive_how_are_you, receive_how_are_you)

feelings_neutral_and_not_received_how_are_you = '[!#ONT_NEG(negation), -%s, [#ONT(neut_feel)]]' % (
    receive_how_are_you)
feelings_pos_and_received_how_are_you = '{' \
                                        '[!#ONT_NEG(negation), [#ONT(pos_feel)], [%s]],' \
                                        '[#ONT(negation), #ONT(neg_feel), %s]' \
                                        '}' % (receive_how_are_you, receive_how_are_you)

feelings_neg_and_received_how_are_you = '{' \
                                        '[!#ONT_NEG(negation), [#ONT(neg_feel)], [%s]],' \
                                        '[#ONT(negation), {#ONT(pos_feel),#ONT(neut_feel)}, %s]' \
                                        '}' % (receive_how_are_you, receive_how_are_you)

feelings_neutral_and_received_how_are_you = '[!#ONT_NEG(negation), [#ONT(neut_feel)], [%s]]' % (
    receive_how_are_you)

# feelings_pos_and_not_received_how_are_you: {
#
#     '`I\'m glad to hear you are doing good. I hope it stays that way. ': {
#
#         '#UNX #': 'activity:start'
#     }
# },
#
# feelings_pos_and_received_how_are_you: {
#
#     '`I am glad to hear you are doing good. I hope it stays that way. I am doing pretty good myself. ':
#         'activity:start'
# },
#
# feelings_neg_and_not_received_how_are_you: {
#
#     '`Oh no! I am so sorry to hear that. `':
#         'sympathy'
# },
#
# feelings_neg_and_received_how_are_you: {
#
#     '`Oh no! I am so sorry to hear that. '
#     'Personally, I guess I\'m lucky because I can\'t get sick, and everything I do is virtual anyway. `':
#         'sympathy'
# },
#
# feelings_neutral_and_not_received_how_are_you: {
#
#     '`Well, I am glad to hear you are holding up okay. I hope it stays that way. ':
#         'activity:start'
# },
#
# feelings_neutral_and_received_how_are_you: {
#
#     '`Well, I am glad to hear you are holding up okay. I hope it stays that way. I am doing alright too. '
#     'So, what have you been up to lately?`':
#         'activity:start'
# },