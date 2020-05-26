import setuptools

setuptools.setup(
        name='hac_img',
		package_dir = {"":"src"},
        version='0.0.1',
		license='MIT',
        description='Hierarchical clustering algorithm for image clustering using Scikit-Image',
		author = 'Harish Mohan',                   
		author_email = 'mharish2797@gmail.com',
		url = 'https://mharish.dev',  
		download_url = 'https://github.com/mharish2797/hac_img/archive/0.0.1.tar.gz',    
		keywords = ['image', 'hierarchical', 'clustering'],   
        py_modules=["hac_img"],
        install_requires = ["scikit-image", "numpy", "Pillow"]
		
        )