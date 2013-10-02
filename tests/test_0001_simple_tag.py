import jinja2
from jinja2_extensions.decorators import simple_tag
from .utils import check_result, check_error


@simple_tag
def string_tag():
    return "string"


def test_0001_string_tag():
    check_result(
        string_tag,
        '{% string_tag %}',
        'string'
    )


def test_0002_string_tag_arg():
    check_error(
        string_tag,
        '{% string_tag 1 %}',
        TypeError,
    )


def test_0003_string_tag_kwarg():
    check_error(
        string_tag,
        '{% string_tag arg=1 %}',
        TypeError,
    )


@simple_tag
def arg_tag(arg):
    return arg


def test_0004_arg_tag():
    check_result(
        arg_tag,
        '{% arg_tag 1 %}',
        '1',
    )


def test_0005_arg_tag_no_args():
    check_error(
        arg_tag,
        '{% arg_tag %}',
        TypeError,
    )


def test_0006_arg_tag_extra_arg():
    check_error(
        arg_tag,
        '{% arg_tag 1 2 %}',
        TypeError,
    )


def test_0007_arg_tag_kwarg():
    check_result(
        arg_tag,
        '{% arg_tag arg=1 %}',
        '1'
    )


def test_0009_arg_tag_incorrect_kwarg():
    check_error(
        arg_tag,
        '{% arg_tag bad=1 %}',
        TypeError,
    )


def test_0010_arg_tag_undefined_arg():
    check_error(
        arg_tag,
        '{% arg_tag foo %}',
        jinja2.UndefinedError,
    )


def test_0011_arg_tag_undefined_kwarg():
    check_error(
        arg_tag,
        '{% arg_tag arg=foo %}',
        jinja2.UndefinedError,
    )


def test_0012_arg_tag_expr_arg():
    check_result(
        arg_tag,
        '{% arg_tag 1+2 %}',
        '3',
    )


def test_0013_arg_tag_expr_kwarg():
    check_result(
        arg_tag,
        '{% arg_tag arg=1+2 %}',
        '3',
    )


@simple_tag
def arg_tag2(arg1, arg2):
    return "%s %s" % (str(arg1), str(arg2))


def test_0014_arg_tag2_positional_positional():
    check_result(
        arg_tag2,
        '{% arg_tag2 1 2 %}',
        '1 2',
    )


def test_0015_arg_tag2_positional_named():
    check_result(
        arg_tag2,
        '{% arg_tag2 1 arg2=2 %}',
        '1 2',
    )


def test_0016_arg_tag2_named_named():
    check_result(
        arg_tag2,
        '{% arg_tag2 arg1=1 arg2=2 %}',
        '1 2',
    )


def test_0017_arg_tag2_named_named_reversed():
    check_result(
        arg_tag2,
        '{% arg_tag2 arg2=2 arg1=1 %}',
        '1 2',
    )


def test_0018_arg_tag2_named_positional():
    check_error(
        arg_tag2,
        '{% arg_tag2 arg2=2 1 %}',
        jinja2.TemplateSyntaxError,
    )


def test_0018_arg_tag2_named_positional_exception_lineno():
    try:
        check_result(
            arg_tag2,
            '''{% arg_tag2
            arg2=2
            1 %}''',
            'pass'
        )
    except jinja2.TemplateSyntaxError as e:
        assert e.lineno == 3
    else:
        assert False, "Expected TemplateSyntaxError"


def test_0019_arg_tag2_expressions():
    check_result(
        arg_tag2,
        '{% arg_tag2 1 + 2 3 + 4 %}',
        '3 7',
    )
