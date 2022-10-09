import hmac
import hashlib

def signature(key,total_param):

    signature = hmac.new(key.encode(), total_param.encode(), hashlib.sha256).hexdigest()
    return signature

