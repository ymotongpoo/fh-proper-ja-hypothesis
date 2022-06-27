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

from pickle import dumps, loads
from typing import Any

from hypothesis import given, settings
from hypothesis.strategies import characters, integers, lists, one_of, text

from . import biggest


##################
### Properties ###
##################
@given(lists(integers(min_value=0, max_value=100000)))
@settings(max_examples=100)
def test_biggest(l: list):
    assert biggest(l) == model_biggest(l)


@given(
    lists(integers(min_value=0, max_value=100000)),
    integers(min_value=0, max_value=100000),
)
@settings(max_examples=100)
def test_last(list, known_last):
    list.append(known_last)
    assert known_last == list[-1]


@given(lists(integers(min_value=0, max_value=100000)))
@settings(max_examples=100)
def test_sort(l: list):
    l.sort()
    assert is_ordered(l)


@given(lists(integers(min_value=0, max_value=100000)))
@settings(max_examples=100)
def test_same_size(l: list):
    original = l.copy()
    l.sort()
    assert len(original) == len(l)


@given(lists(integers(min_value=0, max_value=100000)))
@settings(max_examples=100)
def test_no_added(l: list):
    original = l.copy()
    l.sort()
    for n in l:
        assert n in original


@given(lists(integers(min_value=0, max_value=100000)))
@settings(max_examples=100)
def test_no_remove(l: list):
    original = l.copy()
    l.sort()
    for n in original:
        assert n in l


@given(
    one_of(
        text(),
        lists(text()),
        characters(),
        lists(characters()),
        integers(min_value=-100000, max_value=100000),
        lists(integers(min_value=-100000, max_value=100000)),
    )
)
@settings(max_examples=100)
def test_symmetric(t: Any):
    assert t == decode(encode(t))


##############
### Helper ###
##############
def model_biggest(l: list) -> list:
    # because max is builtin function and can trust its stability
    # we can use it here without any tests.
    return max(l) if len(l) > 0 else l[-1:]


def is_ordered(l: list) -> bool:
    if len(l) < 2:
        return True
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True


def encode(t: Any) -> Any:
    return dumps(t)


def decode(t: Any) -> Any:
    return loads(t)
