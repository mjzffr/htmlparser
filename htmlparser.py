#!/usr/bin/env python2

#with open('test.html', 'r') as f:
testString = """<html>
                <head>
                <title>Parser</title>
                </head>
                <body>
                <p> Hello</p>
                <p> This is so cool!</p>
                </body>
                </html>"""

bad = """<html>
                <head>
                <title>Parser</title>
                </head>
                <body>
                <p> Hello</p>
                <p> This is so cool!</p>
                </body>
                """

class Node(object):
    def __init__(self, tagtype, children=None):
        if not children:
            self.children = []
        else:
            self.children = children
        self.tagtype = tagtype


    def add_child(self, child):
        self.children.append(child)

    def to_str(self, nesting=1):
        import pdb
#        pdb.set_trace()
        slist = [self.tagtype]
        for c in self.children:
            slist.append('\n' + '\t' * nesting)
            slist.append(c.to_str(nesting + 1))
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
    error = ""
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
    print parse(testString)[0].to_str()
