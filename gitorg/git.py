import subprocess
import os

# TODO: Move to libgit? sh?


def run(*args):
    return subprocess.call(
        ["git"] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def is_repo(path):
    return os.path.exists(f"{path}/.git")
