################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import os
from watson_machine_learning_client.libs.repo.mlrepository.meta_props import MetaProps
from watson_machine_learning_client.libs.repo.mlrepository.meta_names import MetaNames

class Artifact(object):
    """
    Class representing artifact.

    :param str uid: optional, uid which indicate that artifact already exists in repository service
    :param str name: optional, name of artifact
    :param MetaProps meta_props: optional, props used by other services

    :ivar str uid: uid which indicate that artifact already exists in repository service
    :ivar str name: name of artifact
    :ivar MetaProps meta_props: props used by other services
    """
    def __init__(self, uid, name, meta_props):
        if uid is not None and not isinstance(uid, str) and not isinstance(uid,unicode):
            raise ValueError('Invalid type for uid: {}'.format(uid.__class__.__name__))

        if name is not None and not isinstance(name, str) and not isinstance(name,unicode):
            raise ValueError('Invalid type for name: {}'.format(name.__class__.__name__))

        if not isinstance(meta_props, MetaProps):
            raise ValueError('Invalid type for meta_props: {}'.format(meta_props.__class__.__name__))

        self.uid = uid
        self.name = name
        self.meta = meta_props

    def reader(self):
        """
        Returns reader to content of pipeline/pipeline model inside.

        :return: Reader connected to pyspark.ml.Pipeline/PipelineModel
        :rtype: ContentReader
        """
        from watson_machine_learning_client.libs.repo.mlrepositoryclient import ContentReader

        try:
            return self._reader
        except:
            if self._content_href is not None:
                if self.meta.prop(MetaNames.SPACE_UID) is not None:
                    if 'DEPLOYMENT_PRIVATE' in os.environ and os.environ['DEPLOYMENT_PRIVATE'] == 'icp4d':
                        space_url = self.meta.prop(MetaNames.SPACE_UID)
                        space_id = space_url.split('/')[-1]
                        self._content_href = self._content_href + "?space_id=" + space_id
                if self.meta.prop(MetaNames.PROJECT_UID) is not None:
                    if 'DEPLOYMENT_PRIVATE' in os.environ and os.environ['DEPLOYMENT_PRIVATE'] == 'icp4d':
                        project_url = self.meta.prop(MetaNames.PROJECT_UID)
                        project_id = project_url.split('/')[-1]
                        self._content_href = self._content_href + "?project_id=" + project_id
                self._reader = ContentReader(self._content_href,
                                             self.client.repository_api)
            else:
                self._reader = None
            return self._reader
