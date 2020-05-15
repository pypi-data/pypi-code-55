####################################################################################################

import os

from Pyterate.Template import TemplateEnvironment, TemplateAggregator

####################################################################################################

template_path = os.path.dirname(__file__)

template_environment = TemplateEnvironment(template_path)

template_aggregator = TemplateAggregator(template_environment)

kwargs = {
    'title': 'A Title',
}

template_aggregator.append('toc.jinja', **kwargs)
print(template_aggregator)
