import time

from . import *

# show_mapping(align('resources/tests/text_audio_head/audio', 'resources/tests/text_audio_head/text', 'resources/tests/text_audio_head/'))
# show_mapping(align('resources/tests/audio_head/audio', 'resources/tests/audio_head/text', 'resources/tests/audio_head/'))
# show_mapping(align('resources/tests/3_to_3/audio', 'resources/tests/3_to_3/text', 'resources/tests/3_to_3/'))

n = time.time()
sync_map = align(
    'resources/tests/3_to_3/text',
    'resources/tests/3_to_3/audio',
    'resources/tests/3_to_3/out',
    output_format='json',
    sync_map_text_path_prefix='../text/',
    sync_map_audio_path_prefix='../audio/'
)

print_sync_map(sync_map)

# sync_map = align('resources/duty/audio', 'resources/duty/text', 'resources/duty/')
# sync_map = align('resources/essays/audio', 'resources/essays/text', 'resources/essays/')
print(time.time() - n)