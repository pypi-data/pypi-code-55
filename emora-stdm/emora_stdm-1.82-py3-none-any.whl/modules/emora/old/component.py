
from emora_stdm import DialogueFlow


component = DialogueFlow('_local_start')
component.add_system_transition('exit', 'SYSTEM:root', '')
component.knowledge_base().load_json_file('_common.json')
component.knowledge_base().load_json_file('_component.json')
component.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GOAL(component)'
}

user = {
    'state': 'user'
}

component.load_transitions(system)
component.load_global_nlu(user)


if __name__ == '__main__':
    component.run(debugging=True)