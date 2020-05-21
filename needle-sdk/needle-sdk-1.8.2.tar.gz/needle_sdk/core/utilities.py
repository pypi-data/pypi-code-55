# Check if keys have sensitive info
def clean_server_values(arg_name, arg_value):
    try:
        # Credit-card data in argument value?
        import re
        pattern = r'(\d[ -]*){13,16}'
        pattern = re.compile(pattern, re.IGNORECASE)

        # Sensitive arg names?
        sensitive_arg_names = ['password', 'passwd', 'api_key', 'apikey', 'access_token', 'secret', 'authorization']

        if len(pattern.findall(arg_value)) > 0 or arg_name in sensitive_arg_names:
            # Redact value
            arg_value = '[Sensitive data removed by Needle.sh]'
    except Exception as e:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
        error_data = str(e)
        needle_app.add_error('Error while checking sensitive data', error_data)

    return arg_name, arg_value