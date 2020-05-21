import copy
from datetime import datetime, timedelta
from typing import List, Union

MILESTONES_TEMPLATE = [
    {
        'audience': ['pi', 'lead', 'group members', 'collaborators'],
        'due_date': timedelta(days=7),
        'name': 'Kick off meeting',
        'objective': 'roll out of project to team',
        'status': 'proposed'
    },
    {
        'audience': ['pi', 'lead', 'group members'],
        'due_date': timedelta(days=14),
        'name': 'project lead presentation',
        'objective': 'lead presents background reading and initial project plan',
        'status': 'proposed'
    },
    {
        'audience': ['pi', 'lead', 'group members'],
        'due_date': timedelta(days=28),
        'name': 'planning meeting',
        'objective': 'develop a detailed plan with dates',
        'status': 'proposed'
    }
]

DELIVERABLE_TEMPLATE = {
    "audience": ['pi', 'lead', 'group members', 'collaborators'],
    "due_date": timedelta(days=365),
    "success_def": "audience is happy",
    "scope": [
        "UCs that are supported or some other scope description "
        "if it is software",
        "sketch of science story if it is paper"
    ],
    "platform": "description of how and where the audience will access "
                "the deliverable.  Journal if it is a paper",
    "roll_out": [
        "steps that the audience will take to access and interact with "
        "the deliverable",
        "not needed for paper submissions"
    ],
    "status": "proposed"
}


def _assgin_due_date(template: Union[List[dict], dict], start_date: str) -> None:
    """Assign the due date to tempalte according to the start_date."""
    if isinstance(template, dict):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        time_gap = template['due_date']
        due_date = start_date + time_gap
        template['due_date'] = due_date.strftime('%Y-%m-%d')
    elif isinstance(template, list):
        for item in template:
            _assgin_due_date(item, start_date)
    else:
        raise TypeError("Unkown template type: {}".format(type(template)))
    return


def auto_gen_milestons(start_date: str, template: List[dict] = None) -> List[dict]:
    """Automatically generate the milestones list according to the template."""
    if template is None:
        template = copy.deepcopy(MILESTONES_TEMPLATE)
    _assgin_due_date(template, start_date)
    return template


def auto_gen_deliverable(start_date: str, template: dict = None) -> dict:
    """Automatically generate the deliverable dictionary according to the template."""
    if template is None:
        template = copy.deepcopy(DELIVERABLE_TEMPLATE)
    _assgin_due_date(template, start_date)
    return template
