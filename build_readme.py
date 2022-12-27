import requests
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()


TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN", "")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        "<!-- {0} starts -->.*<!-- {0} ends -->".format(marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {0} starts -->{1}<!-- {0} ends -->".format(marker, chunk)
    return r.sub(chunk, content)


def fetch_blog_entries():
    entries = requests.get("https://dev.to/api/articles?username=jacobfrericks")
    return [
        {
            "title": entry["title"],
            "url": entry["url"],
            "cover_image": entry["cover_image"],
            "description": entry["description"]
        }
        for entry in entries.json()
    ]

def format_blog(entries):
    md_str = ""
    for entry in entries:
        if entry.get("cover_image"):
            md_str = md_str + "[![blog cover image]({cover_image})]({url})".format(**entry)
        md_str = md_str + """[{title}]({url})<br />{description}<br /><br />""".format(**entry)
    return md_str


def main():
    readme = root / "README.md"

    readme_contents = readme.open().read()

    entries = [fetch_blog_entries()[0]]
    entries_md = format_blog(entries)
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)

if __name__ == "__main__":
    main()