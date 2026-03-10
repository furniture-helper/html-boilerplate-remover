import pickle

from Node import Node


def cache_anchor_tee(tree: Node) -> None:
    with open(".cache/anchor_tree.pkl", "wb") as f:
        pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_anchor_tree_from_cache() -> Node | None:
    try:
        with open(".cache/anchor_tree.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
