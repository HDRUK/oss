#!/usr/bin/env python
# usage: generate_readme.py
__author__ = "Susheel Varma"
__copyright__ = "Copyright (c) 2019-2020 Susheel Varma All Rights Reserved."
__email__ = "susheel.varma@hdruk.ac.uk"
__license__ = "MIT"

import os
import json
import yaml
import subprocess
import statistics
from github import Github

OSS_PROJECTS_YAML = "data/oss_projects.yml"
GITHUB_AUTH_TOKEN = os.environ.get('GITHUB_AUTH_TOKEN', 'b585237c92e2296a2b89ab8bf8b07055f3e3bc91')

g = Github(GITHUB_AUTH_TOKEN)

def read_yaml(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(data, filename):
    with open(filename, 'w') as file:
        docs = yaml.dump(data, file, sort_keys=False)

def read_file(filename):
    with open(filename, 'r') as file:
        doc = file.read()
    return doc

def format_content(projects):
    CATEGORY_TEMPLATE = "### {category} ({count})"
    CONTENT_TEMPLATE = "{i}. [{name}]({url}) ![GitHub stars](https://img.shields.io/github/stars/{gh_repo}?style=flat-square) ![Criticality Score](https://img.shields.io/badge/criticality--score-{score}-yellowgreen?style=flat-square)"
    content = []
    categories = []
    for p in projects:
        categories.extend(p['categories'])
    categories = sorted(list(set(categories)))

    for p in projects:
        if p['url'].startswith("https://github.com/"):
            url = p['url'].split("https://github.com/")
            p['gh_repo'] = url[1]

    for category in categories:
        filtered_projects = [p for p in projects if category in p['categories']]
        content.append(CATEGORY_TEMPLATE.format(category=category.upper(),
                                                count=len(filtered_projects)))
        for i, p in enumerate(filtered_projects):
            content.append(CONTENT_TEMPLATE.format(i=i+1,
                                                name=p['name'], url=p['url'],
                                                gh_repo=p['gh_repo'],
                                                score=p.get('criticality_score', 0.0)))
        content.append("\n")
    return "\n".join(content)

def write_readme(projects, filename="README.md"):
    header = read_file("templates/header.md")
    footer = read_file("templates/footer.md")
    content = format_content(projects)

    criticality_scores = [p.get('criticality_score', 0.0) for p in projects]
    mean_criticality_score = round(statistics.mean(criticality_scores), 5)

    with open(filename, 'w') as file:
        file.writelines(header.format(count=len(projects), score=mean_criticality_score))
        file.writelines(content)
        file.writelines(footer)

def get_repo_info(repo_url, categories=None, keywords=None):
    if categories is None: categories = []
    if keywords is None: keywords = []
    # Get views - repo.get_views_traffic()
    # Get clones - repo.get_clones_traffic()
    repo = g.get_repo(repo_url.replace("https://github.com/", ""))
    data = {
        'name': repo.name,
        'url': "https://github.com/" + repo.full_name,
        'description': repo.description if repo.description is not None else "",
        'keywords': repo.get_topics() if repo.get_topics() else keywords,
        'categories': categories,
        'stars': repo.stargazers_count,
        'forks': repo.forks,
    }
    return data

def get_criticality_score(url):
    env = os.environ.copy()
    env['GITHUB_AUTH_TOKEN'] = GITHUB_AUTH_TOKEN
    cmd = subprocess.Popen("criticality_score --format json --repo {}".format(url),
                            shell=True,
                            stdin=None,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
    cmd.wait()
    out, err = cmd.communicate()
    out = json.loads(out)
    return out

def get_criticality_scores(projects):
    num_projects = len(projects)
    for i, p in enumerate(projects):
        repo_info = get_repo_info(p['url'], p['categories'], p['keywords'])
        p.update(repo_info)
        print("Calculating criticality-score (%s/%s) %s" %(i+1, num_projects, repo_info['url']))
        scores = get_criticality_score(p['url'])
        p.update(scores)
    return projects

def check_for_duplicates(projects):
    return [i for n, i in enumerate(projects) if i not in projects[n + 1:]]

def main():
    projects = read_yaml(OSS_PROJECTS_YAML)
    projects = check_for_duplicates(projects)
    projects = get_criticality_scores(projects)
    write_yaml(projects, 'data/oss_projects.yml')
    write_readme(projects)

if __name__ == "__main__":
    main()