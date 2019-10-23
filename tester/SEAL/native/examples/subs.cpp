// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include "examples.h"

using namespace std;
using namespace seal;

std::string subs(shared_ptr<SEALContext> context, Ciphertext a, Ciphertext b)
{
    /*
    Computations on the ciphertexts are performed with the Evaluator class. In
    a real use-case the Evaluator would not be constructed by the same party
    that holds the secret key.
    */
    Evaluator evaluator(context);
	
	
    Ciphertext result;
    evaluator.sub(a, b, result);
	
	// Write the output to the file
//	filebuf fb;
//	fb.open ("test.txt",ios::out);
//	
//	ostream os(&fb);
//	result.save(os);
//	
  	ostringstream oss;
	result.save(oss);
	
	return oss.str();
}

/**
* Returns the encrypted result of the substraction a - b
**/
std::string subs_from_file(shared_ptr<SEALContext> context, string a_filename, string b_filename)
{
	//cout << a_filename + b_filename << "Inside the library Function" << endl;
	// Create Ciphertext object from filename
	Ciphertext a;
	filebuf cipher_a_fbi;
	if (cipher_a_fbi.open (a_filename,ios::in)){
		istream cipher_a_is(&cipher_a_fbi);
		a.unsafe_load(context, cipher_a_is);
	}
	
	Ciphertext b;
	filebuf cipher_b_fbi;
	if (cipher_b_fbi.open (b_filename,ios::in)){
		istream cipher_b_is(&cipher_b_fbi);
		b.unsafe_load(context, cipher_b_is);
	}
	
	
    /*
    Computations on the ciphertexts are performed with the Evaluator class. In
    a real use-case the Evaluator would not be constructed by the same party
    that holds the secret key.
    */
    Evaluator evaluator(context);
	
	
    Ciphertext result;
    evaluator.sub(a, b, result);
	
	// Write the output to the file
//	filebuf fb;
//	fb.open ("test.txt",ios::out);
//	
//	ostream os(&fb);
//	result.save(os);
//	
  	ostringstream oss;
	result.save(oss);
	
	return oss.str();

}

string encrypt_value(shared_ptr<SEALContext> context, string a) {
	
	PublicKey public_key;
	filebuf pk_fbi;
	if (pk_fbi.open ("pk.txt",ios::in)){
		istream pk_is(&pk_fbi);
		public_key.load(context, pk_is);
	}
	
	Encryptor encryptor(context, public_key);
	
    Plaintext a_plain(a);

	//encrypt a
	Ciphertext a_encrypted;
    encryptor.encrypt(a_plain, a_encrypted);
	
	ostringstream oss;
	a_encrypted.save(oss);
	
	return oss.str();
	
}

string decrypt_value(shared_ptr<SEALContext> context, string cipher) {
	SecretKey secret_key;
	filebuf sk_fbi;
	if (sk_fbi.open ("sk.txt",ios::in)){
		istream sk_is(&sk_fbi);
		secret_key.load(context, sk_is);
	}
    
	Decryptor decryptor(context, secret_key);

	istringstream iss(cipher);
	Ciphertext ct;
	ct.unsafe_load(context, iss);

	Plaintext diff_decrypted;

	decryptor.decrypt(ct, diff_decrypted);
	return diff_decrypted.to_string();
			
}

string decrypt_file(shared_ptr<SEALContext> context, string filename) {
	
	SecretKey secret_key;
	filebuf sk_fbi;
	if (sk_fbi.open ("sk.txt",ios::in)){
		istream sk_is(&sk_fbi);
		secret_key.load(context, sk_is);
	}
    
	Decryptor decryptor(context, secret_key);
	
	Ciphertext ct;
	filebuf cipher_fbi;
	if (cipher_fbi.open (filename,ios::in)){
		istream cipher_is(&cipher_fbi);
		ct.unsafe_load(context, cipher_is);
	}
	
	Plaintext diff_decrypted;

	decryptor.decrypt(ct, diff_decrypted);
	return diff_decrypted.to_string();
			
}