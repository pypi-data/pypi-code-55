
from _globals import PATHDIR
from emora_stdm import DialogueFlow


component = DialogueFlow('_local_start')
component.add_system_transition('exit', 'SYSTEM:root', '#GCOM(component)')
component.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
component.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'component.json'))
component.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM #GOAL(component)'
}

exit = {
    'state': 'exit',

    '#GCOM(component)': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

flow2 = {
    'state': 'flow2',
    'enter': '#GATE #GCOM #GOAL(component)'
}

rexit = {
    'state': 'rexit',

    '#GCOM(component)': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

component.load_transitions(system)
component.load_transitions(flow2)
component.load_transitions(exit)
component.load_transitions(rexit)
component.load_global_nlu(user)


if __name__ == '__main__':
    component.run(debugging=True)