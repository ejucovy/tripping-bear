import email
from email.utils import parseaddr
import sys

from tripping_bear.persistence import EmailContact, User, DeferredEmail
from tripping_bear.web_router import make_request

def handle_mail(mail_string):
    msg = email.message_from_string(mail_string.strip())
    addr = msg.get("From")
    addr = parseaddr(addr)[1]

    contact = EmailContact.get(addr)
    if contact is None:
        print "Contact %s not recognized" % addr
        contact = EmailContact.create(addr)
        # XXX TODO: trigger a confirmation email to the contact

    if not contact.confirmed:
        print "Contact %s not confirmed, deferring message" % addr
        DeferredEmail(mail_string).save()

    print make_request(msg, contact)

if __name__ == '__main__':
    mail_string = sys.stdin.read()
    handle_mail(mail_string)
