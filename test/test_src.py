# stdlib
import os
# 3rd party
import pytest
# local
from src.__main__ import fb_paths


def test_fb_paths():
    result = fb_paths("test/fb_path_samples")
    assert len(result) == 2
    # depends on the order of the files modified
    path1 = os.path.normpath("test/fb_path_samples/empty2.fb")
    path2 = os.path.normpath("test/fb_path_samples/empty.fb")
    assert [path1, path2] == result
