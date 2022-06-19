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

from hypothesis import given
from hypothesis.strategies import (booleans, characters, composite, integers,
                                   lists, one_of, sampled_from, text, tuples)


@composite
def keys(draw):
    fixed = sampled_from(range(1, 11))
    return draw(one_of(fixed, integers()))

@composite
def vals(draw):
    return draw(booleans() | characters() | integers() | text())


@given(lists(tuples(keys(), vals())))
def test_dupes(kv):
    m = {k: v for k, v in kv}
    [m[k] for k, _ in kv] # I want non existing key to be crashed

