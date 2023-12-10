from abc import abstractmethod
from typing import Generic, Iterator, Protocol, Self, TypeVar


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
        raise NotImplementedError("Not implemented for base")

    def get_weighted_neighbors(self, reverse: bool = False) -> Iterator[tuple[Self, W]]:
        raise NotImplementedError("Not implemented for base")
