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
