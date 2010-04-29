import logging
import email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from settings import your_mail_processor

class LogSenderHandler(InboundMailHandler):
    def receive(self, incoming_message):
        logging.info("Received a message from: %s" % (incoming_message.sender))
        outgoing_message = your_mail_processor().process(incoming_message)
        logging.info("Sending message to %s" % (outgoing_message.to))
        
        outgoing_message.send()



application = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()