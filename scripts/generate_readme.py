import sys
import statistics

from common import (
    CATGEORIES,
    OSS_PROJECTS_DIR,
    PROJECT_YAMLS,
    read_yaml,
    write_yaml,
    read_file,
)


def format_content(projects):
    CATEGORY_TEMPLATE = "### {category} ({count})"
    CONTENT_TEMPLATE = "{i}. [{name}]({url}): {description} ![GitHub stars](https://img.shields.io/github/stars/{gh_repo}?style=flat-square) ![Criticality Score](https://img.shields.io/badge/criticality--score-{score}-yellowgreen?style=flat-square)"
    content = []
    categories = []
    for p in projects:
        categories.extend(p["categories"])
    categories = sorted(list(set(categories)))

    for p in projects:
        if p["url"].startswith("https://github.com/"):
            url = p["url"].split("https://github.com/")
            p["gh_repo"] = url[1]

    for category in categories:
        filtered_projects = [p for p in projects if category in p["categories"]]
        filtered_projects = sorted(filtered_projects, key=lambda x: x["name"])
        content.append(
            CATEGORY_TEMPLATE.format(
                category=category.upper(), count=len(filtered_projects)
            )
        )
        for i, p in enumerate(filtered_projects):
            content.append(
                CONTENT_TEMPLATE.format(
                    i=i + 1,
                    name=p["name"],
                    url=p["url"],
                    description=p["description"],
                    gh_repo=p.get("gh_repo", ""),
                    score=p.get("github", {}).get("criticality_score", 0.0),
                )
            )
        content.append("\n")
    return "\n".join(content)


def write_readme(projects, filename="README.md"):
    header = read_file("templates/header.md")
    footer = read_file("templates/footer.md")
    content = format_content(projects)

    criticality_scores = [
        p.get("github", {}).get("criticality_score", 0.0) for p in projects
    ]
    mean_criticality_score = round(statistics.mean(criticality_scores), 5)

    with open(filename, "w") as file:
        file.writelines(
            header.format(count=len(projects), score=mean_criticality_score)
        )
        file.writelines(content)
        file.writelines(footer)


def main(args):
    # Filter project YAMLS with supplied args (if any)
    projects = []
    if len(args):
        args = [a.replace(OSS_PROJECTS_DIR, "") for a in args]
        projects = [p for p in PROJECT_YAMLS for arg in args if p.endswith(arg)]
    else:
        projects = PROJECT_YAMLS

    data = []
    for oss_project_yaml in projects:
        data.append(read_yaml(oss_project_yaml))

    write_readme(data)


if __name__ == "__main__":
    main(sys.argv[1:])
