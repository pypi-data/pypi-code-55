#!python

from quixote import new_context
from quixote.inspection import new_inspection_result, KOError, InternalError, TimeoutError
import panza
import os
import json
import sys
import traceback
from typing import Dict, Any
from panza._utils import augment_syspath

os.chdir("/moulinette/workdir")

with open("/moulinette/context.json", 'r') as context_file:
    context: Dict[str, Any] = json.load(context_file)

os.remove("/moulinette/context.json")

global_failures = []
global_points = 0
job_failure = None

with augment_syspath(["/moulinette"]):
    with new_context(resources_path="/moulinette/resources", delivery_path="/moulinette/rendu", **context):
        blueprint = panza.BlueprintLoader.load_from_directory("/moulinette", complete_load=True)

        print(f"Running inspectors for {blueprint.name}")
        for inspector in blueprint.inspectors:
            with new_inspection_result() as result:
                try:
                    inspector()
                except (KOError, InternalError, AssertionError, TimeoutError) as e:
                    result["assertion_failure"] = str(e)
                    if inspector.checklist_entry:
                        result["checklist"][inspector.checklist_entry] = 0
                    else:
                        result["points"] = 0
                        # mark the reason and optional detail in the inspection result
                    if inspector.is_critical:
                        print("Critical step failure, skipping remaining inspectors")
                        break
                except Exception as e:
                    print(f"Unexpected exception escaped from inspector: {type(e).__name__}: {e}")
                    traceback.print_exc(file=sys.stdout)
                    job_failure = e
                    break
                finally:
                    if inspector.post_process:
                        inspector.post_process(checklist_entry=inspector.checklist_entry)

                    for _, requirement_message, _ in filter(lambda req: not req[0], result["requirements"]):
                        global_failures.append(f"requirement failed: {requirement_message}")
                    if result["assertion_failure"] is not None:
                        global_failures.append(f"assertion failed: {result['assertion_failure']}")
                    global_points += result["points"]

with open("/moulinette/result.json", 'w') as f:
    if job_failure is not None:
        result = {"error": {"message": str(job_failure)}}
    else:
        result = {"success": {"messages": global_failures, "points": global_points}}
    json.dump(result, f, indent=4)

print("Done")
