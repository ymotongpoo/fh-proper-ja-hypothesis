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
from hypothesis.strategies import integers


# NOTE: if we drop the max_value, this PBT may create a tremendously large list
# and may break the system.
@given(start=integers(), count=integers(min_value=0, max_value=100000))
@settings(max_examples=100)
def test_increments(start, count):
    l = range(start, start+count+1)
    assert count+1 == len(l) and increments(l)


def increments(l):
    if len(l) == 1:
        return True
    for i in range(len(l)-1):
        if l[i] >= l[i+1]:
            return False
    return True


if __name__ == "__main__":
    start, count = 5999, 10000000
    l = [start + i for i in range(count+1)]
    print(increments(l))
