import os
import sys
from collections import OrderedDict

from common import read_lines_from_file, write_yaml, CATGEORIES, OSS_PROJECTS_DIR

YAML_SECTIONS = OrderedDict({
    "main-category": "### Main Category\n",
    "name": "### Name\n",
    "url": "### URL\n",
    "description": "### Description\n",
    "keywords": "### Keywords\n",
    "categories": "### Other Categories\n"
})

def extract_sections(issue_data):
    sections = {}
    keys = [k for k in YAML_SECTIONS.keys()]
    for k in keys:
        sections.setdefault(k, {'start': 0, 'end': 0})
    i = 0
    for line in issue_data:
        j = 0
        for field, pattern in YAML_SECTIONS.items():
            if line == pattern:
                sections[field]['start'] = i
                sections[keys[j-1]]['end'] = i
            j += 1
        i += 1
    sections[keys[len(keys)-1]]['end'] = len(issue_data)

    # extract lines from issue_data
    data = {}
    for sec, pos in sections.items():
        data[sec] = issue_data[pos['start']+1: pos['end']]
        data[sec] = [l.strip() for l in data[sec] if l != '\n']
    return data

def format_yaml(sections):
    category = CATGEORIES[sections['main-category'][0]]
    filename = "/".join([category, sections['name'][0]]) + ".yaml"
    categories = sections['categories'][0]
    categories = sections['main-category'] + categories.split(',')
    categories = list(set(categories))
    
    # clean no responses
    description = "\n".join([d for d in sections['description'] if d != '_No response_'])
    keywords = [k for k in sections['keywords'] if k != '_No response_']
    categories = [c for c in categories if c != '_No response_']
    
    # create yaml data
    data = {
        'name': sections['name'][0],
        'url': sections['url'][0],
        'description': description,
        'keywords': [k.lstrip('- ') for k in keywords],
        'categories': categories
    }
    return filename, data

def main(args):
    for a in args:
        if os.path.isfile(a):
            issue_data = read_lines_from_file(a)
            sections = extract_sections(issue_data)
            filename, data = format_yaml(sections)
            write_yaml(data, os.path.join(OSS_PROJECTS_DIR, filename))

if __name__ == '__main__':
    main(sys.argv[1:])