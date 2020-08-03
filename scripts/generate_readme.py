#!/usr/bin/env python
# usage: generate_readme.py
__author__ = "Susheel Varma"
__copyright__ = "Copyright (c) 2019-2020 Susheel Varma All Rights Reserved."
__email__ = "susheel.varma@hdruk.ac.uk"
__license__ = "MIT"

import yaml

OSS_PROJECTS_YAML="data/oss_projects.yml"

def read_yaml(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def read_file(filename):
    with open(filename, 'r') as file:
        doc = file.read()
    return doc

def format_content(projects):
    content = []
    categories = []
    for p in projects:
        categories.extend(p['categories'])
    categories = sorted(list(set(categories)))

    for category in categories:
        filtered_projects = [p for p in projects if category in p['categories']]
        content.append("### {category} ({count})".format(category=category.upper(),
                                                    count=len(filtered_projects)))
        for i, p in enumerate(filtered_projects):
            content.append("{i}. [{name}]({url})".format(i=i+1,
                                                    name=p['name'], url=p['url']))
        content.append("\n")
    return "\n".join(content)

def write_readme(projects, filename="README.md"):
    header = read_file("templates/header.md")
    footer = read_file("templates/footer.md")
    content = format_content(projects)

    with open(filename, 'w') as file:
        file.writelines(header.format(count=len(projects)))
        file.writelines(content)
        file.writelines(footer)

def main():
    projects = read_yaml(OSS_PROJECTS_YAML)
    write_readme(projects)

if __name__ == "__main__":
    main()