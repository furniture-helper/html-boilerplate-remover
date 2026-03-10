from typing import Optional

from bs4 import BeautifulSoup

from Node import Node


def build_tree(soup: BeautifulSoup) -> Node:
    return Node(None, soup.html)


def get_unique_tree(tree: Node, comparison_tree: Optional[Node]) -> Optional[Node]:
    if not comparison_tree:
        return tree

    if comparison_tree.is_unique():
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
