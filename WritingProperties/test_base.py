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

from hypothesis import given, settings
from hypothesis.strategies import integers, lists


@given(lists(integers(), min_size=1))
@settings(max_examples=100)
def test_biggest(l):
    c = l.copy()
    c.sort()
    assert biggest(l) == c[-1]


def biggest(l: list):
    match len(l):
        case 0:
            return l[-1:]
        case 1:
            return l[0]
        case _:
            head, tail = l[0], l[1:]
            return _biggest(tail, head)


def _biggest(x, y):
    if x == []:
        return y
    h, t = x[0], x[1:]
    if h > y:
        return _biggest(t, h)
    return _biggest(t, y)
