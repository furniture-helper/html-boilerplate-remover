from bs4 import BeautifulSoup

from boilerplate_remover.Node import Node
from boilerplate_remover.utils.file_utils import read_file_to_string
from boilerplate_remover.utils.preprocessing_utils import clean_soup
from boilerplate_remover.utils.tree_utils import get_anchor_tree, build_tree, get_unique_tree


class BoilerplateRemover:

    def __init__(self, cache_path: str = ".cache/anchor_tree.pkl") -> None:
        self.anchor_tree: Node = get_anchor_tree(cache_path)

    def get_minimized_tree(self, file_path: str) -> Node:
        content = read_file_to_string(file_path)
        return self.get_minimized_tree_from_string(content)

    def get_minimized_tree_from_string(self, html_content: str) -> Node:
        soup = BeautifulSoup(html_content, 'lxml')
        clean_soup(soup)
        tree = build_tree(soup)
        unique_tree = get_unique_tree(tree, self.anchor_tree)
        if unique_tree is None:
            return generate_base_tree()

        return unique_tree
