import subprocess

# TODO: Move to libgit? sh?


def run(*args):
    return subprocess.call(
        ["git"] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
