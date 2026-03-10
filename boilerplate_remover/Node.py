from __future__ import annotations

from typing import Optional, List, Union

from bs4 import BeautifulSoup, Tag, PageElement

from boilerplate_remover.utils.html_utils import get_attribute, get_direct_text


class Node:

    def __init__(self, parent: Optional['Node'], element: Union[Tag, BeautifulSoup, PageElement]) -> None:
        self.parent: Optional['Node'] = parent
        self.children: List[Node] = []
        self.count: int = 1

        self.html_tag: str = getattr(element, 'name', None)

        self.id: Optional[str] = get_attribute(element, 'id')
        self.classes: List[str] = get_attribute(element, 'class') or []
        self.src: Optional[str] = get_attribute(element, 'src', replace_common_values=False)

        self.text = get_direct_text(element)
        self.populate_children(element)

    def populate_children(self, element) -> None:
        for child in element.children:
            child_name: Optional[str] = getattr(child, 'name', None)
            if child_name is None:
                continue

            matching_child_node_found: bool = False
            for child_node in self.children:
                child_name: Optional[str] = getattr(child, 'name', None)
                if child_name is None:
                    continue

                if child_node.matches(child):
                    matching_child_node_found = True
                    child_node.count += 1

                    new_node = Node(self, child)
                    child_node.merge_with(new_node)
                    break

            if not matching_child_node_found:
                new_node = Node(self, child)
                self.children.append(new_node)

    def matches(self, other: Node) -> bool:
        if self.html_tag != other.html_tag:
            return False

        if self.id and other.id and self.id != other.id:
            return False

        if set(self.classes) != set(other.classes):
            return False

        if self.src and other.src and self.src != other.src:
            return False

        if self.text and other.text and self.text != other.text:
            return False

        return True

    def merge_with(self, other: Node) -> None:
        for other_child in other.children:
            matching_child_node_found: bool = False
            for child_node in self.children:
                if child_node.matches(other_child):
                    matching_child_node_found = True
                    child_node.count += other_child.count
                    child_node.merge_with(other_child)
                    break

            if not matching_child_node_found:
                other_child.parent = self
                self.children.append(other_child)

    def is_unique(self) -> bool:
        if self.is_leaf_node():
            return self.count <= 5
        elif self.children:
            return all(child.is_unique() for child in self.children)
        else:
            return False

    def is_leaf_node(self) -> bool:
        return not self.children

    def __str__(self) -> str:
        result = f"{self.html_tag} (count: {self.count})"

        if self.id:
            result += f" [id: {self.id}]"

        if self.classes:
            result += f" [classes: {' '.join(self.classes)}]"

        if self.src:
            result += f" [src: {self.src}]"

        if self.text:
            result += f" [text: {self.text}]"

        for child in self.children:
            child_str = str(child)
            child_lines = child_str.splitlines()
            indented_child_str = "\n".join("  " + line for line in child_lines)
            result += "\n" + indented_child_str

        return result

    def to_html(self) -> str:
        if self.html_tag is None:
            return ""

        attrs: List[str] = []

        if self.id:
            attrs.append(f'id="{self.id}"')

        if self.classes:
            attrs.append(f'class="{" ".join(self.classes)}"')

        if self.src:
            attrs.append(f'src="{self.src}"')

        attr_str = " " + " ".join(attrs) if attrs else ""
        opening_tag = f"<{self.html_tag}{attr_str}>"
        closing_tag = f"</{self.html_tag}>"

        children_html = "".join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}{self.text}{closing_tag}"

    def copy_without_children(self) -> Node:
        copy_node = Node(None, BeautifulSoup(f"<{self.html_tag}></{self.html_tag}>", 'lxml').find(self.html_tag))
        copy_node.id = self.id
        copy_node.classes = self.classes.copy()
        copy_node.src = self.src
        copy_node.text = self.text
        return copy_node

    # Pickle helpers: avoid serializing bs4 objects and parent cycles
    def __getstate__(self):
        state = self.__dict__.copy()
        # remove or replace non-serializable / cyclic references
        state['parent'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # fix parent pointers for children
        for child in self.children:
            child.parent = self
