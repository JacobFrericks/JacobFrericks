import requests
import pathlib
import os
from github import Github

g = Github(os.getenv("PERSONAL_ACCESS_TOKEN", ""))

root = pathlib.Path(__file__).parent.resolve()

topic_filter = "portfolio"

def fetch_portfolio_entries():
    repos = []
    for repo in g.get_user().get_repos():
        if topic_filter in repo.topics:
            repos.append(repo)

    portfolios = []
    for repo in repos:
        readme=repo.get_contents("README.md").decoded_content.decode("utf-8")
        portfolios.append({
            "html_url": repo.html_url,
            "readme": f"{readme[:297]}...",
            "cover_image": f"{repo.html_url}/blob/master/portfolio_pic.png"
        })
    return portfolios

def format_readme(readme, url):
    lines = []
    count = 0
    for line in readme.split('\n'):
      if line:
        if count == 0:
            # Remove '#'
            line = line.replace("# ", "")
            # Create a link to the project
            line = f"# [{line}]({url})"
        lines.append(line)
        count = count+1
      else:
        break
    return "\n".join(lines)


def build():
    portfolios = fetch_portfolio_entries()
    str_md = ""
    for proj in portfolios:
        if requests.get(proj.get("cover_image")).status_code != 404:
            cover_image = proj.get("cover_image")
            str_md = str_md + f"![portfolio cover image]({cover_image})"
        # print(proj.get("html_url"))
        # print(proj.get("readme"))
        readme = format_readme(proj.get("readme"), proj.get("html_url"))
        str_md = str_md + f"{readme}\n\n"

    return str_md

if __name__ == "__main__":
    build()