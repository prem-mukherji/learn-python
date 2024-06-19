import yaml
import os
import shutil
from git import Repo
from weasyprint import HTML
from markdown2 import markdown
import msal
import requests
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient

# Read settings from a YAML file and return the configuration.
def get_config(filename):
    
    print(f"Read configuration file {filename}")
    try:
        with open(filename, 'r') as file:
            settings = yaml.safe_load(file)
            if settings != None and settings["subscribers"] != None:
               return settings["subscribers"]
        return {}
    except Exception as e:
        print(f"Failed to read settings from {filename}: {e}")
        return {}


# get wiki cloned locally
def get_wiki_by_cloning(owner, repoName):
    if len(owner) == 0 :
        print(f"owner cannot be null")
        return False
    
    if len(repoName) == 0:
        print(f"repoName cannot be null")
        return False
        
    try:
        wiki_url = f"https://{os.getenv('GITHUB_SERVICE_ACCOUNT')}:{os.getenv('GITHUB_SERVICE_ACCOUNT_TOKEN')}@github.com/{owner}/{repoName}.wiki.git"
        print("url:" + wiki_url)
        local_path = f'./wiki/{repoName}'
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        Repo.clone_from(wiki_url, local_path)
        return True
    except Exception as e:
        print(f"Failed to clone {owner}/{repoName}: {e}")
        return False


def convert_directory_markdown_to_pdf(input_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):

        input_file_path = os.path.join(input_dir, filename)
        if os.path.isdir(input_file_path) and filename != ".git":
            convert_directory_markdown_to_pdf(input_dir + "/" + filename, output_dir+"/"+filename+"-pdf")
        
        if filename.endswith('.md'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_name = filename[:-3] + '.pdf'
            output_file_path = os.path.join(output_dir, output_file_name)

            try:
                # Read the Markdown file
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    markdown_text = file.read()

                # Convert Markdown to HTML
                html_text = markdown(markdown_text)

                # Convert HTML to PDF
                HTML(string=html_text).write_pdf(output_file_path)
                print(f"Converted {input_file_path} to {output_file_path}")
            except Exception as e:
                print(f"Failed to convert {input_file_path}: {e}")
                return False

def App():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    subscriberFile = os.path.join(script_directory, 'subscriberInfo.yaml')

    products = get_config(subscriberFile)

    for product in products:
        print(f"{product['name']} : {product['githubwiki']}" )
        content = get_wiki_by_cloning("Maersk-Global", product['githubwiki'])
        if content :
            print(f"successfully fetched {product['name']}")
            input_directory = os.path.join(script_directory, './wiki/' + product['githubwiki'])
            output_directory = os.path.join(script_directory, './wiki/' + product['githubwiki'] + '-pdf')
            convert_directory_markdown_to_pdf('./wiki/' + product['githubwiki'], output_directory)
        else:
            print(f"Failed to fetch {product['name']}")
        

def get_access_token_using_msal():
    app = msal.ConfidentialClientApplication(
        client_id="", 
        authority="https://login.microsoftonline.com/67657",
        client_credential=''
    )

    accounts = app.get_accounts()
    print(accounts)

    scopes = ["api://2187a198-e1af-4748-87fa-1ed245c4cd27/Storage.Access"]
    # result = app.acquire_token_for_client(scopes=scopes)
    result = app.acquire_token_for_client(scopes=scopes)
    return result["access_token"]

def get_access_token_using_rest_api():
    authority = "https://login.microsoftonline.com/8768768/oauth2/token"
    clientId = ""
    clientSecret = ""
    scope=""
    response = requests.post(
        url = authority,
        data = {
            'grant_type': 'client_credentials',
            'client_id' : clientId,
            'client_secret': clientSecret,
            'scope':scope
        },
        headers = { 'content-type': "application/x-www-form-urlencoded" }
        )
    token = response.json()['access_token']
    return token

def get_access_token_using_azure_identity():

    # Create a ClientSecretCredential object
    credential = ClientSecretCredential(
        tenant_id ="",
        client_id ="",
        client_secret =""
    )

    token = credential.get_token("api://klkjlj/Storage.Access")
    print("Access Token:", token.token)


def get_access_token_using_mdp_code():
    tenant_id = ""
    client_id = ""
    client_secret = ''
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    # Parameters to get the token
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "",
        "redirect_uri": "https://jwt.io"
    }
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token = token_response.json().get("access_token")
    print(token)

def get_access_token_hardcoded():
    return "wTlHQ"

def uploadDocuments(file):
    uploadURL = ""
    headers = {"Authorization": "Bearer " + get_access_token_hardcoded()}
    filepath=os.path.join(script_directory, "./wiki/capella-docs-pdf/Using-Capella.pdf")    
    files=[  ('file',('Using-Capella.pdf',open(filepath,'rb'),'application/pdf'))]
    response = requests.post(
        url = uploadURL,
        files = files,
        headers = headers,
        data={},
        verify=False
        )
    print(response)


if __name__ == '__main__':
    script_directory = os.path.dirname(os.path.abspath(__file__))
    filepath=os.path.join(script_directory, "./wiki/capella-docs-pdf/Using-Capella.pdf")
    print(os.path.exists(filepath))
    with open(filepath, 'rb') as file:
        uploadDocuments(file=file)
    # get_access_token_using_rest_api()
