
# The contents of this file are subject to the Mozilla Public License
# (MPL) Version 1.1 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License
# at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and
# limitations under the License.
#
# The Original Code is LEPL (http://www.acooke.org/lepl)
# The Initial Developer of the Original Code is Andrew Cooke.
# Portions created by the Initial Developer are Copyright (C) 2009-2010
# Andrew Cooke (andrew@acooke.org). All Rights Reserved.
#
# Alternatively, the contents of this file may be used under the terms
# of the LGPL license (the GNU Lesser General Public License,
# http://www.gnu.org/licenses/lgpl.html), in which case the provisions
# of the LGPL License are applicable instead of those above.
#
# If you wish to allow use of your version of this file only under the
# terms of the LGPL License and not to allow others to use your version
# of this file under the MPL, indicate your decision by deleting the
# provisions above and replace them with the notice and other provisions
# required by the LGPL License.  If you do not delete the provisions
# above, a recipient may use your version of this file under either the
# MPL or the LGPL License.

'''
See http://groups.google.com/group/lepl/browse_thread/thread/79e39e03a03718cc?hl=en_US

The different tree structures seen here seem to be related to the how the
left-recursive memoisation fails.  In the case without lexer the string is
shorter, which causes failure earlier.  I am not at all sure about this...
'''

from unittest import TestCase
from logging import basicConfig, DEBUG

from lepl import *
from lepl._test.base import assert_str


class LeftBugTest(TestCase):
    
    def test_right_no_lexer(self):
        #basicConfig(level=DEBUG)
        word = Any()
        expr1 = Delayed()
        call = (expr1 & word) > List
        expr1 += (call | Empty() | word)
        program = expr1 & Eos()
        program.config.trace_stack().auto_memoize()
        parser = program.get_parse()
        print(parser.matcher.tree())
        parsed = parser("abc")
        assert_str(parsed[0],
"""List
 +- List
 |   +- List
 |   |   `- 'a'
 |   `- 'b'
 `- 'c'""")
    
    def test_right(self):
        #basicConfig(level=DEBUG)
        #CLine = ContinuedBLineFactory(Token(r'\\'))
        word = Token("[A-Za-z_][A-Za-z0-9_]*")
        expr1 = Delayed()
        call = (expr1 & word) > List
        expr1 += (call | Empty() | word)
        program = Trace(expr1 & Eos())
        program.config.trace_stack().auto_memoize()
        parser = program.get_parse()
        #print(parser.matcher.tree())
        parsed = parser("a b c")
        assert_str(parsed[0],
"""List
 +- List
 |   +- List
 |   |   `- 'a'
 |   `- 'b'
 `- 'c'""")

    def test_left(self):
        CLine = ContinuedBLineFactory(r'\\')
        expr0 = Token("[A-Za-z_][A-Za-z0-9_]*")
        expr1 = Delayed()
        call = (expr1 & expr0) > List # Deliberately not expr0 & expr1
        expr1 += (call | Empty () | expr0)
        program = (CLine(expr1) & Eos())
        program.config.blocks(block_policy=rightmost).auto_memoize()
        parsed = program.parse("a b c")
        assert_str(parsed[0],
"""List
 +- List
 |   +- List
 |   |   `- 'a'
 |   `- 'b'
 `- 'c'""")
        