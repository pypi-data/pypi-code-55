from setuptools import setup, find_packages

setup(
    name             = 'sandwichR',
    version          = '0.0.12',
    description      = 'Python library for Sandwich',
    author           = 'Roborobo',
    author_email     = 'roborobolab@gmail.com',
    url              = 'https://eng.roborobo.co.kr/main',
    download_url     = 'https://github.com/RoboroboLab/Sandwich/archive/master.tar.gz',
    install_requires = [ ],
    packages         = find_packages(),
    keywords         = ['sandwichR','roborobo'],
    python_requires  = '>=3',
    package_data     =  { 
	'sandwichR' :[
		'pins/pins.config'
		'res/guide.png'
		'res/landmark/facelandmark_lbfmodel.yaml'
		'res/lbph/facelandmark_lbfmodel.yaml'
		'res/lbph/haarcascade_frontalface_alt.xml'
		'res/tensorflow/detect.tflite'
		'res/tensorflow/labelmap.txt'
	]},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
