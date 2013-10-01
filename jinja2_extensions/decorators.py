from jinja2 import nodes
from jinja2.ext import Extension


def simple_tag(function):
    tag_name = function.__name__

    class SimpleTagExtension(Extension):
        tags = set([tag_name])

        def parse(self, parser):
            lineno = parser.stream.next().lineno
            node = nodes.Output([self.call_method('_render')])
            node.set_lineno(lineno)
            return node

        def _render(self):
            return function()

    return SimpleTagExtension
