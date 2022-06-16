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

def biggest(l: list):
    if len(l) == 0:
        return l[-1:]
    if len(l) == 1:
        return l[0]
    head, *tail = l
    if tail == []:
        return head
    tmp = head
    for n in tail:
        if n > tmp:
            tmp = n
    return tmp
