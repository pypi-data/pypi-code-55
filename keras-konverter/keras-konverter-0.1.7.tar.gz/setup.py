# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konverter', 'konverter.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.3,<2.0.0', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['konverter = konverter.__main__:run']}

setup_kwargs = {
    'name': 'keras-konverter',
    'version': '0.1.7',
    'description': 'A tool to convert simple Keras models to pure Python + NumPy',
    'long_description': '# Konverter ![Konverter Tests](https://github.com/ShaneSmiskol/Konverter/workflows/Konverter%20Tests/badge.svg)\n### Convert your Keras models into pure Python + NumPy.\n\nThe goal of this tool is to provide a quick and easy way to execute Keras models on machines or setups where utilizing TensorFlow/Keras is impossible. Specifically, in my case, to replace SNPE (Snapdragon Neural Processing Engine) for inference on phones with Python.\n\n## Supported Keras Model Attributes\n- Models:\n  - Sequential\n- Layers:\n  - Dense\n  - Dropout\n    - Will be ignored during inference (SNPE 1.19 does NOT support dropout with Keras!)\n  - SimpleRNN\n    - Batch predictions do not currently work correctly.\n  - GRU\n    - **Important:** The current GRU support is based on [`GRU v3`](https://www.tensorflow.org/api_docs/python/tf/keras/layers/GRU) in tf.keras 2.1.0. It will not work correctly with older versions of TensorFlow.\n    - Batch prediction untested\n  - BatchNormalization\n    - Works with all supported layers\n- Activations:\n  - ReLU\n  - Sigmoid\n  - Softmax\n  - Tanh\n  - Linear/None\n\n#### Roadmap\nThe project to do list can be [found here](https://github.com/ShaneSmiskol/Konverter/projects/1).\n\n## Features\n- Super quick conversion of your models. Takes less than a second.\n- Usually reduces the size of Keras models by about 69.37%.\n- In some cases, prediction is quicker than Keras or SNPE (dense models).\n  - RNNs: Since we lose the GPU using NumPy, predictions may be slower\n- Stores the weights and biases of your model in a separate compressed NumPy file.\n\n## Benchmarks\nBenchmarks can be found in [BENCHMARKS.md](BENCHMARKS.md).\n\n## Installation & Usage\n### Install Konverter using pip:\n`pip install keras-konverter`\n\n### Import Konverter and create an instance:\n```python\n>>> from konverter import Konverter\n>>> konverter = Konverter()\n```\n\nNow you can use the instance to Konvert a model:\n```python\n>>> konverter.konvert(input_model=\'examples/all_dense.h5\', output_file=\'examples/all_dense.py\')\n```\n\nValid parameters:\n- `input_model`: Either the the location of your tf.keras .h5 model, or a preloaded model\n- `output_file`: The desired path and name of the output files, will be automatically formatted if .py is the suffix\n- Optional:\n  - `indent_spaces`: The number of spaces to use for indentation\n  - `verbose`: To print status messages from Konverter\n  - `use_watermark`: To prepend a watermark comment to model wrapper\n\n*Note: The model file will be saved as `f\'{output_file}.py\'` and the weights will be saved as `f\'{output_file}_weights.npz\'` in the same directory. Make sure to change the path inside the model wrapper if you move the files after Konversion.*\n\nThat\'s it! If your model is supported (check [Supported Keras Model Attributes](#Supported-Keras-Model-Attributes)), then your newly converted Konverter model should be ready to go.\n\nTo predict: Import your model wrapper and run the `predict()` function. Always double check that the outputs closely match your Keras model\'s. Automatic verification will come soon. **For safety, always make sure your input is a `np.float32` array.**\n\n```python\nimport numpy as np\nfrom examples.all_dense import predict\npredict(np.random.rand(200).astype(np.float32))\n```\n\n[See limitations and issues.](#Current-Limitations-and-Issues)\n\n## Demo:\n<img src="https://raw.githubusercontent.com/ShaneSmiskol/Konverter/master/.media/konverter.gif?raw=true" width="913">\n\n\n## Dependencies\nThanks to [@apiad](https://github.com/apiad) you can now use [Poetry](https://github.com/python-poetry/poetry) to install all the needed dependencies for this tool! However the requirements are a pretty short list:\n- It seems most versions of TensorFlow that include Keras work perfectly fine. Tested from 1.14 to 2.1.0 using Actions and no issues have occurred.\n  - **Important**: You must create your models with tf.keras currently (not keras)\n- Python >= 3.6 (for the glorious f-strings!)\n- [Typer](https://github.com/tiangolo/typer/issues), requires >= 3.6\n\nTo install all needed dependencies, simply `cd` into the base directory of Konverter, and run:\n\n```\npoetry install --no-dev\n```\n\n## Current Limitations and Issues\n- Dimensionality of input data:\n\n  When working with models using `softmax`, the dimensionality of the input data matters. For example, predicting on the same data with different input dimensionality sometimes results in different outputs:\n  ```python\n  >>> model.predict([[1, 3, 5]])  # keras model, correct output\n  array([[14.792273, 15.59787 , 15.543163]])\n  >>> predict([[1, 3, 5]])  # Konverted model, wrong output\n  array([[11.97839948, 18.09931636, 15.48014805]])\n  >>> predict([1, 3, 5])  # And correct output\n  array([14.79227209, 15.59786987, 15.54316282])\n  ```\n\n  If trying a batch prediction with classes and `softmax`, the model fails completely:\n  ```python\n  >>> predict([[0.5], [0.5]])\n  array([[0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5]])\n  ```\n\n  Always double check that predictions are working correctly before deploying the model.\n- Batch prediction with SimpleRNN (and possibly all RNN) layers\n\n  Currently, the converted model has no way of determining if you\'re feeding a single prediction or a batch of predictions, and it will fail to give the correct output. Support will be added soon.\n',
    'author': 'Shane Smiskol',
    'author_email': 'shane@smiskol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ShaneSmiskol/Konverter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
