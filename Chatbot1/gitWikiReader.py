from github import Auth
from github import Github
from git import Repo
import requests
import base64
from requests.auth import HTTPBasicAuth
import os
import shutil

def get_wiki_page_using_api(owner, repo, page, token):
    url = f'https://api.github.com/repos/prem-mukherji/learn-terraform.wiki'
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # The content will be in the 'content' field
    else:
        return None
    
def get_wiki_page_using_pygithub(owner, repo, page, token):
    g = Github(token)

    # Get the contents of the wiki repository (assumes wiki is a separate repo)
    wiki_repo_name = f"{owner}/{repo}" + ".wiki"
    wiki_repo = g.get_repo(wiki_repo_name)

    # List all wiki pages (typically stored in the "pages" directory)
    contents = wiki_repo.get_contents("")

    for content_file in contents:
        if content_file.path.endswith(".md"):  # Assuming markdown files
            file_content = wiki_repo.get_contents(content_file.path)
            print(file_content.path)
            print(base64.b64decode(file_content.content).decode("utf-8"))


def get_wiki_page_using_api_2(owner, repo, page, token):
    wiki_page_url = f'https://raw.githubusercontent.com/wiki/{owner}/{repo}/{page}.md'
    response = requests.get(wiki_page_url, auth=HTTPBasicAuth('prem-mukherji', token))
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch {page}: {response.status_code}")
        return None


def get_wiki_by_cloning(owner, repoName, page, token):
    g = Github(token)
    repo = g.get_repo(f"{owner}/{repoName}")
    # wiki_url = f'https://github.com/{owner}/{repoName}.wiki.git'
    wiki_url = f'git@github.com:{owner}/{repoName}.wiki.git'
    local_path = f'./wiki/{repoName}'
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    Repo.clone_from(wiki_url, local_path)



_token = ""
_owner = 'Maersk-Global'
_repo = 'admiral'
_page = 'home'  # E.g., 'Home'

content = get_wiki_by_cloning(_owner, _repo, _page, _token)

if content:
    print(content['content'])
else:
    print("Failed to fetch wiki page content.")