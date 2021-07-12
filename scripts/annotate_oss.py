import os
import sys
import yaml
import json
from github import Github
import subprocess
import psutil
import ray

from common import OSS_PROJECTS_DIR, PROJECT_YAMLS, read_yaml, write_yaml

num_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_cpus)

GITHUB_AUTH_TOKEN = os.environ.get(
    "GITHUB_AUTH_TOKEN", ""
)
g = Github(GITHUB_AUTH_TOKEN)


def get_github_repo_url(repo_url):
    if not repo_url.startswith("https://github.com/"):
        return None
    url_paths = repo_url.split("https://github.com/")[1]
    org, repo = url_paths.split("/")[0:2]
    return "https://github.com/" + org + "/" + repo


def get_repo_info(repo_url):
    if not repo_url.startswith("https://github.com"):
        return None
    try:
        repo = g.get_repo(repo_url.replace("https://github.com/", ""))
    except:
        return None
    repo_meta = {
        "name": repo.name,
        "url": "https://github.com/" + repo.full_name,
        "description": repo.description if repo.description is not None else "",
        "keywords": repo.get_topics() if repo.get_topics() else "",
        "language": repo.language,
        "created_at": repo.created_at,
        "updated_at": repo.updated_at,
        "archived": repo.archived,
        "subscribers": repo.subscribers_count,
        "watchers": repo.watchers,
        "stars": repo.stargazers_count,
        "forks": repo.forks,
        "network": repo.network_count,
    }
    return repo_meta


def get_criticality_score(repo_url):
    if not repo_url.startswith("https://github.com"):
        return None
    env = os.environ.copy()
    env["GITHUB_AUTH_TOKEN"] = GITHUB_AUTH_TOKEN
    cmd = subprocess.Popen(
        "criticality_score --format json --repo {}".format(repo_url),
        shell=True,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    cmd.wait()
    out, err = cmd.communicate()
    out = json.loads(out)
    return out


@ray.remote
def annotate_oss(oss_project_yaml, i, len):
    print("{}/{}: {}".format(i, len, oss_project_yaml))
    data = read_yaml(oss_project_yaml)
    repo_url = get_github_repo_url(data["url"])
    if repo_url is None:
        write_yaml(data, oss_project_yaml)
        return

    # Get Repo metadata
    repo_meta = get_repo_info(repo_url)
    if repo_meta is not None:
        data.setdefault("github", {})
        data["github"].update(repo_meta)

    # Get Criticality Score
    try:
        criticality_score = get_criticality_score(repo_url)
        if criticality_score is not None:
            data.setdefault("github", {})
        data["github"].update(criticality_score)
    except:
        write_yaml(data, oss_project_yaml)
        return

    # Write YAML
    write_yaml(data, oss_project_yaml)
    return


def main(args):
    # Filter project YAMLS with supplied args (if any)
    projects = []
    if len(args):
        args = [a.replace(OSS_PROJECTS_DIR, "") for a in args]
        projects = [p for p in PROJECT_YAMLS for arg in args if p.endswith(arg)]
    else:
        projects = PROJECT_YAMLS

    # Annotate OSS
    futures = []
    for i, p in enumerate(projects):
        futures.append(annotate_oss.remote(p, i + 1, len(projects)))
    results = ray.get(futures)


if __name__ == "__main__":
    main(sys.argv[1:])
