import sys
import getpass
from github import Github, PaginatedList, Repository

def get_is_removal():
  try:
    return sys.argv[1] == 'remove'
  except:
    return False

is_removal = get_is_removal()
username = input('👋 Input your GitHub username: ')
password = getpass.getpass('🔐 Input your GitHub password: ')
tag = '#BlackLivesMatter'

github_api = Github(username, password)
github_user = github_api.get_user()

all_repos = PaginatedList.PaginatedList(
  Repository.Repository,
  github_user._requester,
  f'{github_user.url}/repos',
  dict(
    affiliation='owner',
    visibility='public',
  ),
)

def print_separator():
  print(u'\u2500' * 15)

def if_none_to_string(string, fallback = ''):
  return str(string or fallback)

repo_count = 0
for repo in all_repos:
  print_separator()
  print(f'🏴 {repo.full_name}')
  print(if_none_to_string(repo.description, 'None'))

  description_with_tag = if_none_to_string(repo.description).strip()

  if is_removal:
    if description_with_tag.endswith(tag):
      description_without_tag = description_with_tag.replace(tag, '')
      try:
        repo.edit(description=description_without_tag)
        print(f'➡️ {description_without_tag}')
        print('❗️ Removed tag')
        repo_count += 1
      except:
        print('❌ Error occurred while removing tag from description')
      continue

  if tag in description_with_tag:
    print('👍 Already tagged. Passing')
  else:
    if description_with_tag:
      description_with_tag += f' {tag}'
    else:
      description_with_tag = tag
    try:
      repo.edit(description=description_with_tag)
      print(f'➡️ {description_with_tag}')
      repo_count += 1
    except:
      print('❌ Error occurred while editing project description')

print_separator()

if is_removal:
  print(f'✅ Finished removing tag #BlackLivesMatter from {repo_count} repos')
else:
  print(f'✅ Finished adding tag #BlackLivesMatter to {repo_count} repos')
