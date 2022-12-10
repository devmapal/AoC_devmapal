from io import TextIOWrapper
from typing import Optional
from collections.abc import Set


class Node:
    def __init__(
        self,
        name: str,
        children=None,
        parent=None,
        size=0,
    ):
        self.name = name
        self.children = [] if children is None else children
        self.parent = parent
        self.size = size


class TreeBuilder:
    def __init__(self):
        self.root = Node(name="/")
        self._current_node = self.root
        self._a_file = None
        self._files = []
        self.directories = [self.root]

    def build(self, input: str):
        with open(input) as self._a_file:
            line = self._a_file.readline()
            while line:
                line = self.process_command(line)

        self.calculate_dir_sizes()

        return self

    def calculate_dir_sizes(self):
        for file in self._files:
            parent = file.parent
            while parent:
                parent.size += file.size
                parent = parent.parent

    def process_command(self, line: str):
        if line.startswith("$ cd"):
            return self.process_cd(line)
        elif line.startswith("$ ls"):
            return self.process_ls()

    def process_cd(self, line: str):
        directory = line[4:].strip()
        if directory == "/":
            self._current_node = self.root
        elif directory == "..":
            self._current_node = self._current_node.parent
        else:
            self._current_node = next(
                x for x in self._current_node.children if x.name == directory
            )

        return self._a_file.readline()

    def process_ls(self):
        line = self._a_file.readline()
        while line and not line.startswith("$"):
            if line.startswith("dir"):
                _, name = [elem.strip() for elem in line.split(" ")]
                directory = Node(name, parent=self._current_node)
                self.directories.append(directory)
                self._current_node.children.append(directory)
            else:
                size, name = [elem.strip() for elem in line.split(" ")]
                file = Node(name, size=int(size), parent=self._current_node)
                self._files.append(file)
                self._current_node.children.append(file)

            line = self._a_file.readline()

        return line


treeBuilder = TreeBuilder().build("input")
to_remove = treeBuilder.root.size - 40000000

dir_sizes = [directory.size for directory in treeBuilder.directories]
print(min([dir_size for dir_size in dir_sizes if dir_size >= to_remove]))
