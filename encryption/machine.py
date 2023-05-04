from sqlalchemy import Column, Integer, String, LargeBinary, create_engine
from sqlalchemy.orm import declarative_base, Session
from cryptography.fernet import Fernet

import base64

Base = declarative_base()


class settings_tabel(Base):
	__tablename__ = "settings"
	id = Column(Integer, primary_key=True)
	paranoid = Column(Integer)
	delete = Column(Integer)

	def __repr__(self):
		return self.paranoid, self.delete



class passwordTest(Base):
	__tablename__ = "passwordTest"
	id = Column(Integer, primary_key=True)
	password_test = Column(String(200))

class PasswordIndex(Base):
	__tablename__ = "password_index"

	id = Column(Integer, primary_key=True)
	refrence = Column(String(1000))
	site_url = Column(String(2000))
	username = Column(String(300))
	password = Column(String(1000))
	pin = Column(String(40))
	email = Column(String(400))
	phonenumber = Column(String(10000))
	public_key = Column(LargeBinary())
	private_key = Column(LargeBinary())
	pgp_password = Column(String(1000))
	note = Column(String(100000))

	def __repr__(self):
		return self.refrence, self.id, self.site_url, self.username, self.password, self.pin, self.email, self.phonenumber, self.public_key, self.private_key, self.pgp_password, self.note
	def __str__(self):
		return f" {self.refrence}, {self.id}, {self.site_url}, {self.username}, {self.password}, {self.pin}, {self.email}, {self.phonenumber}, {self.public_key}, {self.private_key}, {self.pgp_password}, {self.note}"
class FileManager(Base):
	__tablename__ = "file_manager"
	refrence = Column(String(1000))
	id = Column(Integer, primary_key=True)
	filename = Column(String(400))
	file_extention = Column(String(50))
	data = Column(LargeBinary())

	def __repr__(self):
		return self.refrence, self.filename, self.file_extention, self.data

	
	

