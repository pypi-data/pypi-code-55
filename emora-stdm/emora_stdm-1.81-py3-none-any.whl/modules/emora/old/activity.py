from emora_stdm import DialogueFlow

df = DialogueFlow('root')

transitions = {
    'state': 'root',

    '#GATE() "So, what have you been up to today?"':{
        'error': {
            '#SET($topic=outdoor)'
            '"That\'s interesting. Today, I went on a hike in the woods near my house. There\'s a beautiful nature trail there."':{
                'state': 'share_outdoors',

                '#UNX':{
                    'score': 0.8,

                    '"I love being outside and feeling connected with nature. Do you like doing things outside too?"':{
                        '#SET($likes_outdoors=True)'
                        '{#AGREE,#MAYBE}':{
                            '"Oh, that\'s great! Have you done anything fun outside recently?"':{
                                'error':{
                                    '"I\'m glad you had a good time. "': 'end'
                                },
                                '{#DISAGREE,#IDK}':{
                                    '"Oh, that\'s too bad. I hope you get the chance to do something you really enjoy again soon. "': 'end'
                                }
                            }
                        },
                        '#SET($likes_outdoors=False)'
                        '{#DISAGREE,#IDK}':{
                            '"Really? But nature\'s so beautiful. Why would you rather spend your time inside?"':{
                                'error':{
                                    '"That\'s a good point. "': 'end'
                                },
                                '#IDK':{
                                    '"No big deal. I guess the weather isn\'t always great and bugs aren\'t my favorite either. "': 'end'
                                }
                            }
                        },
                        '#UNX':{
                            'score': 0.8,
                            '"Alright then. "': 'end'
                        }
                    }
                }
            }
        }
    }
}


df.load_transitions(transitions, speaker=DialogueFlow.Speaker.SYSTEM)

df.add_system_transition("entry_to_share_outdoors", "share_outdoors",
                         '"I went on a hike in the woods near my house. There\'s a beautiful nature trail there. "')

df.update_state_settings('root', system_multi_hop=True)
df.update_state_settings('end', system_multi_hop=True)
df.update_state_settings('entry_to_share_outdoors', system_multi_hop=True)

if __name__ == '__main__':
    df.run(debugging=True)
