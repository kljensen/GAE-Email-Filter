from mail_processor import *
import logging
class your_mail_processor(mail_processor):
    """docstring for your_mail_processor"""
    address_book = {
        'post' : 'post@kyle-jensen.posterous.com',
    }
    email_aliases = {
        'kljensen@gmail.com' : 'kljensen@gmail.com',
        'kyle@pipra.org' : 'kljensen@gmail.com',
    }
    filters = {
        'm' : ('Markdown', do_markdown),
        # 'g' : ('Google', do_google_for_msg),
    }

    # default_filters = ['g','m']
