####################################################################################################

import Pyterate.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

import nbformat

from Pyterate.Jupyter import JupyterClient

####################################################################################################

jupyter_client = JupyterClient(working_directory='.')

for code in (
        '1 + 1',
        'print("foo")',
        '''
import numpy as np
import matplotlib.pyplot as plt
        ''',
        '''
figure = plt.figure(1, (20, 10))
x = np.arange(1, 10, .1)
y = np.sin(x)
        ''',
        'plt.plot(x, y)',
        'plt.show()',
):
    outputs = jupyter_client.run_cell(code)
    if outputs:
        output = outputs[0]
        # if output.output_type == 'display_data':
        #     output.data['image/png'] = None
        print()
        print('OUTPUTS >>>>>\n', output, '\n')

jupyter_client.restart()
outputs = jupyter_client.run_cell('2*2')
print(outputs)
