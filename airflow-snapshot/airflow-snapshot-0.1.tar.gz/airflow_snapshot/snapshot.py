import json
import os
import unittest

from airflow import DAG


class DoubleQuoteDict(dict):
    def __str__(self):
        return json.dumps(self, indent=2)


def having_cyclic_tasks_dependency(snapshot: json):
    for key, value in snapshot['tasks'].items():
        if key in value:
            return True
    return False


class Snapshot(unittest.TestCase):
    def __str__(self):
        return json.dumps(self)

    def create(dag: DAG):
        snapshot_location = "src/unittest/resources/"
        os.makedirs(os.path.dirname(snapshot_location), exist_ok=True)
        snapshot = {"dag_id": dag.dag_id, "task_count": len(dag.tasks), 'tasks': {}}
        all_tasks = list(map(lambda task: task, dag.tasks))
        for task in all_tasks:
            downstream_list = task.downstream_task_ids
            snapshot['tasks'][task.task_id] = sorted(downstream_list)
        f = open(f"{snapshot_location}/snapshot-{dag.dag_id}.json", "w+")
        quote_dict = DoubleQuoteDict(snapshot)
        f.write(quote_dict.__str__())
        return snapshot

    def validate(self, snapshot, actual_dag: DAG):
        print(f'Running snapshot test of <{actual_dag.dag_id}>')
        self.assertEqual(snapshot['dag_id'], actual_dag.dag_id)
        self.assertEqual(snapshot['task_count'], actual_dag.task_count, f"Count mismatch in dag {actual_dag.dag_id}")
        for task in snapshot['tasks'].keys():
            try:
                downstream = actual_dag.get_task(task).downstream_task_ids
            except:
                self.assertTrue(False, f"Task {task} not found in dag")
            self.assertEqual(list(sorted(downstream)), sorted(snapshot['tasks'][task]),
                             f"\nDependency mismatch in dag <<<{actual_dag.dag_id}>>> for task {task}:\n actual:"
                             f" {list(sorted(downstream))} \n expected: {sorted(snapshot['tasks'][task])} ")
        self.assertFalse(having_cyclic_tasks_dependency(snapshot))
        return True

