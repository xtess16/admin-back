import hashlib


#  Сгенерировать название аккаунта по email
def get_account_by_email(email):
    hash_account = hashlib.md5(email.encode())
    return hash_account.hexdigest()
