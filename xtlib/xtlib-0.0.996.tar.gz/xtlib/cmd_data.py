''' cmd_data.py: contains information about each XT command:
    - name          (str: name of the cmd)
    - init_cont     (boolean: should controller be initialized on current box?)
    - needs_ws      (boolean: does this command need the default workspace to exist?)
    - options       (list: valid option names for this cmd)
'''

# 37 XT Commands
# Python and Run commands have 22 options.

command_info = [
    {"name": "addr", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "attach", "init_cont": False, "needs_ws": True, "options": []},
    {"name": "cat", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "config", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "create.workspace", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "delete.file", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "delete.workspace", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "diagnostics", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "dir", "init_cont": False, "needs_ws": False, "options": ["subdirs"]},
    {"name": "download.file", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "explore", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "extract", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "help", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "keysend", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "keygen", "init_cont": False, "needs_ws": False, "options": ["overwrite"]},
    {"name": "kill", "init_cont": False, "needs_ws": True, "options": ["job"]},
    {"name": "list.boxes", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "list.experiments", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "list.files", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "list.pools", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "list.jobs", "init_cont": False, "needs_ws": False, "options": []},

    {"name": "list.runs", "init_cont": False, "needs_ws": False, "options": [
            "detail", "flat", "sort", "reverse", "escape", "boxout", "monitor", 
            "max-width", "precision", "first", "last",
            "active", "finished", "queued", "spawning", "running", "killed", 
            "aborted", "error", "completed", "unknown"
    ]},

    {"name": "list.workspaces", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "max-runs", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "plot", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "repl", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "rerun", "init_cont": True, "needs_ws": True, "options": ["box"]},
    {"name": "ssh", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "status", "init_cont": False, "needs_ws": True, "options": ["box", "active", "queued", "monitor", "auto-start"]},
    {"name": "upload.file", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "version", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "view.console", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "view.log", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "view.metrics", "init_cont": False, "needs_ws": False, "options": []},
    {"name": "workspace", "init_cont": False, "needs_ws": False, "options": []},

    {"name": "python", "init_cont": True, "needs_ws": True,
        "options": ["hold", "box", "pool", "workspace", "log", "capture", "notes", "experiment", "store",
            "description", "max-runs", "runs", "dry-run", "repeat", "scrape", "vm-size", "azure-image", "nodes", 
            "demand-mode", "resume", "keep-name", "attach"]},

    {"name": "run", "init_cont": True, "needs_ws": True,
        "options": ["hold", "box", "pool", "workspace", "log", "capture", "notes", "experiment", "store",
            "description", "max-runs", "runs", "dry-run", "repeat", "scrape", "vm-size", "azure-image", "nodes",
            "demand-mode", "resume", "keep-name", "attach"]},

]

