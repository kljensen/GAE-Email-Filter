import re
import logging

try:
    from google.appengine.api import mail
except ImportError:
    import sys
    sys.path.append("/usr/local/google_appengine")
    sys.path.append("/usr/local/google_appengine/lib/yaml/lib")
    from google.appengine.api import mail


def do_markdown( msg):
    """docstring for do_markdown"""
    from markdown2 import Markdown
    markdowner = Markdown()
    msg.html = markdowner.convert(msg.body)
    return msg

class mail_processor(object):
    """docstring for MailProcessor"""
    address_book = {
        'post' : 'post@posterous.com',
    }
    email_aliases = {}
    filters = {
        'm' : ('Markdown', do_markdown),
    }

    default_filters = ['m']

    def __init__(self):
        super(mail_processor, self).__init__()

    def process(self, incoming_message):
        """docstring for process"""
        
        bodies = incoming_message.bodies(content_type='text/plain')
        allBodies = ""; 
        for body in bodies:
            allBodies = allBodies + "\n\n" + body[1].decode()
        
        outgoing_message = mail.EmailMessage(
                            to = self.to_maker(incoming_message),
                            sender = self.sender_maker(incoming_message.sender),
                            subject = incoming_message.subject,
                            body = allBodies,
        )
        
        (filters_to_apply, outgoing_message) = self.filter_chooser(outgoing_message)
        for (name, f) in filters_to_apply:
            logging.info('Applying %s' % (name))
            outgoing_message = f(outgoing_message)
        return outgoing_message

    @staticmethod
    def clean_email_address(address):
        """docstring for clean_email_address"""
        add_re = re.compile(r'.*<(.+@.*\..+)>')
        m = add_re.search(address)
        if m:
            address = m.group(1)
        else:
            address = address.split('<')[-1].strip('>')
        return address.lower()

    def to_maker(self, msg):
        """docstring for to_maker"""
        if isinstance(msg.to, list):
            address = msg.to[0]
        else:
            address = msg.to
        
        address = self.clean_email_address(address)
        address = address.split('@')[0]
        if address == 'test':
            return msg.sender
    
        if address in self.address_book:
            return self.address_book[address]
    
        return address.replace('$', '@')
        
    def sender_maker(self, em):
        """docstring for sender_maker"""
        s = self.clean_email_address(em)
        s = self.email_aliases.get(s, s)
        logging.info('Sender = %s' % (s))
        return s



    def filter_chooser(self, msg):
        """docstring for filter_chooser"""
        # Subject ends with [m,jk,foo,e] string that specifies filters to apply
        filter_subject = re.compile(r'\s*\[([a-z]{1,3},?)+\]$')
        filters_to_apply = filter_subject.findall(msg.subject)
        if not filters_to_apply:
            filters_to_apply = self.default_filters
        else:
            msg.subject = filter_subject.sub('', msg.subject)
        return ([self.filters[f] for f in filters_to_apply], msg)
    