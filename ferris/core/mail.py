from ferris.core import settings, template
from google.appengine.api import mail, app_identity
import logging


def send(recipient, subject, body, text_body=None, sender=None, reply_to=None, **kwargs):
    """
    Sends an html email to ``recipient`` with the given ``subject`` and ``body``.

    If ``sender`` is none, it's automatically set to ``app_config['email']['sender']``.

    If ``text_body`` is not specified, then ``body`` is used.

    Any additionally arguments are passed to ``mail.send_mail``, such as headers.
    """
    sender = sender if sender else settings.get('email')['sender']
    if not sender:
        sender = "noreply@%s.appspotmail.com" % app_identity.get_application_id()
        logging.info("No sender configured, using the default one: %s" % sender)

    if not text_body:
        text_body = body

    res = mail.send_mail(
        sender=sender,
        to=recipient,
        subject=subject,
        body=text_body,
        html=body,
        reply_to=reply_to if reply_to else sender,
        **kwargs)
    logging.info('Email sent to %s by %s with subject %s and result %s' % (recipient, sender, subject, res))
    return res


def send_template(recipient, subject, template_name, context=None, theme=None, **kwargs):
    """
    Renders a template and sends an email in the same way as :func:`send`.
    templates should be stored in ``/templates/email/<template>.html`` and ``/templates/email/<template>.txt``.
    If the txt template is not specified, then the html one will be used for the "plaintext" body.

    For example::

        mail.send_template(
            recipient='jondoe@example.com',
            subject='A Test Email',
            template_name='test',
            context={
                'name': 'George'
            }
        )

    Would render the template ``/templates/email/test.html`` and email the rendered html.
    """
    context = context if context else {}

    name = ('email/' + template_name + '.html', template)
    body = template.render_template(name, context, theme=theme)

    try:
        name = ('email/' + template_name + '.txt', template)
        text_body = template.render_template(name, context, theme=theme)
    except:
        logging.warning("No txt template found for email template %s, html will be used for plaintext as well." % template_name)
        text_body = None

    res = send(recipient, subject, body, text_body=text_body, **kwargs)

    return res, body, text_body
