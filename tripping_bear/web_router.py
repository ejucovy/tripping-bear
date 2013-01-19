import urllib

def get_headers(msg, contact):
    return {'Http-X-Username': contact.username}

def get_url(msg, contact):
    if msg['subject'].strip().lower() == 'subscribe':
        return 'http://localhost:8000/subscribe/'
    if msg['subject'].strip().lower() == 'unsubscribe':
        return 'http://localhost:8000/unsubscribe/'
    return 'http://localhost:8000/post_message/'
    
def get_body(msg, contact):
    list = msg['To'].split('@')[0]
    payload = {'list': list}
    if msg['subject'].strip().lower() == 'subscribe':
        pass
    elif msg['subject'].strip().lower() == 'unsubscribe':
        pass
    else:
        payload['subject'] = msg['subject']
    return urllib.urlencode(payload)

from httplib2 import Http
def make_request(msg, contact):
    http = Http()
    headers = get_headers(msg, contact)
    url = get_url(msg, contact)
    return http.request(url, "POST", headers=headers, body=get_body(msg, contact))
