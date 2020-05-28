from emora_stdm import DialogueFlow
from _globals import PATHDIR

df = DialogueFlow('start')
df.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))

"""
is_employed
likes_job
is_looking_job
job
----
split at "how did you make your decision" 
-> relevant to people not employed but looking for job
-> relevant to people who are employed
"""
transitions = {
    'state': 'start',
    'enter': '#GATE(worklifev:None) #SET($worklifev=True) #IF($life_in=True)',

    '`So, you mentioned you had a job. Are you happy where you work now?`'
    '#GATE #IF($is_employed=True)': 'asked_happy_work',

    '"You know, this has been on my mind a lot recently. I hope that when I get a job someday, I am doing something that I really enjoy. Do you currently work?"'
    '#GATE() #IF($is_employed=None)':{
        '#SET($is_employed=True)'
        '#AGREE':{
            '"Oh, cool! Are you happy where you work now?"':{
                'state': 'asked_happy_work',

                '#SET($likes_job=True)'
                '#AGREE':{
                    '"That\'s really great to hear! What do you do for work?"':{
                        'error':{
                            '"Interesting. Well, I am glad you found something that is a good fit for you. '
                            'I really don\'t know what I want to do. How did you make your decision?"': {
                                'error': {
                                    '"I will have to keep that in mind for sure. "': 'end'
                                },
                                '#IDK':{
                                    '"I guess things just have a way of working themselves out sometimes. "': 'end'
                                }
                            }
                        }
                    }
                },
                '#SET($likes_job=False)'
                '#DISAGREE':{
                    '"Oh no! I am sorry to hear that. What do you do for work?"': {
                        'error':{
                            '"Gotcha. I hope it gets better for you soon. Are you looking for a new job?"': {
                                '#SET($is_looking_job=True)'
                                '#AGREE':{
                                    '"You\'ll find something better suited for you, I am sure of it. "': 'end'
                                },
                                '#SET($is_looking_job=False)'
                                '[#DISAGREE,#MAYBE]':{
                                    '"I bet you\'re in a difficult position, leaving a job is never easy. I am sure it will '
                                    'all work out though, no matter what you end up doing. "': 'end'
                                },
                                '#IDK':{
                                    '"It can be a tough choice for sure, but you should just do whatever is best and try not '
                                    'to worry about it too much."': 'end'
                                },
                                'error':{
                                    '"I am sure it will all work out though, no matter what you end up doing. "': 'end'
                                }
                            }
                        }
                    }
                },

                '[i,#NEGATION,{job,work,#LEM(employ)}]'
                '#SET($is_employed=False)': {
                    'score': 1.1,
                    'state': 'is_jobless'
                },

                '#UNX':{
                    'score': 0.8,
                    '"Okay, I see what you mean. "': 'end'
                }
            }
        },
        '#SET($is_employed=False)'
        '{#DISAGREE,[unemployed],[#NEGATION,{work,job,employed}]}':{
            'state': 'is_jobless',

            '"Oh, you aren\'t currently working? Do you want to get a job?"': {
                '#SET($is_looking_job=True)'
                '#AGREE':{
                    '"Got it. What kind of job are you looking for?"':{
                        'error':{
                            '"Cool! Well, I hope you are able to find one soon. "': 'end'
                        }
                    }
                },
                '#SET($is_looking_job=False)'
                '#DISAGREE':{
                    '"I see, that\'s perfectly understandable. I don\'t really think I want a job right now either. '
                    'Having a job is hard."': 'end'
                },
                '#SET($is_looking_job=False)'
                '{#MAYBE,#IDK}':{
                    '"It could be a tough choice, for sure, depending on what\'s going on. '
                    'I don\'t really think I want a job right now either."': 'end'
                },
                'error':{
                    '"Alright. Well, I don\'t really want a job right now, to be honest. I am still trying to figure '
                    'out what I want to do."': 'end'
                }
            }
        },
        '#UNX':{
            'score': 0.8,
            '"I enjoy hearing about all of the jobs that are out there. "': 'end'
        }
    }
}

df.load_transitions(transitions)

df.add_system_transition("entry_to_happy_work", "asked_happy_work", '"Are you happy where you work now? "')

df.update_state_settings('start', system_multi_hop=True)
df.update_state_settings('end', system_multi_hop=True)
df.add_system_transition('end', ('SYSTEM', 'intermediate_topic_switch'), '"Anyway, "', score=0.0)
df.update_state_settings('entry_to_happy_work', system_multi_hop=True)

if __name__ == '__main__':
    df.precache_transitions()
    df.run(debugging=False)