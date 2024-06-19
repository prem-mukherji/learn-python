from jwt import (
    jwk_from_pem,
    JWT
)
import os
import requests
import time

API_HOST = "https://api.github.com"


def headers_for_app(jwt):
    return {
        "Authorization": f"Bearer {jwt}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_jwt(app_id, private_key, expiry_secs: int = 600):
    
    with open(private_key, 'rb') as pemFile:
        signing_key = jwk_from_pem(pemFile.read())

    now = int(time.time())
    payload = {
        # Issued at time
        'iat': now,
        # JWT expiration time (10 minutes maximum)
        'exp': now + expiry_secs,
        # GitHub App's identifier
        'iss': app_id
    }
    jwt_instance = JWT()
    return jwt_instance.encode(payload, signing_key, alg='RS256')


def get_installation_id(session):
    r = session.get(f"{API_HOST}/orgs/Maersk-Global/installation")
    r.raise_for_status()
    return str(r.json()['id'])


def get_token(session, installation_id):
    r = session.post(f"{API_HOST}/app/installations/{installation_id}/access_tokens")
    r.raise_for_status()
    return r.json()


def do_token_acquisition(app_id, private_key, installation_id = None):
    jwt = get_jwt(app_id, private_key)
    session = requests.session()
    session.headers.update(headers_for_app(jwt))
    if installation_id is None:
        installation_id = get_installation_id(session)
    return get_token(session, installation_id)


def main(argv = None):
    app_id = "905414"
    installation_id = "51118907"
    private_key = "./rsa_private_key.pem"

    script_directory = os.path.dirname(os.path.abspath(__file__))
    filepath=os.path.join(script_directory, private_key)

    token = do_token_acquisition(app_id, filepath, installation_id)
    print(token['token'])

if __name__ == '__main__':
    main()
