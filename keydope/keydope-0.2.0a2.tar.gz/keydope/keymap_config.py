# import yaml

# from keydope import keymap

# def parse_yaml_config(yaml_content: str):
#     yaml_object = yaml.load(yaml_content)
#     if 'top_level_keymap' not in yaml_object:
#         raise ValueError('No top_level_keymap provided.')
#     top_level_keymap = parse_keymap(yaml_object['top_level_keymap'])
#     fallback_keymap = None
#     if 'fallback_keymap' in yaml_object:
#         fallback_keymap = parse_keymap(fallback_keymap)
#     return keymap.KeyProcessor(top_level_keymap, fallback_keymap)
