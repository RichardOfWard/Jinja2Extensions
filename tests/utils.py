import jinja2


def render_template_string(extension, template_string, **kwargs):
    env = jinja2.Environment(extensions=[extension],
                             undefined=jinja2.StrictUndefined)
    template = env.from_string(template_string)
    return template.render(**kwargs)


def check_result(extension, template_string, expected, **kwargs):
    result = render_template_string(extension, template_string, **kwargs)
    assert result == expected, "Expected %s, got %s" % (
        repr(expected), repr(result))


def check_error(extension, template_string, exception_class, **kwargs):
    try:
        render_template_string(extension, template_string, **kwargs)
    except exception_class:
        pass
    else:
        assert False, "Expected %s for %s" % (
            exception_class.__name__,
            repr(template_string)
        )
