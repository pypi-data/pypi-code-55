org_read = "/api/org/%s/read" #%(org_id)

project_list = "/api/project/list"
project_read = "/api/project/%s/detail/read" #%(project_idx)

episode_list = "/api/project/%s/episode/list" #%(project_idx)
episode_create = "/api/project/%s/episode/create" #%(project_idx)

sequence_list = "/api/project/%s/episode/%s/sequence/list" #%(project_idx,episode_idx)
sequence_create = "/api/project/%s/episode/%s/sequence/create" #%(project_idx,episode_idx)

shot_list =  "/api/project/%s/episode/%s/sequence/%s/shot/list" #%(project_idx,episode_idx,sequence_idx)
shot_read = "/api/project/%s/shot/%s/read" #%(project_idx,shot_idx)
shot_create = "/api/project/%s/episode/%s/sequence/%s/shot/create" #%(project_idx,episode_idx,sequence_idx)
shot_thumbnail_up = "/api/project/%s/shot/%s/thumbnail/update" #%(project_idx,shot_idx)
shot_overview_all = "/api/project/%s/shot/task/overview/read" #%(project_idx)
shot_overview = "/api/project/%s/episode/%s/shot/task/overview/read" #%(project_idx,episode_idx)
shot_relation = "/api/project/%s/episode/%s/shot/asset/relation/overview/read" #%(project_idx,episode_idx)

category_list = "/api/project/%s/asset/category/list/detail" #%(project_idx)
category_create = "/api/project/%s/asset/category/create" #%(project_idx)

asset_list = "/api/project/%s/category/%s/asset/list" #%(project_idx,category_idx)
asset_create = "/api/project/%s/category/%s/asset/create" #%(project_idx,category_idx)
asset_thumbnail_up ="/api/project/%s/asset/%s/thumbnail/update" #%(project_idx,asset_idx)
asset_overview_all = "/api/project/%s/asset/task/overview/read" #%(project_idx)
asset_overview_category = "/api/project/%s/category/%s/asset/task/overview/read" #%(project_idx,category_idx)

asset_task_read = "/api/asset/task/%s/read" #%(task_idx)
asset_task_list = "/api/project/%s/asset/%s/task/list" #%(project_idx,asset_idx)
asset_task_create = "/api/project/%s/asset/%s/task/create" #%(project_idx,asset_idx)
asset_task_status_change = "/api/project/%s/asset/task/%s/status/update" #%(project_idx,task_idx)
asset_task_start = "/api/project/%s/asset/task/%s/start" #%(project_idx,task_idx)
asset_task_stop = "/api/project/%s/asset/task/%s/stop" #%(project_idx,task_idx)

shot_task_read = "/api/shot/task/%s/read" #%(task_idx)
shot_task_list = "/api/project/%s/shot/%s/task/list" #%(project_idx,shot_idx)
shot_task_create = "/api/project/%s/shot/%s/task/create" #%(project_idx,shot_idx)
shot_task_status_change = "/api/project/%s/shot/task/%s/status/update" #%(project_idx,task_idx)
shot_task_start = "/api/project/%s/shot/task/%s/start" #%(project_idx,task_idx)
shot_task_stop = "/api/project/%s/shot/task/%s/stop" #%(project_idx,task_idx)

mytask_todo = "/api/mytask/todo/read"
mytask_inprogress = "/api/mytask/inprogress/read/%s" #%(last)
mytask_done = "/api/mytask/done/read"
mytask_cc = "/api/mytask/cc/read/%s" #%(last)

team_list = "/api/team/list"
team_user_list =  "/api/team/%s/user/list" #%(team_idx)

track_version = "/api/project/%s/track/from/%s/to/%s/version/read/%s" #%(project_idx,from_date,to_date,last)

user_list = "/api/user/list"

version_key = "/api/%s/task/%s/version/setting/create" #%(which,task_idx)
version_key_read = "/api/version/setting/read"
version_create = "/api/%s/task/version/create" #%(which)

publish_key = "/api/%s/task/%s/publish/setting/create" #%{which,task_idx}
publish_key_read = "/api/publish/setting/read"
publish_create = '/api/%s/task/publish/create' #%(which)