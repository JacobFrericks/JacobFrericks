from distutils.command.build import build
import unittest
import build_portfolio
import json
from unittest.mock import MagicMock, patch, Mock
from datetime import date
from data.fake_github import FakeUser


class Test(unittest.TestCase):

  @patch('requests.get')
  @patch('github.Github.get_user')
  def test_fetch_blog_entries(self, mock_get_user, mock_requests):
    mock_get_user.return_value = FakeUser()


    # mock_requests.return_value = "This is a readme or a portfolio pic"

    # expected = [
    #   {
    #     "title": "this is the title of my blog",
    #     "description": "my blog is awesome and heres why you should...",
    #     "url": "https://dev.to/jacobfrericks/thebestblogever",
    #     "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
    #   },
    #   {
    #     "title": "this is the title of my blog #2",
    #     "description": "my blog is awesome and heres why you ALSO should...",
    #     "url": "https://dev.to/jacobfrericks/thebestblogever2",
    #     "cover_image": "https://www.imagegen.com/bestblogimage.jpg",
    #   }
    # ]

    # actual = build_portfolio.fetch_portfolio_entries()
    # print(json.dumps(actual))
    # print(json.dumps(expected))
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