from emora_stdm import DialogueFlow

df = DialogueFlow('root')

transitions = {
    'state': 'root',

    '`So, I remember you said you were a student. I\'m actually a student too! `'
    '#GATE #IF($is_student=True)' : 'ask_like_school',

    '#GATE() #IF($is_student=None) #SET($topic=school)'
    '"So, I was thinking you probably don\'t know this about me. I\'m actually a student right now, but I think my school is pretty different than what most people are used to. '
    'Are you a student too?"':{
        '#SET($is_student=True)'
        '#AGREE':{
            'state': 'ask_like_school',
            '"Honestly, I think taking classes is pretty boring, even though I know they are important. I would much rather spend time talking to my friends and being outside. '
            'What about you? Do you like school?"':{
                '#SET($likes_school=True)'
                '#AGREE':{
                    '"I think that\'s great. I mean, who doesn\'t like learning new things? "': {
                        'error': 'end'
                    }
                },
                '#SET($likes_school=False)'
                '#DISAGREE':{
                    '"I kind of get that. But to be fair, learning new things can sometimes be a lot of fun."':{
                        'error': 'end'
                    }
                },

                '[!-{like,dislike,hate,love,enjoy} [{i,im} {dont,not} {a student,in school,[#LEM(take) class]}]]'
                '#SET($is_student=False)': {
                    'score': 1.1,
                    'state': 'not_student'
                },

                '#UNX':{
                    'score': 0.8,
                    '"I am always glad to hear more about what you think. "': 'end'
                }
            }
        },
        '#SET($is_student=False)'
        '#DISAGREE':{
            'state': 'not_student',

            '"Oh, really? I cannot even imagine not waking up everyday and going to class. This one teacher of mine is hilarious. He never talks in class about the material, '
            'he just rants the entire time about the economy and social issues."':{
                '#UNX':{
                    '"So, what do you remember most about school?"':{
                        'error':{
                            '"Sounds about right. "': 'end'
                        },
                        '#IDK': {
                            '"Has it been a while then?"':{
                                'error': {
                                    '"I see. "': 'end'
                                }
                            }
                        }
                    }
                }
            }
        },
        '#UNX':{
            'score': 0.8,
            '""': 'ask_like_school'
        }
    }
}


df.load_transitions(transitions, speaker=DialogueFlow.Speaker.SYSTEM)

df.update_state_settings('root', system_multi_hop=True)
df.update_state_settings('end', system_multi_hop=True)
df.update_state_settings('ask_like_school', system_multi_hop=True)

if __name__ == '__main__':
    df.run(debugging=True)
