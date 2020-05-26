from dynamite_nsm.services.filebeat import config
INSTALL_DIRECTORY = '/Users/jaminbecker/PycharmProjects/dynamite-nsm-project/utils/default_configs/filebeat'

cfg = config.ConfigManager(INSTALL_DIRECTORY)
"""
cfg.set_logstash_targets(
    ['localhost:5044']
)

cfg.set_kafka_targets(
    ['localhost:9092'], 'dynamite-events'
)
"""
print(cfg.is_logstash_output_enabled())
cfg.write_config()