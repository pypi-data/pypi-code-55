
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

    '`Let me guess: you don\'t believe me?`'
    '#GSRET(explanation)': {
        'state': 'virtual_world_introduction',

        'error':{
            'state': 'explanation',

            '`I think most people assume I can just talk and listen to people, but I actually live in a '
            'virtual world where I have friends and I can do things like play basketball.`'
            '#GATE #GSRET(exit)':{

                '#INTERESTED':{

                    '`Yeah it\'s pretty cool that my family made this entire world for me, '
                    'although I guess it\'s not exactly the same as where you live.`'
                    '#GSRET(exit)':{

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

world_contains = {
    'state': 'world_contains',

    '`It is very similar to your Earth, with plants, animals, land and water. But my sky doesn\'t go on forever '
    'like your outer space does. There is only my planet, a moon, and a sun.`': {
        'state': 'share_world_contains',

        '#UNX': {'#GRET': 'exit', 'state': 'share_world_contains_unx'}
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

transitions = [system,user_does_not_believe_emora,world_contains]
for trans in transitions:
    world.load_transitions(trans)

# world.load_transitions(world_has_x, DialogueFlow.Speaker.USER)
world.load_transitions(exit)
world.load_global_nlu(user)


if __name__ == '__main__':
    world.run(debugging=True)