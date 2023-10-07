from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Person:
    id: int
    full_name: str
    known_for: str
    movies: Tuple[Optional[str], ...]


justin = Person(
    id=12111,
    full_name='Justin Timberlake',
    known_for='Acting',
    movies=('In Time', 'The Social Network')
)
