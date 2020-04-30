from biazza.models import UserTokens, Accounts, db

from hashlib import sha512
import secrets
import string

MIN_TOKEN_LENGTH = 20
MAX_TOKEN_LENGTH = 40


def generate_token_and_hash(min_length=MIN_TOKEN_LENGTH, max_length=MAX_TOKEN_LENGTH):

    if min_length > max_length or min_length <= 0 or max_length <= 0:
        raise Exception("Invalid arguments. min_length must be greater than max_length and both must be positive.")

    length = secrets.randbelow(max_length - min_length + 1) + min_length

    allowed_chars = string.ascii_letters + string.digits + string.punctuation

    token = ''
    for i in range(length):
        token += allowed_chars[secrets.randbelow(len(allowed_chars))]

    print(token)
    token_bytes = token.encode('utf-8')
    token_hash = sha512(token_bytes).hexdigest()
    return token, token_hash


def table_contains_hash(token_hash):
    return UserTokens.query.filter(UserTokens.token_hash == token_hash).scalar() is not None


def table_contains_token(token):
    token_bytes = token.encode('utf-8')
    return table_contains_hash(sha512(token_bytes).hexdigest())


def create_token_for_user(uid):
    token, token_hash = generate_token_and_hash()

    while table_contains_hash(token_hash):
        token, token_hash = generate_token_and_hash()

    db.session.add(UserTokens(user_id=uid, token_hash=token_hash))
    db.session.commit()
    return token


def get_user_with_token(token):
    if not token:
        return None

    t = token.encode('utf-8')
    token_obj = UserTokens.query.filter(UserTokens.token_hash == sha512(t).hexdigest()).first()
    user = None

    if token_obj:
        user = Accounts.query.filter(Accounts.id == token_obj.user_id).first()

    return user


def delete_token(token):
    if not token:
        return False

    t = token.encode('utf-8')
    token_obj = UserTokens.query.filter(UserTokens.token_hash == sha512(t).hexdigest()).first()

    if not token_obj:
        return False

    db.session.delete(token_obj)
    db.session.commit()
    return True
