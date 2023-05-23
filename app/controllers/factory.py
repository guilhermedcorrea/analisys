from dataclasses import dataclass, asdict,field
from dataclasses import dataclass, asdict,field
from collections.abc import Sequence
from typing import Any

@dataclass
class Variaveis(Sequence):
    venda_id: int
    variavel: str
    _data = {}
    _index = 0
    _next_index = 0

    def __len__(self) -> int:
        return self._index

    def __getitem__(self, index) -> Any:
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value
        
    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        if self._next_index >= self._index:
            self._next_index = 0
            raise StopIteration
        value = self._data[self._next_index]
        self._next_index +=1
        return value

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}