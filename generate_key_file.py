from cryptography.fernet import Fernet


key = Fernet.generate_key()

with open('key.bin', 'wb') as file:
	file.write(key)
