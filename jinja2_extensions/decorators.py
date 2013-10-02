from jinja2 import nodes
from jinja2.ext import Extension


def simple_tag(function):
    tag_name = function.__name__

    class SimpleTagExtension(Extension):
        tags = set([tag_name])

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
                else:
                    args.append(parser.parse_expression())

            args_node = nodes.List(args)
            kwargs_node = nodes.List(kwargs)
            return nodes.Output(
                [self.call_method('_render', args=[args_node, kwargs_node])]
            ).set_lineno(lineno)

        def _render(self, args, kwargs_list):
            kwargs = dict(zip(kwargs_list[::2], kwargs_list[1::2]))
            return function(*args, **kwargs)

    return SimpleTagExtension
