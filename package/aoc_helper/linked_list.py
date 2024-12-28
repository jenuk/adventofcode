from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class LinkedNode(Generic[T]):
    """
    A node in a (double) linked list
    """

    # TODO: this is missing a manager class, currently empty lists can't be displayed

    def __init__(
        self,
        value: T,
        prev: "LinkedNode[T] | None" = None,
        forw: "LinkedNode[T] | None" = None,
    ):
        self.value = value
        self.prev = prev
        self.forw = forw

    def insert(self, value: T) -> "LinkedNode[T]":
        new_node = LinkedNode(value, prev=self, forw=self.forw)
        if self.forw is not None:
            self.forw.prev = new_node
        self.forw = new_node
        return self.forw

    def __iter__(self) -> "Iterator[LinkedNode[T]]":
        curr = self
        while curr is not None:
            yield curr
            curr = curr.forw

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __str__(self) -> str:
        return " -> ".join(map(lambda x: str(x.value), self))

    def reversed(self):
        curr = self
        while curr is not None:
            yield curr
            curr = curr.prev
