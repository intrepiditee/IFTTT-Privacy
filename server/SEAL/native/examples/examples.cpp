// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include "examples.h"

using namespace std;
using namespace seal;

int main(int argc, char *argv[])
{
#ifdef SEAL_VERSION
    // cout << "Microsoft SEAL version: " << SEAL_VERSION << endl;
#endif
	    /*
    In this example, we demonstrate performing simple computations (a polynomial
    evaluation) on encrypted integers using the BFV encryption scheme.

    The first task is to set up an instance of the EncryptionParameters class.
    It is critical to understand how the different parameters behave, how they
    affect the encryption scheme, performance, and the security level. There are
    three encryption parameters that are necessary to set:

        - poly_modulus_degree (degree of polynomial modulus);
        - coeff_modulus ([ciphertext] coefficient modulus);
        - plain_modulus (plaintext modulus; only for the BFV scheme).

    The BFV scheme cannot perform arbitrary computations on encrypted data.
    Instead, each ciphertext has a specific quantity called the `invariant noise
    budget' -- or `noise budget' for short -- measured in bits. The noise budget
    in a freshly encrypted ciphertext (initial noise budget) is determined by
    the encryption parameters. Homomorphic operations consume the noise budget
    at a rate also determined by the encryption parameters. In BFV the two basic
    operations allowed on encrypted data are additions and multiplications, of
    which additions can generally be thought of as being nearly free in terms of
    noise budget consumption compared to multiplications. Since noise budget
    consumption compounds in sequential multiplications, the most significant
    factor in choosing appropriate encryption parameters is the multiplicative
    depth of the arithmetic circuit that the user wants to evaluate on encrypted
    data. Once the noise budget of a ciphertext reaches zero it becomes too
    corrupted to be decrypted. Thus, it is essential to choose the parameters to
    be large enough to support the desired computation; otherwise the result is
    impossible to make sense of even with the secret key.
    */
    EncryptionParameters parms(scheme_type::BFV);

    /*
    The first parameter we set is the degree of the `polynomial modulus'. This
    must be a positive power of 2, representing the degree of a power-of-two
    cyclotomic polynomial; it is not necessary to understand what this means.

    Larger poly_modulus_degree makes ciphertext sizes larger and all operations
    slower, but enables more complicated encrypted computations. Recommended
    values are 1024, 2048, 4096, 8192, 16384, 32768, but it is also possible
    to go beyond this range.

    In this example we use a relatively small polynomial modulus. Anything
    smaller than this will enable only very restricted encrypted computations.
    */
    size_t poly_modulus_degree = 4096;
    parms.set_poly_modulus_degree(poly_modulus_degree);

    /*
    Next we set the [ciphertext] `coefficient modulus' (coeff_modulus). This
    parameter is a large integer, which is a product of distinct prime numbers,
    each up to 60 bits in size. It is represented as a vector of these prime
    numbers, each represented by an instance of the SmallModulus class. The
    bit-length of coeff_modulus means the sum of the bit-lengths of its prime
    factors.

    A larger coeff_modulus implies a larger noise budget, hence more encrypted
    computation capabilities. However, an upper bound for the total bit-length
    of the coeff_modulus is determined by the poly_modulus_degree, as follows:

        +----------------------------------------------------+
        | poly_modulus_degree | max coeff_modulus bit-length |
        +---------------------+------------------------------+
        | 1024                | 27                           |
        | 2048                | 54                           |
        | 4096                | 109                          |
        | 8192                | 218                          |
        | 16384               | 438                          |
        | 32768               | 881                          |
        +---------------------+------------------------------+

    These numbers can also be found in native/src/seal/util/hestdparms.h encoded
    in the function SEAL_HE_STD_PARMS_128_TC, and can also be obtained from the
    function

        CoeffModulus::MaxBitCount(poly_modulus_degree).

    For example, if poly_modulus_degree is 4096, the coeff_modulus could consist
    of three 36-bit primes (108 bits).

    Microsoft SEAL comes with helper functions for selecting the coeff_modulus.
    For new users the easiest way is to simply use

        CoeffModulus::BFVDefault(poly_modulus_degree),

    which returns std::vector<SmallModulus> consisting of a generally good choice
    for the given poly_modulus_degree.
    */
    parms.set_coeff_modulus(CoeffModulus::BFVDefault(poly_modulus_degree));

    /*
    The plaintext modulus can be any positive integer, even though here we take
    it to be a power of two. In fact, in many cases one might instead want it
    to be a prime number; we will see this in later examples. The plaintext
    modulus determines the size of the plaintext data type and the consumption
    of noise budget in multiplications. Thus, it is essential to try to keep the
    plaintext data type as small as possible for best performance. The noise
    budget in a freshly encrypted ciphertext is

        ~ log2(coeff_modulus/plain_modulus) (bits)

    and the noise budget consumption in a homomorphic multiplication is of the
    form log2(plain_modulus) + (other terms).

    The plaintext modulus is specific to the BFV scheme, and cannot be set when
    using the CKKS scheme.
    */
    parms.set_plain_modulus(256);

    /*
    Now that all parameters are set, we are ready to construct a SEALContext
    object. This is a heavy class that checks the validity and properties of the
    parameters we just set.
    */
    auto context = SEALContext::Create(parms);

    /*
    The encryption schemes in Microsoft SEAL are public key encryption schemes.
    For users unfamiliar with this terminology, a public key encryption scheme
    has a separate public key for encrypting data, and a separate secret key for
    decrypting data. This way multiple parties can encrypt data using the same
    shared public key, but only the proper recipient of the data can decrypt it
    with the secret key.

    We are now ready to generate the secret and public keys. For this purpose
    we need an instance of the KeyGenerator class. Constructing a KeyGenerator
    automatically generates the public and secret key, which can immediately be
    read to local variables.
    */
    
    PublicKey public_key;
	filebuf pk_fbi;
	if (pk_fbi.open ("pk.txt",ios::in)){
		istream pk_is(&pk_fbi);
		public_key.load(context, pk_is);
	}

    SecretKey secret_key;
	filebuf sk_fbi;
	if (sk_fbi.open ("sk.txt",ios::in)){
		istream sk_is(&sk_fbi);
		secret_key.load(context, sk_is);
	}

    /*
    To be able to encrypt we need to construct an instance of Encryptor. Note
    that the Encryptor only requires the public key, as expected.
    */
    Encryptor encryptor(context, public_key);
	
	/*
    We will of course want to decrypt our results to verify that everything worked,
    so we need to also construct an instance of Decryptor. Note that the Decryptor
    requires the secret key.
    */
    Decryptor decryptor(context, secret_key);
		
	/*
	Print how much memory we have allocated from the current memory pool.
	By default the memory pool will be a static global pool and the
	MemoryManager class can be used to change it. Most users should have
	little or no reason to touch the memory allocation system.
	*/
	size_t megabytes = MemoryManager::GetPool().alloc_byte_count() >> 20;

	int selection = 0;
	bool invalid = true;
	
	switch (atoi(argv[1])){
		case 1: {
			std::string diff_str;
//			
//			//parsing a
//			std::string a = argv[2];
//			std::string enc_string_a = encrypt_value(context, a);
//			// convert encrypted string to a Ciphertext object
//			istringstream iss_ct_a(enc_string_a);
//			Ciphertext a_encrypted;
//			a_encrypted.unsafe_load(context, iss_ct_a);
//			
//			//parsing b
//			std::string b = argv[3];
//			std::string enc_string_b = encrypt_value(context, b);
//
//			//convert encrypted string to Ciphertext object
//			istringstream iss_ct_b(enc_string_b);
//			Ciphertext b_encrypted;
//			b_encrypted.unsafe_load(context, iss_ct_b);
				
			diff_str = subs_from_file(context, argv[2], argv[3]);
			cout << diff_str;
			break;
		}
		case 2: {
			// Decryption
			// usage : ./sealexamples 2 <filename>
			string filename = argv[2];
			cout << decrypt_file(context, filename) << endl;	
			
			break;
		}
		case 3: {
			// Encryption 
			// usage ./sealexamples 3 <variable in hex, two characters only e.g. FF>
			string plain = argv[2];
			cout << encrypt_value(context, plain) << endl;		
			break;
		}
		case 4: {
			// Add multiple numbers
			vector<string> vec;
			for (size_t i = 0; i < argc - 2; i++) {
				vec.push_back(argv[2+i]);
			}
			cout << add_from_file_vector(context, vec);
			break;
		}	
	}

	return 0;

}