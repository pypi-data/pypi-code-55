from distutils.core import setup, Extension

sfc_module = Extension('igeVmath', sources=['pyVectorMath.cpp'])

setup(name='igeVmath', version='0.5.8',
	author=u'Indigames',
	author_email='dev@indigames.net',
	description='C++ extension Vector Mathematics Package for Indi game engine.',
	ext_modules=[sfc_module],
	long_description='C++ extension Vector Mathematics Package for Indi game engine.',
	long_description_content_type='text/markdown',
	license='MIT',
	classifiers=[
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows',
		'Topic :: Games/Entertainment',
	],
)
