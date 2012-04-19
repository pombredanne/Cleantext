"""
Cleantext
"""

from html5lib import parse


__version__ = '0.1'


ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
    'sup',
    'sub',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
]


ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}


class CleanText(object):

    def __init__(self,
                 tags=ALLOWED_TAGS,
                 attributes=ALLOWED_ATTRIBUTES,
                 replace={},
                 delete=[],
        ):
        """
        :param tags: list of tags to keep
        :param attributes: dictionnary of allowed attributes
                           by tags.
        :param replace: dictionnary of tags to replace
        :param delelte: tag of nodes to delete
        """
        self.tags = tags
        self.attributes = attributes
        self.replace = replace
        self.delete = delete

    def __call__(self, string):
        # e.g. string  = '<texte>spam <b>&</b> egg</texte>'
        xml = parse(string)
        # even if string is an html fragment
        # html5lib build a full document
        # we need to grab body content
        html = xml.childNodes[0]
        body = html.childNodes[1]
        for child in body.childNodes:
            self._run(child)
        output = ''
        # the parent node is not included in output
        for child in body.childNodes:
            output += child.toxml()
        return output

    def _recursive_run(self, node):
        for child in node.childNodes:
            self._run(child)

    def _run(self, node):
        if node.type == 6:  # CommentNode
            node.parent.removeChild(node)
            return
        if node.type == 4:  # TextNode
            return
        if node.name in self.tags:
            if node.name in self.attributes:
                self.sanitize_attributes(node)
            else:
                node.attributes.clear()
            for child in node.childNodes:
                self._run(child)
        elif node.name in self.replace:
            self.sanitize_attributes(node)
            # add attributes provided
            new_attributes = self.replace[node.name][1]
            node.attributes.update(new_attributes)
            # rename node
            node.name = self.replace[node.name][0]
            # recurse
            for child in node.childNodes:
                self._run(child)
        elif node.name in self.delete:
            node.parent.removeChild(node)
        else:
            # move child to parent and recurse
            for child in node.childNodes:
                node.parent.insertBefore(child, node)
                self._run(child)
            node.parent.removeChild(node)

    def sanitize_attributes(self, node):
        # clean up attributes
        for attr in node.attributes.keys():
            if attr not in self.attributes.get(node.name, []):
                del node.attributes[attr]

cleantext = CleanText()
