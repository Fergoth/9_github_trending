import requests
import datetime


def get_week_ago():
    week = datetime.timedelta(days=7)
    week_ago = datetime.datetime.today() - week
    return week_ago.strftime('%Y-%m-%d')


def get_trending_repositories(top_size=20):
    date = get_week_ago()
    params = {'q': 'created:>{}'.format(date),
              'sort': 'stars',
              'per_page': top_size}
    url = "https://api.github.com/search/repositories"
    response = requests.get(url, params=params)
    return response.json()['items']


def get_open_issues_amount(repositories):
    for repo in repositories:
        url = repo['issues_url'].strip('{/number}')
        request = requests.get(url)
        issue_info = request.json()
        repo['open_issues_info'] = issue_info


def print_repo_info(repo):
    print('Name : {}'.format(repo['name']))
    print('Description : {}'.format(repo['description']))
    print('Stars : {}'.format(repo['stargazers_count']))
    print('Issues count : {}'.format(repo['open_issues']))
    print('Issues urls: ')
    for issue in repo['open_issues_info']:
        print('    {}'.format(issue['html_url']))


def print_repositories_info(repositories):
    print('Репозитории с наибольшим количеством звёзд за неделю')
    for repo in repositories:
        print_repo_info(repo)
        print()


if __name__ == '__main__':
    trending_repositories = get_trending_repositories()
    get_open_issues_amount(trending_repositories)
    print_repositories_info(trending_repositories)
