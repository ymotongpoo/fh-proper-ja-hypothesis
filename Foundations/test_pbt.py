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

from hypothesis import Verbosity, given, settings
from hypothesis.strategies import booleans, integers, one_of, text


# Hypothesis doesn't have any() strategy that generates arbitrary value of arbitrary type.
# Here, I use one_of() strategy to generate arbitrary value from a couple of primitive strategies.
@given(one_of(text(), booleans(), integers()))
@settings(max_examples=100, verbosity=Verbosity.verbose)
def test_prop(s):
    assert boolean(s)


def boolean(_):
    return True
