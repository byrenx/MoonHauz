from ferrisnose import AppEngineTest
from ferris.core import mail


class MailTest(AppEngineTest):

    def test(self):
        res, body, text_body = mail.send_template(
            sender='user@example.com',
            recipient='test@example.com',
            subject='Hello!',
            template_name='ferris_test',
            context={
                'name': 'Doctor'
            })

        assert 'Doctor' in body
        assert 'Doctor' in text_body
        assert '<h1>' in body
        assert '<h1>' not in text_body
