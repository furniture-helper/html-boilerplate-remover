from bs4 import BeautifulSoup

from Node import Node
from utils.cache_utils import load_anchor_tree_from_cache, cache_anchor_tee
from utils.file_utils import read_file_to_string, write_string_to_file, get_all_files_in_directory
from utils.preprocessing_utils import clean_soup
from utils.tree_utils import get_unique_tree, build_tree


def generate_anchor_tree() -> Node:
    base_html = "<html></html>"
    base_soup = BeautifulSoup(base_html, 'lxml')
    base_tree = Node(None, base_soup.html)

    data_files = get_all_files_in_directory("data")
    for file_path in data_files:
        print(f"Reading {file_path}...")
        content = read_file_to_string(file_path)
        soup = BeautifulSoup(content, 'lxml')
        clean_soup(soup)

        tree = build_tree(soup)
        base_tree.merge_with(tree)

    return base_tree


def generate_unique_trees(base_tree: Node) -> None:
    data_files = get_all_files_in_directory("data")
    for file_path in data_files:
        print(f"Generating unique tree for {file_path}...")
        content = read_file_to_string(file_path)
        soup = BeautifulSoup(content, 'lxml')
        clean_soup(soup)

        tree = build_tree(soup)

        unique_tree = get_unique_tree(tree, base_tree)

        generated_html = unique_tree.to_html()
        output_file_path = file_path.replace("data", "output").replace(".html", "_unique.html")
        write_string_to_file(output_file_path, generated_html)


anchor_tree = load_anchor_tree_from_cache()
if not anchor_tree:
    print("Generating anchor tree...")
    anchor_tree = generate_anchor_tree()
    cache_anchor_tee(anchor_tree)

generate_unique_trees(anchor_tree)