class Database_equiptment:
	def __init__(self, fname):
		self.database_name = fname
		self.engine = create_engine(self.database_name)


	def create_database(self):
		Base.metadata.create_all(self.engine)
	

	def fresh_and_clean(self):
		"""make it easyer to start from scratch"""
		key = bytes(base64.urlsafe_b64encode(b'Sixteen byte keySixteen byte key'))#32 byte key
		f = Fernet(key)
		s = settings_tabel(paranoid = 0, delete=0)
		p = passwordTest(password_test=str(base64.urlsafe_b64encode(f.encrypt(b'test')).decode()))
		with Session(self.engine) as session:
			session.add(s)
			session.add(p)
			session.flush()
			session.commit()

	def decrypt_entry(self, password, data: str, is_file=False):
		"""This will decrypt the data"""
		if not self.test_password(password):
			return "Get Fucked"
		
		key = bytes(base64.urlsafe_b64encode(password))#b'Sixteen byte keySixteen byte key'
		f = Fernet(key)
		try:
			
			if type(data) == bytes:
				if is_file:
					return f.decrypt(data.decode())

				return f.decrypt(data.decode()).decode()
			
			e = base64.urlsafe_b64decode(data)
			return f.decrypt(e).decode()
		except: 
			pass



	def test_password(self, password):
		"""This will verify that the password will work"""
		key = bytes(base64.urlsafe_b64encode(password))#b'Sixteen byte keySixteen byte key'
		try:
			f = Fernet(key)
		except ValueError:#not correct lenght 
			return False
		try:
			with Session(self.engine) as session:
				tes = session.query(passwordTest).filter_by(id=1).first()

				de = base64.urlsafe_b64decode(str(tes.password_test).encode())
				f.decrypt(de).decode()
				return True
		except:#Fernet.InvalidToken:
			return False

	def add_a_password(self, password, items: dict):
		"""This will add a password tos the database"""
		if not self.test_password(password):
			return "Get Fucked"
		
		key = bytes(base64.urlsafe_b64encode(bytes(password)))
		f = Fernet(key)
		refrence = items["refrence"]
		site_url = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["site_url"].encode()))).decode())
		username = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["username"].encode()))).decode())
		password = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["password"].encode()))).decode())
		pin = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["pin"].encode()))).decode())
		email = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["email"].encode()))).decode())
		phonenumber = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["phonenumber"].encode()))).decode())


		#make these base64 /utf8 encoded
		public_key = f.encrypt(bytes(items["public_key"].encode()))
		private_key = f.encrypt(bytes(items["private_key"].encode()))

		pgp_password = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["pgp_password"].encode()))).decode())
		note = str(base64.urlsafe_b64encode(f.encrypt(bytes(items["note"].encode()))).decode())

		password_data_to_add = PasswordIndex(refrence=refrence, site_url=site_url, username=username, password=password, pin=pin, email=email, phonenumber=phonenumber, public_key=public_key, private_key=private_key, pgp_password=pgp_password ,note=note)

		with Session(self.engine) as session:
			session.add(password_data_to_add)
			session.commit()

	def retreve_password_refrences(self):
		"""This will get the non encrypted text in the tabel so we can pick the right password"""
		with Session(self.engine) as session:
			retreved_refrances = session.query(PasswordIndex).with_entities(PasswordIndex.refrence)
			return [refrences[0] for refrences in retreved_refrances]
		
	def get_password_data_by_refrance(self, refr, password) -> dict:
		"""This will get a row with a specified refrance"""
		with Session(self.engine) as session:
			password_data = session.query(PasswordIndex).filter(PasswordIndex.refrence == refr).first()
			dic_data = {"refrance":password_data.refrence, "site_url":self.decrypt_entry(password, password_data.site_url), "username":self.decrypt_entry(password, password_data.username), "password":self.decrypt_entry(password, password_data.password), "pin":self.decrypt_entry(password, password_data.pin), "email":self.decrypt_entry(password, password_data.email), "phonenumber":self.decrypt_entry(password, password_data.phonenumber), "public_key":self.decrypt_entry(password, password_data.public_key), "private_key":self.decrypt_entry(password, password_data.private_key), "pgp_password":self.decrypt_entry(password, password_data.pgp_password),"note":self.decrypt_entry(password, password_data.note)}
			return dic_data
		
	def delete_password_data_by_refrance(self, refr):
		"""deletes a password by the refrence"""
		with Session(self.engine) as session:
			password_data = session.query(PasswordIndex).filter(PasswordIndex.refrence == refr).first()
			session.delete(password_data)
			session.commit()	



	def add_a_file(self, password, items: dict):
		if not self.test_password(password):
			return "Get Fucked"
		
		key = bytes(base64.urlsafe_b64encode(bytes(password)))
		f = Fernet(key)

		refrence = items["refrence"]
		parsed_filename = items["filename"].split("/")[-1].split(".")[0]
		filename = str(base64.urlsafe_b64encode(f.encrypt(bytes(parsed_filename.encode()))).decode())
		parsed_file_extention = items["filename"].split(".")[-1]
		file_extention = str(base64.urlsafe_b64encode(f.encrypt(bytes(parsed_file_extention.encode()))).decode())

		with open(items["filename"], "rb") as file:
			data = f.encrypt(file.read())

		password_data_to_add = FileManager(refrence=refrence, filename=filename, file_extention=file_extention, data=data)
		with Session(self.engine) as session:
			session.add(password_data_to_add)
			session.commit()

	def retreve_file_refrences(self):
		"""This will get the non encrypted text in the tabel so we can pick the right file"""
		with Session(self.engine) as session:
			retreved_refrances = session.query(FileManager).with_entities(FileManager.refrence).all()
			return [refrences[0] for refrences in retreved_refrances]
		
	def get_file_data_by_refrance(self, refr, password) -> dict:
		"""This will get a row with a specified refrance"""
		with Session(self.engine) as session:
			password_data = session.query(FileManager).filter(FileManager.refrence == refr).first()
			dict_data = {"refrence":self.decrypt_entry(password, password_data.refrence), "filename":self.decrypt_entry(password, password_data.filename), "file_extention":self.decrypt_entry(password, password_data.file_extention), "data": self.decrypt_entry(password, password_data.data, is_file=True)}
			return dict_data
		
	def delete_file_data_by_refrance(self, refr):
		"""deletes a file by the refrence"""
		with Session(self.engine) as session:
			password_data = session.query(FileManager).filter(FileManager.refrence == refr).first()
			session.delete(password_data)
			session.commit()

	def change_paranoid_setting(self):
		"""this changes a value in the data base to a 1 or a 0"""
		with Session(self.engine) as session:
			paranoid_setting = session.query(settings_tabel).filter(settings_tabel.id == 1).first()
			if paranoid_setting.paranoid == 0:
				paranoid_setting.paranoid = 1
			else:
				paranoid_setting.paranoid = 0
			session.flush()
			session.commit()

	def get_paranoid_setting(self):
		with Session(self.engine) as session:
			paranoid_setting = session.query(settings_tabel).filter(settings_tabel.id == 1).first()
		return paranoid_setting.paranoid

	def change_delete_setting(self):
		"""this changes a value in the data base to a 1 or a 0"""
		with Session(self.engine) as session:
			delete_setting = session.query(settings_tabel).filter(settings_tabel.id == 1).first()
			if delete_setting.delete == 0:
				delete_setting.delete = 1
			else:
				delete_setting.delete = 0
			session.commit()

	def get_delete_setting(self):
		with Session(self.engine) as session:
			delete_setting = session.query(settings_tabel).filter(settings_tabel.id == 1).first()
		return delete_setting.delete
	
	def get_entries_with_private_keys(self, password):
		with Session(self.engine) as session:
			retreved_refrances = session.query(PasswordIndex).with_entities(PasswordIndex.private_key, PasswordIndex.refrence)
			return [refrences[1] for refrences in retreved_refrances if self.decrypt_entry(password, refrences[0]) != "default data"]
		
	def get_private_key_and_passphrase_by_refrance(self, password, refr) -> tuple:
		with Session(self.engine) as session:
			pgp_data = session.query(PasswordIndex).filter(PasswordIndex.refrence == refr).first()
			
			return (self.decrypt_entry(password, pgp_data.private_key), self.decrypt_entry(password, pgp_data.pgp_password))

#t = Database_equiptment("sqlite:///fhritp.db")
#t.create_database()

#a, w = t.get_private_key_and_passphrase_by_refrance(b'Sixteen byte keySixteen byte key', "pgp test")
#print(a,w)
#print(t.get_password_data_by_refrance("test", b'Sixteen byte keySixteen byte key'))

#test = {"refrence":"test", "filename":"test.txt", "file_extention":".txt"}
#t.add_a_file(b"Sixteen byte keySixteen byte key", test)
#print(t.get_file_data_by_refrance("test", b'Sixteen byte keySixteen byte key'))

'''
test = {"refrence":"test", "site_url":"test", "username":"test", "password":"test", "pin":"test", "email":"test", "phonenumber":"test", "public_key":"test", "private_key":"test", "note":"test"}
t.add_a_password(b"Sixteen byte keySixteen byte key", test)
'''

