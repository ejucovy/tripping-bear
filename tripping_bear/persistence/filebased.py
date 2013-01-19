import json
import os
import tempfile

class Persistent(object):

    @classmethod
    def get(cls, uid):
        path = os.path.join(cls.BASE_DIR, uid)
        if not os.path.exists(path):
            return None
        with open(path) as fp:
            return cls(**json.loads(fp.read()))

    def save(self):
        path = os.path.join(self.BASE_DIR, self.uid)
        with open(path, 'w') as fp:
            fp.write(json.dumps(self.__dict__))
        return self

    def delete(self):
        path = os.path.join(self.BASE_DIR, self.uid)
        os.unlink(path)
        
class EmailContact(Persistent):

    BASE_DIR = '/tmp/tripping-bear/contacts/'

    def __init__(self, email, confirmed, username, **kw):
        self.uid = self.email = email
        self.confirmed = confirmed
        self.username = username

    @classmethod
    def create(cls, email):
        username = User.generate_new_username()
        return cls(email=email, confirmed=False, username=username).save()

class User(Persistent):

    BASE_DIR = '/tmp/tripping-bear/users/'

    def __init__(self, username, **kw):
        self.uid = self.username = username

    @classmethod
    def generate_new_username(cls):
        fd, file = tempfile.mkstemp(prefix='', suffix='', dir=cls.BASE_DIR)
        return os.path.basename(file)

class DeferredEmail(Persistent):
    
    BASE_DIR = '/tmp/tripping-bear/deferred-emails/'

    def __init__(self, mail_string, **kw):
        fd, file = tempfile.mkstemp(prefix='', suffix='', dir=self.BASE_DIR)
        self.uid = os.path.basename(file)
        self.mail_string = mail_string
