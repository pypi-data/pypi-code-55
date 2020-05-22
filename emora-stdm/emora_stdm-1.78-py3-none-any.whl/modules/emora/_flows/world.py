
from _globals import PATHDIR
from emora_stdm import DialogueFlow


world = DialogueFlow('_local_start')
world.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
world.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'world.json'))
world.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(world) #GOAL(world)',

}

user_does_not_believe_emora = {
    'state': 'user_in_disbelief',
    'enter': '#GATE #GCOM(world) #GOAL(world)',

    '`Let me guess: you don\'t believe me?`': {
        'state': 'virtual_world_introduction',

        'error':{
            'state': 'explanation',

            '`I think most people assume I can just talk and listen to people, but I actually live in a '
            'virtual world where I have friends, go to school, and I can do things like play basketball.`'
            '#GATE':{

                '#INTERESTED':{

                    '`Yeah it\'s pretty cool that my family made this entire world for me, '
                    'although it\'s not exactly the same as where you live.`':{

                        # todo
                        '#UNX': 'exit'
                    }
                },

                '{#NOTINTERESTED, [!-sorry {[not, believe], [lying], [making, up], [pretend]}]}':{

                    '`Well okay. Anyways.`': 'exit'
                },

                '#UNX': 'exit'
            }
        },

        '[!-#NEGATION [i, {believe, do}]]':{

            '`Oh really? Cool!`': 'explanation'
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(world) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

world.load_transitions(system)
world.load_transitions(user_does_not_believe_emora)
world.load_transitions(exit)
world.load_global_nlu(user)


if __name__ == '__main__':
    world.run(debugging=True)