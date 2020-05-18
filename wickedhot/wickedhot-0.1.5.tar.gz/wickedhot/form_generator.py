from wickedhot.one_hot_encode import unknown_level_value
from wickedhot.html_form import form_data_to_form_elements, form_data_to_html_page


def encoder_package_to_schema(encoder_package):

    properties = {}
    stats = encoder_package['numeric_stats']
    for field in encoder_package['numeric_cols']:
        properties[field] = {
            "type": "number",
            "title": field.capitalize(),
            "required": True
        }

        if stats is not None:
            properties[field]['minimum'] = stats[field]['min']
            properties[field]['maximum'] = stats[field]['max']

    encoder_dicts = encoder_package['one_hot_encoder_dicts']

    for field, value_dicts in encoder_dicts.items():
        values = sorted(value_dicts.items(), key=lambda x: x[1])
        levels = [v[0] for v in values]
        levels = levels + [unknown_level_value]

        properties[field] = {
            "type": "string",
            "title": field.capitalize(),
            "required": True,
            "enum": levels
        }

    schema = {
        "title": "Input features",
        "description": "Enter features",
        "type": "object",
        "properties": properties
    }

    return schema


def encoder_package_to_options(encoder_package, post_url=None):
    """
    :param encoder_package: one hot encoder package
    :param post_url: url to send form data to on submission
        default is ''
        for testing purposes, you may use PUBLIC and it will use
        "http://httpbin.org/post" which prints the result
        this is not secure so don't do that with sensitive data
    :return:
    """

    if post_url is None:
        post_url = ''

    if post_url == 'PUBLIC':
        post_url = "http://httpbin.org/post"

    fields = {}
    for field in encoder_package['numeric_cols']:
        fields[field] = {
            "size": 20,
            # "helper": "Please enter %s" % field
        }

    encoder_dicts = encoder_package['one_hot_encoder_dicts']

    for field, value_dicts in encoder_dicts.items():
        values = sorted(value_dicts.items(), key=lambda x: x[1])
        levels = [v[0] for v in values]
        levels = levels + [unknown_level_value]

        fields[field] = {
            "type": "select",
            # "helper": "Select %s" % field,
            "optionLabels": levels,
            "sort": False
        }

    options = {
        "form": {
            "attributes": {
                "action": post_url,
                "method": "post"
            },
            "buttons": {
                "submit": {}
            }
        },
        "helper": "Hit submit to update the prediction",
        "fields": fields}

    return options


def encoder_package_to_form_data(encoder_package, post_url=None):
    """
    Generate the form
    :param encoder_package: encoder package dict
    :param post_url: url to send form data to on submission
        default is ''
        for testing purposes, you may use PUBLIC and it will use
        "http://httpbin.org/post" which prints the result
        this is not secure so don't do that with sensitive data
    :return: form data
    """

    schema = encoder_package_to_schema(encoder_package)
    options = encoder_package_to_options(encoder_package, post_url=post_url)

    stats = encoder_package['numeric_stats']

    if stats is None:
        data = {field: 0 for field in encoder_package['numeric_cols']}
    else:
        data = {field: "%0.2f" % stats[field]['median'] for field in encoder_package['numeric_cols']}

    form_data = {"schema": schema,
                 "options": options,
                 "view": "bootstrap-edit",
                 "data": data}

    return form_data


def encoder_package_to_form_elements(encoder_package, post_url=None):
    form_data = encoder_package_to_form_data(encoder_package, post_url=post_url)
    header_text, form_div = form_data_to_form_elements(form_data)
    return header_text, form_div


def encoder_package_to_html_page(encoder_package, post_url=None):
    form_data = encoder_package_to_form_data(encoder_package, post_url=post_url)
    return form_data_to_html_page(form_data)
