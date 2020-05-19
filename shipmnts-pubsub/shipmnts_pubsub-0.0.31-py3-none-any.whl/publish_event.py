import logging
import json
from google.cloud import pubsub_v1


retry_settings = {
    "interfaces": {
        "google.pubsub.v1.Publisher": {
            "retry_codes": {
                "publish": [
                    "ABORTED",
                    "CANCELLED",
                    "DEADLINE_EXCEEDED",
                    "INTERNAL",
                    "RESOURCE_EXHAUSTED",
                    "UNAVAILABLE",
                    "UNKNOWN",
                ]
            },
            "retry_params": {
                "messaging": {
                    "initial_retry_delay_millis": 100,  # default: 100
                    "retry_delay_multiplier": 1.3,  # default: 1.3
                    "max_retry_delay_millis": 60000,  # default: 60000
                    "initial_rpc_timeout_millis": 5000,  # default: 25000
                    "rpc_timeout_multiplier": 1.0,  # default: 1.0
                    "max_rpc_timeout_millis": 600000,  # default: 30000
                    "total_timeout_millis": 600000,  # default: 600000
                }
            },
            "methods": {
                "Publish": {
                    "retry_codes_name": "publish",
                    "retry_params_name": "messaging",
                }
            },
        }
    }
}
"""
Retry settings control both the total number of retries and exponential backoff (how long the client waits between subsequent retries). The initial RPC timeout is the time the client waits for the initial RPC to succeed before retrying. The total timeout is the time the client waits before it stops retrying. To retry publish requests, the initial RPC timeout should be shorter than the total timeout.

Once the first RPC fails or times out, the exponential backoff logic determines when the subsequent retries occur. On each retry, the RPC timeout increases by this multiplier, up to the maximum RPC timeout. In addition, the retry delay settings determine how long the client waits between getting an error or timeout and initiating the next request.
"""

publisher = pubsub_v1.PublisherClient(client_config=retry_settings)
def publish_event(data, project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    topic_path = publisher.topic_path(project_id, topic_name)
    logging.info("{} Topic Path".format(topic_path))

    def callback(message_future):
        # When timeout is unspecified, the exception method waits indefinitely.
        if message_future.exception(timeout=30):
            logging.info(
                "Publishing message on {} threw an Exception {}.".format(
                    topic_name, message_future.exception()
                )
            )
        else:
            logging.info(message_future.result())

    logging.info("Published message IDs:")
    data = json.dumps(data).encode("utf-8")
    message_future = publisher.publish(topic_path, data=data)
    message_future.add_done_callback(callback)
    message_future.result()
 