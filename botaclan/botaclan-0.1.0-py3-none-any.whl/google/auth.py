from google.oauth2 import service_account


def generate_credentials(credentials_path: str) -> service_account.Credentials:
    return service_account.Credentials.from_service_account_file(credentials_path)
