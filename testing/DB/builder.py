from cryptography.fernet import Fernet



key = Fernet.generate_key()
f = Fernet(key)

token = f.decrypt(b'gAAAAABkTZ87Svm9ASvNLSOi1lZwfEIahpoFNtUaUGEZ2grCwgwUsA1KBggmukbsb2D8sdRwvaubEWOG5GV2dEijJ0hCJVl-Gf3hw2cIkgCId-RrU8HMSwg=')

print(token)