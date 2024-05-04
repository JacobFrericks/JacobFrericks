from distutils.command.build import build
import unittest
import build_blog
import json
from unittest.mock import patch, Mock
from datetime import date


class Test(unittest.TestCase):

  @patch('requests.get')
  def test_fetch_blog_entries(self, mock_requests):
    mock_requests.return_value = Mock(status_code=201, json=lambda : [{
      "type_of": "article",
      "title": "this is the title of my blog",
      "description": "my blog is awesome and heres why you should...",
      "url": "https://dev.to/jacobfrericks/thebestblogever",
      "published_timestamp": "2000-01-01T01:01:01Z",
      "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
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
      "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
      "published_at": "2000-01-01T01:01:01Z",
      "last_comment_at": "2000-01-01T01:01:01Z",
      "reading_time_minutes": 5,
      "tag_list": [],
      "tags": "",
    }])

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

    actual = build_blog.fetch_blog_entries()
    print(json.dumps(actual))
    print(json.dumps(expected))
    self.assertEqual(actual, expected)

  @patch('build_blog.fetch_blog_entries')
  def test_format_blog(self, mock_fetch_blog_entries):
    mock_fetch_blog_entries.return_value = [
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

    expected = "[![blog cover image](https://www.imagegen.com/bestblogimage.jpg)](https://dev.to/jacobfrericks/thebestblogever)[this is the title of my blog](https://dev.to/jacobfrericks/thebestblogever)<br />my blog is awesome and heres why you should...<br /><br />"
    actual = build_blog.build()

    self.assertEqual(actual, expected)