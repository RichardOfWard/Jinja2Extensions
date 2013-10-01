import jinja2

from jinja2.exceptions import TemplateSyntaxError


def render_template_string(extension, template_string, **kwargs):
    env = jinja2.Environment(extensions=[extension],
                             undefined=jinja2.StrictUndefined)
    template = env.from_string(template_string)
    return template.render(**kwargs)


def check_result(extension, template_string, expected, **kwargs):
    result = render_template_string(extension, template_string, **kwargs)
    assert result == expected, "Expected %s, got %s" % (
        repr(expected), repr(result))


def check_syntax_error(extension, template_string, **kwargs):
    try:
        render_template_string(extension, template_string, **kwargs)
    except TemplateSyntaxError:
        pass
    else:
        assert False, "Expected a syntax error for " + repr(template_string)
