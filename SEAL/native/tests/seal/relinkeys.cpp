// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include "gtest/gtest.h"
#include "seal/relinkeys.h"
#include "seal/context.h"
#include "seal/keygenerator.h"
#include "seal/util/uintcore.h"
#include "seal/modulus.h"
#include "seal/util/polyarithsmallmod.h"

using namespace seal;
using namespace seal::util;
using namespace std;

namespace SEALTest
{
    TEST(RelinKeysTest, RelinKeysSaveLoad)
    {
        stringstream stream;
        {
            EncryptionParameters parms(scheme_type::BFV);
            parms.set_poly_modulus_degree(64);
            parms.set_plain_modulus(1 << 6);
            parms.set_coeff_modulus(CoeffModulus::Create(64, { 60 }));
            auto context = SEALContext::Create(parms, false, sec_level_type::none);
            KeyGenerator keygen(context);

            RelinKeys keys;
            RelinKeys test_keys;
            keys = keygen.relin_keys();
            keys.save(stream);
            test_keys.load(context, stream);
            ASSERT_EQ(keys.size(), test_keys.size());
            ASSERT_TRUE(keys.parms_id() == test_keys.parms_id());
            for (size_t j = 0; j < test_keys.size(); j++)
            {
                for (size_t i = 0; i < test_keys.key(j + 2).size(); i++)
                {
                    ASSERT_EQ(keys.key(j + 2)[i].data().size(), test_keys.key(j + 2)[i].data().size());
                    ASSERT_EQ(keys.key(j + 2)[i].data().int_array().size(), test_keys.key(j + 2)[i].data().int_array().size());
                    ASSERT_TRUE(is_equal_uint_uint(keys.key(j + 2)[i].data().data(), test_keys.key(j + 2)[i].data().data(), keys.key(j + 2)[i].data().int_array().size()));
                }
            }
        }
        {
            EncryptionParameters parms(scheme_type::BFV);
            parms.set_poly_modulus_degree(256);
            parms.set_plain_modulus(1 << 6);
            parms.set_coeff_modulus(CoeffModulus::Create(256, { 60, 50 }));

            auto context = SEALContext::Create(parms, false, sec_level_type::none);
            KeyGenerator keygen(context);

            RelinKeys keys;
            RelinKeys test_keys;
            keys = keygen.relin_keys();
            keys.save(stream);
            test_keys.load(context, stream);
            ASSERT_EQ(keys.size(), test_keys.size());
            ASSERT_TRUE(keys.parms_id() == test_keys.parms_id());
            for (size_t j = 0; j < test_keys.size(); j++)
            {
                for (size_t i = 0; i < test_keys.key(j + 2).size(); i++)
                {
                    ASSERT_EQ(keys.key(j + 2)[i].data().size(), test_keys.key(j + 2)[i].data().size());
                    ASSERT_EQ(keys.key(j + 2)[i].data().int_array().size(), test_keys.key(j + 2)[i].data().int_array().size());
                    ASSERT_TRUE(is_equal_uint_uint(keys.key(j + 2)[i].data().data(), test_keys.key(j + 2)[i].data().data(), keys.key(j + 2)[i].data().int_array().size()));
                }
            }
        }
    }
    TEST(RelinKeysTest, RelinKeysSeededSaveLoad)
    {
        // Returns true if a, b contains the same error.
        auto compare_kswitchkeys = [](const KSwitchKeys &a, const KSwitchKeys &b,
            const SecretKey &sk, shared_ptr<SEALContext> context)
        {
            auto compare_error = [](const Ciphertext &a_ct, const Ciphertext &b_ct,
                const SecretKey &sk1, shared_ptr<SEALContext> context1)
            {
                auto get_error = [](
                    const Ciphertext &encrypted, const SecretKey &sk2,
                    shared_ptr<SEALContext> context2)
                {
                    auto pool = MemoryManager::GetPool();
                    auto &context_data = *context2->get_context_data(encrypted.parms_id());
                    auto &parms = context_data.parms();
                    auto &coeff_modulus = parms.coeff_modulus();
                    size_t coeff_count = parms.poly_modulus_degree();
                    size_t coeff_mod_count = coeff_modulus.size();
                    size_t rns_poly_uint64_count = util::mul_safe(coeff_count, coeff_mod_count);

                    IntArray<Ciphertext::ct_coeff_type> error;
                    error.resize(rns_poly_uint64_count);
                    auto destination = error.begin();

                    auto copy_operand1(util::allocate_uint(coeff_count, pool));
                    for (size_t i = 0; i < coeff_mod_count; i++)
                    {
                        // Initialize pointers for multiplication
                        const uint64_t *encrypted_ptr = encrypted.data(1) + (i * coeff_count);
                        const uint64_t *secret_key_ptr = sk2.data().data() + (i * coeff_count);
                        uint64_t *destination_ptr = destination + (i * coeff_count);
                        util::set_zero_uint(coeff_count, destination_ptr);
                        util::set_uint_uint(encrypted_ptr, coeff_count, copy_operand1.get());
                        // compute c_{j+1} * s^{j+1}
                        util::dyadic_product_coeffmod(copy_operand1.get(), secret_key_ptr, coeff_count,
                            coeff_modulus[i], copy_operand1.get());
                        // add c_{j+1} * s^{j+1} to destination
                        util::add_poly_poly_coeffmod(destination_ptr,
                            copy_operand1.get(), coeff_count, coeff_modulus[i],
                            destination_ptr);
                        // add c_0 into destination
                        util::add_poly_poly_coeffmod(destination_ptr,
                            encrypted.data() + (i * coeff_count), coeff_count, coeff_modulus[i],
                            destination_ptr);
                    }
                    return error;
                };

                auto error_a = get_error(a_ct, sk1, context1);
                auto error_b = get_error(b_ct, sk1, context1);
                ASSERT_EQ(error_a.size(), error_b.size());
                ASSERT_TRUE(is_equal_uint_uint(
                    error_a.cbegin(), error_b.cbegin(), error_a.size()));
            };

            ASSERT_EQ(a.size(), b.size());
            auto iter_a = a.data().begin();
            auto iter_b = b.data().begin();
            for (; iter_a != a.data().end(); iter_a++, iter_b++)
            {
                ASSERT_EQ(iter_a->size(), iter_b->size());
                auto pk_a = iter_a->begin();
                auto pk_b = iter_b->begin();
                for (; pk_a != iter_a->end(); pk_a++, pk_b++)
                {
                    compare_error(pk_a->data(), pk_b->data(), sk, context);
                }
            }
        };

        stringstream stream;
        {
            EncryptionParameters parms(scheme_type::BFV);
            parms.set_poly_modulus_degree(8);
            parms.set_plain_modulus(65537);
            parms.set_coeff_modulus(CoeffModulus::Create(8, { 60 }));
            random_seed_type seed;
            for (auto &i: seed)
            {
                i = random_uint64();
            }
            auto rng = make_shared<BlakePRNGFactory>(BlakePRNGFactory(seed));
            parms.set_random_generator(rng);
            auto context = SEALContext::Create(parms, false, sec_level_type::none);
            KeyGenerator keygen(context);
            SecretKey secret_key = keygen.secret_key();

            keygen.relin_keys_save(stream);
            RelinKeys test_keys;
            test_keys.load(context, stream);
            RelinKeys keys = keygen.relin_keys();
            compare_kswitchkeys(keys, test_keys, secret_key, context);
        }
        {
            EncryptionParameters parms(scheme_type::BFV);
            parms.set_poly_modulus_degree(256);
            parms.set_plain_modulus(65537);
            parms.set_coeff_modulus(CoeffModulus::Create(256, { 60, 50 }));
            random_seed_type seed;
            for (auto &i: seed)
            {
                i = random_uint64();
            }
            auto rng = make_shared<BlakePRNGFactory>(BlakePRNGFactory(seed));
            parms.set_random_generator(rng);
            auto context = SEALContext::Create(parms, false, sec_level_type::none);
            KeyGenerator keygen(context);
            SecretKey secret_key = keygen.secret_key();

            keygen.relin_keys_save(stream);
            RelinKeys test_keys;
            test_keys.load(context, stream);
            RelinKeys keys = keygen.relin_keys();
            compare_kswitchkeys(keys, test_keys, secret_key, context);
        }
    }
}
