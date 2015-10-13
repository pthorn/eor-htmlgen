# coding: utf-8

from markupsafe import escape as html_escape


__all__ = ['Tag', 'Text', 'RawText']


class Tag(object):

    def __init__(self, tag, text=None, **attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = []
        if text:
            self.add(Text(text))

    def _render_attrs(self):
        strings = []

        for k, v in self.attrs.items():
            if v is None:
                continue

            # e.g. class_ => class, data_foo => data-foo
            k = k.rstrip('_').replace('_', '-')

            if k in _boolean_attrs:
                if v:
                    strings.append(k)
            else:
                if k == 'class':
                    v = _render_val_for_class_attr(v)
                strings.append('%s="%s"' % (html_escape(k), html_escape(v)))

        return '' if len(strings) == 0 else ' ' + ' '.join(strings)

    def add(self, child):
        if _is_sequence(child):
            self.children.extend([i for i in child if i])
        elif child:
            self.children.append(child)

        return self

    def render(self):
        rendered_children = [child.render() for child in self.children]
        return '<{tag}{attrs}>{children}{closing_tag}'.format(
            tag = html_escape(self.tag),
            attrs = self._render_attrs(),
            children=''.join(rendered_children),
            closing_tag = '' if self.tag in _singleton_tags else '</{0}>'.format(self.tag)
        )

    def __str__(self):
        return self.render()


class Text(object):

    def __init__(self, val):
        self.val = str(val)

    def render(self):
        return html_escape(self.val)

    def __str__(self):
        return self.render()


class RawText(object):

    def __init__(self, val):
        self.val = str(val)

    def render(self):
        return self.val

    def __str__(self):
        return self.render()


def _is_sequence(arg):
    """
    see http://stackoverflow.com/questions/10160416/json-serialization-of-sqlalchemy-association-proxies
    """
    return not hasattr(arg, "strip") and (hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))


def _render_val_for_class_attr(val):
    if isinstance(val, dict):
        return ' '.join([str(k) for k, v in val.items() if v])
    elif _is_sequence(val):
        return ' '.join([str(i) for i in val if i])
    else:
        return val


_singleton_tags = frozenset((
    "area",
    "base", "br",
    "col", "command",
    "embed",
    "hr",
    "img", "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
))


_boolean_attrs = frozenset((
    "allowfullscreen", "async", "autofocus",
    "checked", "compact",
    "declare", "default", "defer", "disabled",
    "formnovalidate",
    "hidden",
    "inert", "ismap", "itemscope",
    "multiple", "muted",
    "nohref", "noresize", "noshade", "novalidate", "nowrap",
    "open",
    "readonly", "required", "reversed",
    "seamless", "selected", "sortable",
    "truespeed","typemustmatch"
))
