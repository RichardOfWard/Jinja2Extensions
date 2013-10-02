import jinja2
from jinja2 import nodes
from jinja2.ext import Extension


def simple_tag(function):
    """Using simple tag to decorate a function will result in a Jinja2
    Extension allowing that function to be called from a template.

    Incorrect numbers, ordering or naming of arguments in the template will
    cause a TypeError to be raised, exactly if the funcion had been
    incorrectly in python. As with Python code, positional arguments cannot
    follow keyword arguments (i.e. you can't do `{% foo arg1=1 2 %}`).

    simple_tag is a thin wrapper around the SimpleTag class.
    """

    tag_name = function.__name__

    class SimpleTagDecorated(SimpleTag):
        tags = set([tag_name])

        def render(self, *args, **kwargs):
            return function(*args, **kwargs)

    return SimpleTagDecorated


class SimpleTag(Extension):
    """SimpleTag is base class for creating simple extensions that
    simply return a value to be rendered in the template.

    To use SimpleTag you must create your own class inheriting from it
    You must give it a tags attribute (a set containing the names by
    which your tag can be called from a template) and implement your own
    render method. `render` can accept positional and keyword arguments.

    Incorrect numbers, ordering or naming of arguments in the template will
    cause a TypeError to be raised, exactly if the funcion had been
    incorrectly in python. As with Python code, positional arguments cannot
    follow keyword arguments (i.e. you can't do `{% foo arg1=1 2 %}`).

    The simple_tag decorator is a quick and easy method of using SimpleTag.
    """

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
        return self.render(*args, **kwargs)

    def render(self, *args, **kwargs):
        raise NotImplementedError(
            "render not implemented for %s" % self.__class__)
