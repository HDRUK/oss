import os
import yaml
from pathlib import Path

CATGEORIES = {
    "Applied Analytics": "applied-analytics",
    "BHF Data Science Centre": "bhf-dsc",
    "Bioinformatics": "bioinformatics",
    "Gateway": "gateway",
    "COVID-19": "covid-19",
    "National Phenomics Resource": "phenomics",
    "National Text Analytics": "text-analytics",
    "HDR UK": "hdruk",
    "Cohort Discovery": "cohort-discovery",
    "Better Care": "better-care",
    "Gateway (MVP)": "gateway-mvp",
    "Uncategorised": "uncategorised",
    "Training": "training",
    "ICODA": "icoda",
}

OSS_PROJECTS_DIR = "data/oss"
PROJECT_YAMLS = []
for (dirpath, dirnames, filenames) in os.walk(OSS_PROJECTS_DIR):
    for file in filenames:
        PROJECT_YAMLS.append(os.path.join(dirpath, file))


def read_yaml(filename):
    with open(filename, "r") as file:
        return yaml.safe_load(file)


def write_yaml(data, filename):
    directory = os.path.dirname(filename)
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as file:
        docs = yaml.dump(data, file, sort_keys=False)


def read_file(filename):
    with open(filename, "r") as file:
        doc = file.read()
    return doc

def read_lines_from_file(filename):
    with open(filename, "r") as file:
        doc = file.readlines()
    return doc
