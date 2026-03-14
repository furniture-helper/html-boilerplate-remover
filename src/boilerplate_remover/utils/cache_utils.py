import os
import pickle

from boilerplate_remover.Node import Node


def cache_anchor_tree(tree: Node) -> None:
    create_cache_directory()

    with open(".cache/anchor_tree.pkl", "wb") as f:
        pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("Anchor tree cached successfully.")
    size = os.path.getsize(".cache/anchor_tree.pkl")
    print(f"Cache file size: {size} bytes")


def load_anchor_tree_from_cache(cache_path: str) -> Node | None:
    create_cache_directory()

    try:
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def create_cache_directory():
    if not os.path.exists(".cache"):
        os.makedirs(".cache")
