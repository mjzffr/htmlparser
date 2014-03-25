#!/usr/bin/env python2
import sys

testString = """<html>
              i  <head>
                <title>Parser</title>
                </head>
                <body>
                <p> Hello</p>
                <p> This is so cool!</p>
                </body>
                </html>"""

class Node(object):
    def __init__(self, tagtype, children=None):
        if not children:
            self.children = []
        else:
            self.children = children
        self.tagtype = tagtype

    def add_child(self, child):
        self.children.append(child)

    def prettystr(self, nesting=1):
        slist = [self.tagtype]
        for c in self.children:
            slist.append('\n' + '\t' * nesting)
            slist.append(c.prettystr(nesting + 1))
        return ''.join(slist)


def eat_head(s):
    return Node('head', [Node('title')]), """<body>
                <p> Hello</p>
                <p> This is so cool!</p>
                </body>
                </html>""", ""

def eat_body(s):
    return Node('body', []), """</html>""", ""


def eat_html(s):
    s = s.strip()
    node = None
    rest = s
    error = "No opening <html> tag"
    if s.startswith('<html>'):
        headnode, rest, error = eat_head(s[len('<html>'):])
        if not error:
            bodynode, rest, error = eat_body(rest)
            if not error:
                if rest.strip() == '</html>':
                    node = Node('html', [headnode, bodynode])
                    rest = ''
                else:
                    error = "no closing html tag"

    return node, rest, error


def parse(s):
    return eat_html(s)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            node, rest, error = parse(f.read())
            if node:
                print node.prettystr()
            print '\n-Rest:\n' + rest
            print '-Err:\n' + error
    else:
        print parse(testString)[0].prettystr()
