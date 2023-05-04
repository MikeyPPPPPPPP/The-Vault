from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base


from cryptography.fernet import Fernet
import base64

key = bytes(base64.urlsafe_b64encode(b'Sixteen byte keySixteen byte key'))#32 byte key
f = Fernet(key)

Base = declarative_base()



class test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cool = Column(String)
    
    #def __repr__(self):
    #    return self.name, self.cool
    
class new(Base):
    __tablename__ = "new"

    id = Column(Integer, primary_key=True)
    fun = Column(String)
    
    def __repr__(self):
        return self.fun


from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#make the database file
engine = create_engine("sqlite:///foo.db")

#create the database with the defined model
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()




with Session(engine) as session:
    
    a = new(fun=str(base64.urlsafe_b64encode(f.encrypt(b'sdf')).decode()))
    t = test(name="michaetl", cool="test")
    s = test(name="micfdsfhaetl", cool="tefsdsdfst")
    session.add(a)
    session.add(s)
    session.add(t)
    session.commit()
    
    #this is how i will get stof from the database
    #print(session.query(test).filter_by(id=1).first())

    #this will decrypt the stuf in the database
    #t = session.query(test).filter_by()#need to be a string
    t = session.query(test).with_entities(test.cool).all()#with_entities(test.cool)

    for x in t:
        print(x[0])

    #de = base64.urlsafe_b64decode(t.encode())

    #print(f.decrypt(de).decode())

"""
#https://www.pycryptodome.org/src/cipher/classic#cbc-mode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

import base64, json



data = b"secret"
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))
iv = base64.b64encode(cipher.iv).decode('utf-8')
ct = base64.b64encode(ct_bytes).decode('utf-8')
result = json.dumps({'iv':iv, 'ciphertext':ct})
print(result)

key = b'Sixteen byte key'
try:
    b64 = json.loads(result)
    iv = base64.b64decode(b64['iv'])
    ct = base64.b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)
except (ValueError, KeyError):
    print("Incorrect decryption")
"""
'''
#this uses ASE 128 CBC
from cryptography.fernet import Fernet



key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"my deep dark secret")
type(token)  -> byte


.generate_key()    -> base64.urlsafe_b64encode(os.urandom(32))  -> b'1hmq4_bJJ30FxGen344gb9njgCGKYZ0uHRi-cKZHcQY='  or str
'''