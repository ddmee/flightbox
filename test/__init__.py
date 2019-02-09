import sys
import os


repo_dir = os.path.dirname(__path__[0])
src_dir = os.path.join(repo_dir, "src")
sys.path.insert(1, repo_dir)
sys.path.insert(1, src_dir)
