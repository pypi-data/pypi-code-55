#!/usr/bin/env python
import rospy


class SharedSubscriber(rospy.Subscriber):
    def __init__(self, name, data_class, extract_uuid_callback, callback_args=None, queue_size=None, tcp_nodelay=False):
        super(SharedSubscriber, self).__init__(name, data_class, self._callback,
                                               callback_args=callback_args, queue_size=queue_size,
                                               tcp_nodelay=tcp_nodelay)
        self.subscribers = {}
        assert extract_uuid_callback is not None
        self.extract_uuid = extract_uuid_callback

    def add_callback(self, uuid, callback):
        self.subscribers[uuid] = callback

    def remove_callback(self, uuid):
        self.subscribers.pop(uuid, None)

    def _callback(self, msg):
        # Dispatch the callback
        uuid = self.extract_uuid(msg)
        callback = self.subscribers.get(uuid)
        if callback is None:
            rospy.loginfo('Callback not found, uuid={}'.format(uuid))
            return
        callback(msg)
