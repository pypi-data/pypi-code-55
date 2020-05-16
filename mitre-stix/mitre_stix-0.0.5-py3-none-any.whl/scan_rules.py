import pkgutil
import importlib
import mitre_stix.rules as rules

def import_package(package):
    modules = []
    prefix = package.__name__ + "."
    for loader, name, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        if ispkg:
            continue
        modules.append(importlib.import_module(name))
    return modules

def logs(bundles):
    signatures = import_package(rules)
    hits = []
    for sig in signatures:
        scan = sig.mitre_rules()
        result = scan.run_rules(bundles)
        if result is not False:
            hits.append({'tactic': result.tactic, 'tid': result.tid, 'name':  result.name, \
                        'description': result.description, 'oid': result.oid})
    return hits