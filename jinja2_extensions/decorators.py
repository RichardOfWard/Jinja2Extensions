import jinja2
from jinja2 import nodes
from jinja2.ext import Extension


def simple_tag(function):
    tag_name = function.__name__

    class SimpleTagDecorated(SimpleTag):
        tags = set([tag_name])

        def _render(self, *args, **kwargs):
            return function(*args, **kwargs)

    return SimpleTagDecorated


class SimpleTag(Extension):

    def parse(self, parser):
        stream = parser.stream
        lineno = next(stream).lineno
        args = []
        kwargs = []
        while not stream.current.test('block_end'):
            current = stream.current
            if current.test('name') and stream.look().test('assign'):
                key = nodes.Const(next(stream).value,
                                  lineno=stream.current.lineno)
                stream.skip()
                value = parser.parse_expression()
                kwargs += [key, value]
            elif kwargs:
                raise jinja2.TemplateSyntaxError(
                    "non-keyword arg after keyword arg",
                    next(stream).lineno,
                    stream.name,
                    stream.filename
                )
            else:
                args.append(parser.parse_expression())

        args_node = nodes.List(args)
        kwargs_node = nodes.List(kwargs)
        return nodes.Output(
            [self.call_method(
                '_process_args_and_render',
                args=[args_node, kwargs_node])]
        ).set_lineno(lineno)

    def _process_args_and_render(self, args, kwargs_list):
        kwargs = dict(zip(kwargs_list[::2], kwargs_list[1::2]))
        return self._render(*args, **kwargs)

    def _render(self, args, **kwargs):
        raise NotImplementedError(
            "_render not implemented for %s" % self.__class__)
