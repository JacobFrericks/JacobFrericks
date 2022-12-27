from distutils.command.build import build
import unittest
import build_readme
import json
from unittest.mock import patch
from datetime import date


class Test(unittest.TestCase):
  def test_replace_chunk(self):
    content = """
<!-- blog starts -->
oldblog
<!-- blog ends -->
    """
    marker = "blog"
    chunk = "newblog"

    expected = """
<!-- blog starts -->
newblog
<!-- blog ends -->
    """
    actual = build_readme.replace_chunk(content, marker, chunk)

    self.assertEqual(actual, expected)

  @patch('requests.get')
  def test_fetch_blog_entries(self, mock_requests):
    mock_requests.return_value = [{
      "type_of": "article",
      "title": "this is the title of my blog",
      "description": "my blog is awesome and heres why you should...",
      "url": "https://dev.to/jacobfrericks/thebestblogever",
      "published_timestamp": "2000-01-01T01:01:01Z",
      "cover_image": "https://res.cloudinary.com/practicaldev/image/fetch/s--GhUvytVI--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://tr1.cbsistatic.com/hub/i/r/2017/04/06/6f6fb9b1-b297-464d-a0e0-48b366745fe2/resize/770x/e75cd06318a179e5041993a6a8034df6/dockersechero.jpg",
      "published_at": "2000-01-01T01:01:01Z",
      "last_comment_at": "2000-01-01T01:01:01Z",
      "reading_time_minutes": 5,
      "tag_list": [],
      "tags": "",
      },
      {
      "type_of": "article",
      "title": "this is the title of my blog #2",
      "description": "my blog is awesome and heres why you ALSO should...",
      "url": "https://dev.to/jacobfrericks/thebestblogever2",
      "published_timestamp": "2000-01-01T01:01:01Z",
      "cover_image": "https://res.cloudinary.com/practicaldev/image/fetch/s--GhUvytVI--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://tr1.cbsistatic.com/hub/i/r/2017/04/06/6f6fb9b1-b297-464d-a0e0-48b366745fe2/resize/770x/e75cd06318a179e5041993a6a8034df6/dockersechero.jpg",
      "published_at": "2000-01-01T01:01:01Z",
      "last_comment_at": "2000-01-01T01:01:01Z",
      "reading_time_minutes": 5,
      "tag_list": [],
      "tags": "",
    }]

    expected = [
      {
        "title": "this is the title of my blog",
        "description": "my blog is awesome and heres why you should...",
        "url": "https://dev.to/jacobfrericks/thebestblogever",
        "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
      },
      {
        "title": "this is the title of my blog #2",
        "description": "my blog is awesome and heres why you ALSO should...",
        "url": "https://dev.to/jacobfrericks/thebestblogever2",
        "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
      }
    ]
    actual = build_readme.fetch_blog_entries()

    self.assertEqual(actual, expected)


  def test_format_blog(self):
    entries = [
      {
        "title": "this is the title of my blog",
        "description": "my blog is awesome and heres why you should...",
        "url": "https://dev.to/jacobfrericks/thebestblogever",
        "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
      },
      {
        "title": "this is the title of my blog #2",
        "description": "my blog is awesome and heres why you ALSO should...",
        "url": "https://dev.to/jacobfrericks/thebestblogever2",
      }
    ]

    expected = "[![blog cover image](https://www.imagegen.com/bestblogimage.jpg)](https://dev.to/jacobfrericks/thebestblogever)[this is the title of my blog](https://dev.to/jacobfrericks/thebestblogever)<br />my blog is awesome and heres why you should...<br /><br />[this is the title of my blog #2](https://dev.to/jacobfrericks/thebestblogever2)<br />my blog is awesome and heres why you ALSO should...<br /><br />"
    actual = build_readme.format_blog(entries)

    self.assertEqual(actual, expected)