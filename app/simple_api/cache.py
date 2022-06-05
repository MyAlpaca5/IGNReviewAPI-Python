from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generic, TypeVar


Node = TypeVar('Node')
KeyType = TypeVar('KeyType', str, int)
ValueType = TypeVar('ValueType')


@dataclass
class Node:

    key: KeyType | None = None
    value: ValueType | None = None
    freq: int = 1
    prev: Node | None = None
    next: Node | None = None


@dataclass
class DLL:

    head: Node | None = None
    tail: Node | None = None

    def append(self, node: Node) -> None:
        # reset prev and next value
        node.prev, node.next = None, None

        if self.head is None:
            self.head = self.tail = node
            return

        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def delete(self, node: Node) -> bool:
        """
        delete a node

        Parameters:
            node: the node to be deleted

        Returns:
            bool: whether the DLL is empty after deletion
        """
        prev, next = node.prev, node.next

        if prev is not None:
            prev.next = next
        else:
            # node is head
            self.head = next

        if next is not None:
            next.prev = prev
        else:
            # node is tail
            self.tail = prev

        # reset prev and next value
        node.prev, node.next = None, None

        return self.head is None

    def delete_head(self) -> tuple[bool, Node]:
        """
        upper service is full, needed to remove the oldest element
        in order to append a new one. The oldest element is the head

        Parameters:
            None

        Returns:
            Tuple[bool, Node]: whether this DLL is empty after deletion and head deleted
        """

        if self.head is None:
            return None

        node = self.head
        is_empty = self.delete(node)
        return is_empty, node


@dataclass
class LFUCache(Generic[KeyType, ValueType]):

    capacity: int = 1
    least_freq: int = 1
    node_map: dict[KeyType, Node] = field(default_factory=dict)
    freq_map: dict[int, DLL] = field(default_factory=lambda: defaultdict(DLL))

    def __post_init__(self):
        if self.capacity <= 0:
            self.capacity = 1

    def get(self, key: KeyType) -> ValueType:
        if key not in self.node_map:
            return None

        node = self.node_map[key]
        freq = node.freq

        is_empty = self.freq_map[freq].delete(node)
        if is_empty:
            # no more element has this frequency
            self.freq_map.pop(freq)
            if freq == self.least_freq:
                self.least_freq = freq + 1

        node.freq += 1
        self.freq_map[node.freq].append(node)

        # print("get", key, "freq", node.freq, "map size", len(self.node_map))
        return node.value

    def put(self, key: KeyType, value: ValueType | None = None) -> None:
        if key in self.node_map:
            self.node_map[key].value = value
            return

        if self.capacity == len(self.node_map):
            # remove oldest element to insert a new one
            is_empty, deleted_node = self.freq_map[self.least_freq].delete_head()
            if is_empty:
                # no more element has this frequency
                self.freq_map.pop(self.least_freq)
            self.node_map.pop(deleted_node.key)

        node = Node(key=key, value=value)
        self.node_map[key] = node
        self.least_freq = 1
        self.freq_map[1].append(node)
        # print("put first time", key)
