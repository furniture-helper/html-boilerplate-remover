import os
import pickle

from boilerplate_remover.Node import Node


def cache_anchor_tree(tree: Node) -> None:
    create_cache_directory()

    with open(".cache/anchor_tree.pkl", "wb") as f:
        pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_anchor_tree_from_cache() -> Node | None:
    create_cache_directory()

    try:
        with open(".cache/anchor_tree.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def create_cache_directory():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")
