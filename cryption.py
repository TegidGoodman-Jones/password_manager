from cryptography.fernet import Fernet

with open('key.bin', 'rb') as file:
	key = file.read()


def encrypt_password(password):

	cipher_suite = Fernet(key)

	b_password = bytes(password, 'utf-8')

	encrypted = cipher_suite.encrypt(b_password)

	return encrypted

def decrypt_password(encrypted_password):

	cipher_suite = Fernet(key)

	decrypted = cipher_suite.decrypt(encrypted_password)

	str_decrypted = bytes(decrypted).decode('utf-8')

	return str_decrypted




