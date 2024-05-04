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