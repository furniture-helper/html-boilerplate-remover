from typing import Optional

from bs4 import BeautifulSoup

from boilerplate_remover.Node import Node
from boilerplate_remover.utils.cache_utils import load_anchor_tree_from_cache, cache_anchor_tree
from boilerplate_remover.utils.file_utils import get_all_files_in_directory, read_file_to_string
from boilerplate_remover.utils.preprocessing_utils import clean_soup


def generate_base_tree():
    base_html = "<html></html>"
    base_soup = BeautifulSoup(base_html, 'lxml')
    base_tree = Node(None, base_soup.html)
    return base_tree


def generate_anchor_tree(directory: str) -> Node:
    base_tree = generate_base_tree()

    data_files = get_all_files_in_directory(directory)
    for file_path in data_files:
        print(f"Reading {file_path}...")
        content = read_file_to_string(file_path)
        soup = BeautifulSoup(content, 'lxml')
        clean_soup(soup)

        tree = build_tree(soup)
        base_tree.merge_with(tree)

    result_tree = base_tree.copy_without_children()
    for child in base_tree.children:
        child = child.trim()
        result_tree.children.append(child)

    return result_tree


def get_anchor_tree(cache_path: str) -> Node:
    anchor_tree = load_anchor_tree_from_cache(cache_path)
    if not anchor_tree:
        anchor_tree = generate_anchor_tree("data")
        cache_anchor_tree(anchor_tree)
    return anchor_tree


def build_tree(soup: BeautifulSoup) -> Node:
    return Node(None, soup.html)


def get_unique_tree(tree: Node, comparison_tree: Optional[Node]) -> Optional[Node]:
    if not comparison_tree:
        return tree

    if comparison_tree.is_unique():
        return tree

    text = (tree.text or "").lower()
    if tree.is_leaf_node() and any(term in text for term in ("404", "stock", "not found")):
        return tree

    unique_node = tree.copy_without_children()
    for child in tree.children:

        matching_comparison_child = None
        for comparison_child in comparison_tree.children:
            if child.matches(comparison_child):
                matching_comparison_child = comparison_child
                break

        unique_child = get_unique_tree(child, matching_comparison_child)
        if unique_child and unique_child.is_unique():  # TODO: Can i remove this?
            unique_node.children.append(unique_child)

    return unique_node if unique_node.children else None
