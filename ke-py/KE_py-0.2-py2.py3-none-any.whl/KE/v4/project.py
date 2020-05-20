# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.base import Base
from KE.util import danger_action
from datetime import datetime


class Project(Base):

    def __init__(self, client=None, project_id=None, name=''):
        """Project Object
        """
        super(Project, self).__init__(client=client)
        self.id = project_id
        self.name = name

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the project json object to a Project object

        :param client: the KE client
        :param json_obj: the project json object
        :return: Project object
        """
        project = Project(client=client, project_id=json_obj['uuid'], name=json_obj['name'])
        project.last_modified = json_obj['last_modified']
        project.status = json_obj['status']
        project.create_time_utc = json_obj['create_time_utc']
        project.create_time_dt = datetime.utcfromtimestamp(json_obj.get('create_time_utc', 0) / 1000)
        project.description = json_obj['description']
        project.owner = json_obj['owner']
        project.last_modified = json_obj['last_modified']
        project.override_kylin_properties = json_obj['override_kylin_properties']
        project.version = json_obj['version']
        project.name = json_obj['name']
        project.segment_config = json_obj['segment_config']

        return project

    def models(self, name=None, offset=0, size=20, exact=True, status=None):
        """Get Models

        :param name:
        :param offset:
        :param size:
        :param exact: 是否和模型名称完全匹配
        :param status: 模型状态
        :return: Model List
        """
        return self._client.models(project=self.name, name=name, offset=offset, size=size, exact=exact, status=status)

    def jobs(self, time_filter=4, offset=0, size=20, sort_by='last_modify', reverse=True, key=None):
        """Get jobs

        :parameter:
            time_filter:
                最近一天	0
                最近一周	1
                最近一月	2
                最近一年	3
                所有	4

            offset: - 可选 int，每页返回的任务的偏移量，默认值为 "0"
            size: - 可选 int，每页返回的任务数量，默认值为 "20"
            sort_by: - 可选 string，排序字段，默认为 "last_modified"
            reverse: - 可选 boolean，是否倒序，默认为 "true"
            key: 筛选字段，目前支持筛选任务 ID 及任务对象名称

        :return: Job object list
        :rtype: jobs
        """
        return self._client.jobs(project=self.name, time_filter=time_filter,
                                 offset=offset, size=size, sort_by=sort_by,
                                 reverse=reverse, key=key)

    def push_down_config(self):
        pass

    @danger_action
    def delete(self):
        json_obj = self._client.fetch_json(uri='/api/projects/{project}'.format(project=self.name), method='DELETE')
        return json_obj['data']

    def __repr__(self):
        return '<Project %s>' % self.name
