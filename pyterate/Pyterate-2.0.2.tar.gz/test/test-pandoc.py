# https://pypi.python.org/pypi/pypandoc

# import os
# os.environ.setdefault('PYPANDOC_PANDOC', '/home/x/whatever/pandoc')

import pypandoc

output = pypandoc.convert_text('#some title', 'rst', format='md')
print(output)

output = pypandoc.convert_text('##some title', 'rst', format='md')
print(output)

# input_file = '../doc/sphinx/source/examples/document-generator/full-test.rst'
# pypandoc.convert_file(input_file, to='md', outputfile="full-test.md")
# pypandoc.convert_file(input_file, to='html5', outputfile="full-test.html5")
