import requests

def get(email, key):
    if isinstance(email, str):
        return requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={"hibp-api-key": key}  
        )
    
    if isinstance(email, list):
        result = {}
        for e in email:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{e}",
                headers={"hibp-api-key": key}  
            )
            result[e] = r
        return result
    