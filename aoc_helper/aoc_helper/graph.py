from abc import abstractmethod
from typing import Any, Generic, Hashable, Iterator, Protocol, TypeVar

from typing_extensions import Self


class Weight(Protocol):
    @abstractmethod
    def __le__(self, other: Self) -> bool:
        pass

    @abstractmethod
    def __lt__(self, other: Self) -> bool:
        pass

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        pass


W = TypeVar("W", bound=Weight)  # weight for a weighted graph


class BaseNode(Generic[W]):
    has_unique = False

    def __hash__(self) -> int:
        return hash(self.unique())

    def unique(self) -> Hashable:
        raise NotImplementedError("Not implemented for base")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self.has_unique:
            return self.unique() == other.unique()
        else:
            return object.__eq__(self, other)

    def get_neighbors(self, reverse: bool = False) -> Iterator[Self]:
        # default implementation for weighted graphs
        for neighbor, _ in self.get_weighted_neighbors(reverse=reverse):
            yield neighbor

    def get_weighted_neighbors(self, reverse: bool = False) -> Iterator[tuple[Self, W]]:
        raise NotImplementedError("Not implemented for base")


class ExplicitNode(BaseNode):
    def __init__(self, idx: int, all_nodes: list["ExplicitNode"]):
        self.idx = idx
        self.incoming: list[tuple[int, W]] = []
        self.outgoing: list[tuple[int, W]] = []
        self.all_nodes = all_nodes

    def add_arrow(self, target: int, distance=1):
        self.outgoing.append((target, distance))
        self.all_nodes[target].incoming.append((self.idx, distance))

    def unique(self) -> int:
        return self.idx

    def get_weighted_neighbors(
        self, reverse: bool = False
    ) -> Iterator[tuple["ExplicitNode", W]]:
        source = self.incoming if reverse else self.outgoing

        for n_idx, distance in source:
            yield self.all_nodes[n_idx], distance
