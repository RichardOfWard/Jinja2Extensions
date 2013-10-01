from .utils import check_result, check_syntax_error
from jinja2_extensions.decorators import simple_tag


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
    check_syntax_error(
        string_tag,
        '{% string_tag 1 %}',
    )


def test_0002_string_tag_kwarg():
    check_syntax_error(
        string_tag,
        '{% string_tag arg=1 %}',
    )
