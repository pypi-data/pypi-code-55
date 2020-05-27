from emora._flows.tournament import tournament
from emora._flows.school import school as school2
from emora._flows.baby import baby
from emora._flows.backstory import backstory
from emora._flows.competition import competition
from emora._flows.house import house
from emora._flows.reading import reading
from emora._flows.world import world
from emora._flows.work import work
from emora._flows.sibling import sibling
from emora._flows.relationships import relationships

from _globals import PATHDIR
from emora_stdm import CompositeDialogueFlow,DialogueFlow
import emora_stdm
from emora._flows._global_nlu import personal_nlu, global_update_rules

flow_components = {
    'tournament': tournament,
    'school_new': school2,
    'baby': baby,
    'house': house,
    'reading': reading,
    'competition': competition,
    'backstory': backstory,
    'world': world,
    'worklife': work,
    'sibling': sibling,
    'relationships': relationships
}

cdf = CompositeDialogueFlow('root', 'recovery_from_failure', 'recovery_from_failure', DialogueFlow.Speaker.USER)
cdf.add_state('root', 'root')
cdf.add_user_transition('root', 'root', '/.*/ #RAND(life_in,True)')
cdf.component('SYSTEM').knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))

for namespace, component in flow_components.items():
    cdf.add_component(component, namespace)

cdf.add_system_transition('root', 'house:start', '', score=1.5)
cdf.add_system_transition('root', 'worklife:start', '', score=3.0)
cdf.add_system_transition('root', 'school_new:start', '', score=4.0)
cdf.add_system_transition('root', 'sibling:start', '', score=1.5)
cdf.add_system_transition('root', 'relationships:dating', '', score=2.0)
cdf.add_system_transition('root', 'relationships:marriage', '', score=2.0)

cdf.add_system_transition('life_opening', 'house:start', '')
cdf.add_system_transition('life_opening', 'worklife:start', '')
cdf.add_system_transition('life_opening', 'school_new:start', '', score=3.0)
cdf.add_system_transition('life_opening', 'root', '', score=0.0)
cdf.controller().update_state_settings('life_opening', system_multi_hop=True)

for component in cdf.components():
    component.load_global_nlu(personal_nlu, 5.0)
    component.load_update_rules(global_update_rules)
    component.add_macros({'CNC': emora_stdm.CheckNotComponent(cdf)})

if __name__ == '__main__':
    #cdf.precache_transitions()
    cdf.run(debugging=False)