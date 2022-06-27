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

from hypothesis import event, given
from hypothesis.strategies import (booleans, characters, composite, integers,
                                   lists, one_of, sampled_from, text, tuples)


@composite
def keys(draw):
    fixed = sampled_from(range(1, 11))
    return draw(one_of(fixed, integers()))

@composite
def vals(draw):
    return draw(booleans() | characters() | integers() | text())

# In order to print the statistics from `event`, you need to specify
# Hypothesis' statistics option: `--hypothesis-show-statistics`.
# See details here: https://hypothesis.readthedocs.io/en/latest/details.html#statistics
@given(lists(tuples(keys(), vals())))
def test_dupes(kv):
    m = {k: v for k, v in kv}
    [m[k] for k, _ in kv] # I want non existing key to be crashed
    range_min, range_max = to_range(5, len(kv) - len(ukey(kv)))
    event(f"dupes: {range_min}-{range_max}")


def to_range(m, n):
    base = n // m
    return (base*m, (base+1)*m)


def ukey(lt):
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
