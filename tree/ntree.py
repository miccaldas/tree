#!/usr/bin/python3.10
import os
import pathlib
import sys

import isort
import snoop
from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


class DevNull:
    def write(self, msg):
        pass


sys.stderr = DevNull()

# @snoop
def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold #5E8B7E]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "#B2B8A3")
            text_filename.highlight_regex(r"\..*$", "bold #F4C7AB")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            # text_filename.append(f" ({decimal(file_size)})", "#A7C4BC")
            icon = "" if path.suffix == ".py" else ""
            tree.add(text_filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="#D8B384",
    )
    walk_directory(pathlib.Path(directory), tree)
    print(tree)
