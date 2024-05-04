import pathlib
import re
import os
import build_portfolio
import build_blog

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


def build():
    readme = root / "README.md"
    readme_contents = readme.open().read()

    # BLOG
    blog_md = build_blog.build()
    rewritten = replace_chunk(readme_contents, "blog", blog_md)

    # PORTFOLIO
    portfolio_md = build_portfolio.build()

    rewritten = replace_chunk(rewritten, "portfolio", portfolio_md)

    readme.open("w").write(rewritten)
    return rewritten

def main():
    build()

if __name__ == "__main__":
    main()