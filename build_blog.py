import requests

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


def build():
    entries = [fetch_blog_entries()[0]]
    str_md = ""
    for entry in entries:
        if entry.get("cover_image"):
            str_md = str_md + "[![blog cover image]({cover_image})]({url})".format(**entry)
        str_md = str_md + """[{title}]({url})<br />{description}<br /><br />""".format(**entry)
    return str_md


if __name__ == "__main__":
    build()