from abc import abstractmethod
from typing import Generic, Iterator, Protocol, TypeVar
from typing_extensions import Self


class Weight(Protocol):
    @abstractmethod
    def __le__(self, other: Self) -> bool:
        pass

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        pass


W = TypeVar("W", bound=Weight)  # weight for a weighted graph


class BaseNode(Generic[W]):
    def __hash__(self) -> int:
        raise NotImplementedError("Not implemented for base")

    def get_neighbors(self, reverse: bool = False) -> Iterator[Self]:
        # default implementation for weighted graphs
        for neighbor, _ in self.get_weighted_neighbors(reverse=reverse):
            yield neighbor

    def get_weighted_neighbors(self, reverse: bool = False) -> Iterator[tuple[Self, W]]:
        raise NotImplementedError("Not implemented for base")
