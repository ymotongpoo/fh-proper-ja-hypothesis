# Copyright 2022 Yoshi Yamaguchi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from hypothesis import event, given, settings
from hypothesis.strategies import (
    DrawFn,
    binary,
    booleans,
    builds,
    characters,
    composite,
    integers,
    lists,
    one_of,
    sampled_from,
    text,
    tuples,
)


## START:dupes_gen
@composite
def keys(draw: DrawFn) -> int:
    fixed = sampled_from(range(1, 11))
    return draw(one_of(fixed, integers()))


@composite
def vals(draw: DrawFn) -> Any:
    return draw(booleans() | characters() | integers() | text())


## END:dupes_gen

## START:dupes
# In order to print the statistics from `event`, you need to specify
# Hypothesis' statistics option: `--hypothesis-show-statistics`.
# See details here: https://hypothesis.readthedocs.io/en/latest/details.html#statistics
@given(lists(tuples(keys(), vals())))
def test_dupes(kv: list[tuple[int, Any]]) -> None:
    m = {k: v for k, v in kv}
    [m[k] for k, _ in kv]  # I want non existing key to be crashed
    range_min, range_max = to_range(5, len(kv) - len(ukey(kv)))
    event(f"dupes: {range_min}-{range_max}")


## END:dupes

## START:collect1
# TODO: confirm if there's some function that corresponds to Erlang's is_binary/1.
@given(binary())
def test_collect1(b: bytes) -> None:
    size = len(b)
    event(f"size: {size}")


## END:collect1

## START:collect2
# TODO: confirm if there's some function that corresponds to Erlang's is_binary/1.
@given(binary())
def test_collect2(b: bytes) -> None:
    range_min, range_max = to_range(10, len(b))
    event(f"size: {range_min}-{range_max}")


## END:collect2

## START:to_range
def to_range(m: int, n: int) -> tuple[int, int]:
    base = n // m
    return (base * m, (base + 1) * m)


def ukey(lt: list[tuple[int, Any]]) -> Dict[int, list[Any]]:
    """ukeysort sorts list of tuples based on nth element in tuple and removed
    duplicated elements from it.

    Args:
        lt (List[Tuple])): List of tuples
    """
    ret = defaultdict(list)
    for e in lt:
        ret[e[0]].append(e[1])
    ret = dict(ret)
    return ret


## END:to_range

## START:aggregate
class Suit(Enum):
    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4


@dataclass(frozen=True)
class Card:
    suit: Suit
    num: int

    def __str__(self):
        return f"Card({self.suit}, {self.num})"

    def __repr__(self):
        return f"Card({self.suit}, {self.num})"


@composite
def card(draw: DrawFn) -> Card:
    s = draw(sampled_from(Suit))
    n = draw(sampled_from(range(1, 14)))
    return Card(s, n)


@composite
def hand(draw: DrawFn) -> list[Card]:
    return draw(lists(card(), min_size=5, max_size=5))


@given(hand())
def test_aggregate(h: list[Card]) -> None:
    # converting to str is the work around for events to handle
    # lists/tuples.
    # https://github.com/HypothesisWorks/hypothesis/issues/3393
    s = str(h)
    event(s)


## END:aggregate

## START:char_classes
@given(text())
def test_escape(s: str):
    c = classes(s)
    cs = str(c)
    event(cs)


def classes(s: str) -> list[tuple[str, tuple[int, int]]]:
    l = letters(s)
    n = numbers(s)
    p = punctuation(s)
    o = len(s) - (l + n + p)
    return [
        ("letters", to_range(5, l)),
        ("numbers", to_range(5, n)),
        ("punctuation", to_range(5, p)),
        ("others", to_range(5, o)),
    ]


def letters(s: str) -> int:
    f = filter(lambda c: "A" <= c <= "Z" or "a" <= c <= "z", s)
    return len(list(f))


def numbers(s: str) -> int:
    f = filter(lambda c: "0" <= c <= "9", s)
    return len(list(f))


def punctuation(s: str) -> int:
    f = filter(lambda c: c in """.,;:'"-""", s)
    return len(list(f))


## END:char_classes


## START:resize
@given(binary(max_size=150))
def test_resize(b: bytes) -> None:
    t = to_range(10, len(b))
    event(str(t))


## END:resize


## START:profile1
@dataclass
class Profile:
    name: str
    age: int
    bio: str

    def __eq__(self, other):
        return (
            self.name == other.name and self.age == other.age and self.bio == other.bio
        )


@given(
    builds(
        Profile,
        text(max_size=10),
        integers(min_value=1, max_value=150),
        text(max_size=350),
    )
)
@settings(max_examples=100)
def test_profile1(p: Profile) -> None:
    name_len = to_range(10, len(p.name))
    bio_len = to_range(300, len(p.bio))
    event(f"(name: {name_len}, bio: {bio_len})")


## END:profile1


## START:profile2
# TODO: find better ways to set two variables proportional.
# https://stackoverflow.com/q/72863388/515508
@composite
def profiles(draw: DrawFn) -> Profile:
    name = draw(text(max_size=10))
    name_len = len(name)
    age = draw(integers(min_value=1, max_value=150))
    bio_len = 35 * name_len
    bio = draw(text(min_size=bio_len, max_size=bio_len))
    return Profile(name, age, bio)


@given(profiles())
@settings(max_examples=100)
def test_profile2(p: Profile) -> None:
    name_len = to_range(10, len(p.name))
    bio_len = to_range(300, len(p.bio))
    event(f"(name: {name_len}, bio: {bio_len})")


## END:profile2
