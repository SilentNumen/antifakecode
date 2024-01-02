import hashlib
import random
import time

def generate_authentication_code(user_id, secret_key):
    # 用于生成防伪认证码的字符串
    data = str(user_id) + str(secret_key) + str(int(time.time()))
    random_suffix = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
    data += random_suffix

    # 使用sha256算法生成防伪认证码
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    authentication_code = sha256.hexdigest()

    return authentication_code

# 示例
user_id = 12345
secret_key = 'secret_key'
authentication_code = generate_authentication_code(user_id, secret_key)
print(authentication_code)
