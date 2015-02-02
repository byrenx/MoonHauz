import wtforms


class MultipleReferenceCheckboxWidget(object):
    """
    Widget for MultipleReferenceField. Displays options as checkboxes"""
    def __init__(self, html_tag='div'):
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs['class'] = kwargs.get('class', '').replace('span6', '')
        html = [u'<%s %s>'
            % (self.html_tag, wtforms.widgets.html_params(**kwargs))]
        for subfield in field:
            html.append(u'<label class="checkbox" for="%s">%s %s</label>'
                % (subfield.label.field_id, subfield(), subfield.label.text))
        html.append(u'</%s>' % self.html_tag)
        return wtforms.widgets.HTMLString(u''.join(html))
