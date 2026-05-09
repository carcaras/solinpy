============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- /home/jeiel/hackton/solana/solana-hackathon/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/jeiel/hackton/solana/solana-hackathon
configfile: pyproject.toml
plugins: cov-7.1.0, anyio-4.13.0
collecting ... collected 79 items

solinpy/client/test_client.py::TestSolanaRPCClient::test_endpoint_resolution PASSED [  1%]
solinpy/client/test_client.py::TestSolanaRPCClient::test_get_health_success PASSED [  2%]
solinpy/client/test_client.py::TestSolanaRPCClient::test_get_latest_blockhash PASSED [  3%]
solinpy/client/test_client.py::TestSolanaRPCClient::test_retry_on_network_error PASSED [  5%]
solinpy/client/test_client.py::TestSolanaRPCClient::test_rpc_error_response PASSED [  6%]
solinpy/client/test_client.py::TestSolanaRPCClient::test_send_transaction_payload PASSED [  7%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_insufficient_funds_error_is_friendly PASSED [  8%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_invalid_account_error_is_friendly PASSED [ 10%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_no_retry_on_fatal_rpc_error PASSED [ 11%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_exhausted_on_network_error PASSED [ 12%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_on_http_429 PASSED [ 13%]
solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_timeout_applied_to_config PASSED [ 15%]
solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_base64_to_bytes PASSED [ 16%]
solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_invalid_base64 PASSED [ 17%]
solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_encode_bytes_to_base64 PASSED [ 18%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey PASSED [ 20%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey_insufficient_bytes PASSED [ 21%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64 PASSED [ 22%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_big_endian PASSED [ 24%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_insufficient_bytes PASSED [ 25%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32 PASSED [ 26%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32_insufficient_bytes PASSED [ 27%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8 PASSED [ 29%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8_insufficient_bytes PASSED [ 30%]
solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_with_offset PASSED [ 31%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_basic PASSED [ 32%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_with_delegate PASSED [ 34%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_frozen PASSED [ 35%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_native PASSED [ 36%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_invalid_size PASSED [ 37%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_basic PASSED [ 39%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_with_authorities PASSED [ 40%]
solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_invalid_size PASSED [ 41%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_dict_data PASSED [ 43%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_string_data PASSED [ 44%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_base64_string PASSED [ 45%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token PASSED [ 46%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token_mint PASSED [ 48%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_explicit_program_type PASSED [ 49%]
solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_unknown_program_type PASSED [ 50%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_create_airdrop_devnet_success PASSED [ 51%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_devnet_success PASSED [ 53%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_testnet_success PASSED [ 54%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_invalid_cluster PASSED [ 55%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_custom_lamports PASSED [ 56%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_timeout_error PASSED [ 58%]
solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_polling_until_confirmed PASSED [ 59%]
solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_with_aliases PASSED [ 60%]
solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_without_aliases PASSED [ 62%]
solinpy/tests/test_coverage_boost.py::test_format_context_empty_and_filtered PASSED [ 63%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32601-Method not found-Metodo RPC desconhecido] PASSED [ 64%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-Account not found-Conta invalida ou inexistente] PASSED [ 65%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-blockhash expired-Blockhash expirado] PASSED [ 67%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32004-busy-Servico RPC temporariamente indisponivel] PASSED [ 68%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None-custom problem-Erro RPC ao executar getX: custom problem] PASSED [ 69%]
solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None--Erro RPC ao executar getX.] PASSED [ 70%]
solinpy/tests/test_coverage_boost.py::test_rpc_error_str_without_details PASSED [ 72%]
solinpy/tests/test_coverage_boost.py::test_rpc_error_from_rpc_error_with_data PASSED [ 73%]
solinpy/tests/test_coverage_boost.py::test_rpc_error_from_transport_default_message PASSED [ 74%]
solinpy/tests/test_coverage_boost.py::test_client_retryable_rpc_code_path PASSED [ 75%]
solinpy/tests/test_coverage_boost.py::test_client_retries_rpc_error_then_succeeds PASSED [ 77%]
solinpy/tests/test_coverage_boost.py::test_client_http_non_retryable_raises_transport_error PASSED [ 78%]
solinpy/tests/test_coverage_boost.py::test_client_balance_and_token_methods PASSED [ 79%]
solinpy/tests/test_coverage_boost.py::test_client_sol_and_token_balances_helpers PASSED [ 81%]
solinpy/tests/test_coverage_boost.py::test_mnemonic_import_from_mnemonic_success PASSED [ 82%]
solinpy/tests/test_coverage_boost.py::test_mnemonic_import_validation_errors PASSED [ 83%]
solinpy/tests/test_coverage_boost.py::test_derive_slip10_ed25519_path_validation_and_output PASSED [ 84%]
solinpy/tests/test_coverage_boost.py::test_decode_spl_token_account_all_optional_fields PASSED [ 86%]
solinpy/tests/test_coverage_boost.py::test_decode_account_data_fallback_paths PASSED [ 87%]
solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_airdrop_and_account_read SKIPPED [ 88%]
solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_send_sol_between_wallets SKIPPED [ 89%]
solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_generate_wallet_returns_valid_keypair SKIPPED [ 91%]
solinpy/tests/test_token.py::test_get_associated_token_address_matches_program_derivation PASSED [ 92%]
solinpy/tests/test_token.py::test_send_token_transfer_creates_receiver_ata_when_missing PASSED [ 93%]
solinpy/tests/test_token.py::test_send_token_transfer_skips_receiver_ata_creation_when_present PASSED [ 94%]
solinpy/tests/test_wallet.py::test_generate_keypair PASSED               [ 96%]
solinpy/tests/test_wallet.py::test_import_from_json PASSED               [ 97%]
solinpy/tests/test_wallet.py::test_import_from_json_file_not_found PASSED [ 98%]
solinpy/tests/test_wallet.py::test_import_from_json_invalid_format PASSED [100%]

============================== slowest durations ===============================
1.29s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_retry_on_network_error
0.10s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_polling_until_confirmed
0.10s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_timeout_error
0.08s call     solinpy/tests/test_coverage_boost.py::test_mnemonic_import_from_mnemonic_success
0.01s call     solinpy/tests/test_token.py::test_send_token_transfer_skips_receiver_ata_creation_when_present
0.01s call     solinpy/tests/test_coverage_boost.py::test_format_context_empty_and_filtered
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_on_http_429
0.00s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_rpc_error_response
0.00s call     solinpy/tests/test_coverage_boost.py::test_client_retries_rpc_error_then_succeeds
0.00s setup    solinpy/tests/test_wallet.py::test_import_from_json
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None--Erro RPC ao executar getX.]
0.00s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_create_airdrop_devnet_success
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_exhausted_on_network_error
0.00s call     solinpy/tests/test_token.py::test_send_token_transfer_creates_receiver_ata_when_missing
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_exhausted_on_network_error
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_no_retry_on_fatal_rpc_error
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None--Erro RPC ao executar getX.]
0.00s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_get_health_success
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_insufficient_funds_error_is_friendly
0.00s call     solinpy/tests/test_coverage_boost.py::test_mnemonic_import_validation_errors
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32_insufficient_bytes
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_invalid_account_error_is_friendly
0.00s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_devnet_success
0.00s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_send_transaction_payload
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32
0.00s call     solinpy/tests/test_coverage_boost.py::test_client_http_non_retryable_raises_transport_error
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32
0.00s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_testnet_success
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_base64_string
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_on_http_429
0.00s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_custom_lamports
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_base64_string
0.00s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_get_latest_blockhash
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32_insufficient_bytes
0.00s call     solinpy/tests/test_coverage_boost.py::test_client_sol_and_token_balances_helpers
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_rpc_error_response
0.00s setup    solinpy/tests/test_coverage_boost.py::test_rpc_error_str_without_details
0.00s call     solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_invalid_base64
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None--Erro RPC ao executar getX.]
0.00s call     solinpy/tests/test_coverage_boost.py::test_client_balance_and_token_methods
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32004-busy-Servico RPC temporariamente indisponivel]
0.00s call     solinpy/tests/test_coverage_boost.py::test_rpc_error_str_without_details
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_endpoint_resolution
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u32_insufficient_bytes
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-Account not found-Conta invalida ou inexistente]
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8_insufficient_bytes
0.00s call     solinpy/tests/test_coverage_boost.py::test_derive_slip10_ed25519_path_validation_and_output
0.00s setup    solinpy/tests/test_wallet.py::test_import_from_json_invalid_format
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-blockhash expired-Blockhash expirado]
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_timeout_applied_to_config
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token_mint
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32601-Method not found-Metodo RPC desconhecido]
0.00s call     solinpy/tests/test_wallet.py::test_import_from_json
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8
0.00s setup    solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None-custom problem-Erro RPC ao executar getX: custom problem]
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_base64_string
0.00s setup    solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_invalid_base64
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token_mint
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_create_airdrop_devnet_success
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_auto_detect_spl_token_mint
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_insufficient_funds_error_is_friendly
0.00s setup    solinpy/tests/test_coverage_boost.py::test_rpc_error_from_rpc_error_with_data
0.00s teardown solinpy/tests/test_coverage_boost.py::test_rpc_error_from_transport_default_message
0.00s setup    solinpy/tests/test_coverage_boost.py::test_client_retries_rpc_error_then_succeeds
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8_insufficient_bytes
0.00s call     solinpy/tests/test_coverage_boost.py::test_rpc_error_from_rpc_error_with_data
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_timeout_applied_to_config
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_frozen
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_retry_on_network_error
0.00s setup    solinpy/tests/test_coverage_boost.py::test_client_retryable_rpc_code_path
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_explicit_program_type
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_on_http_429
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey_insufficient_bytes
0.00s teardown solinpy/tests/test_coverage_boost.py::test_client_retryable_rpc_code_path
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_string_data
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_unknown_program_type
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_no_retry_on_fatal_rpc_error
0.00s call     solinpy/tests/test_wallet.py::test_import_from_json_invalid_format
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_string_data
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_retry_exhausted_on_network_error
0.00s call     solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_invalid_cluster
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_unknown_program_type
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_invalid_size
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32004-busy-Servico RPC temporariamente indisponivel]
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_send_transaction_payload
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32004-busy-Servico RPC temporariamente indisponivel]
0.00s teardown solinpy/tests/test_coverage_boost.py::test_rpc_error_str_without_details
0.00s call     solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_airdrop_and_account_read
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_basic
0.00s setup    solinpy/tests/test_coverage_boost.py::test_client_http_non_retryable_raises_transport_error
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_native
0.00s setup    solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_base64_to_bytes
0.00s teardown solinpy/tests/test_coverage_boost.py::test_rpc_error_from_rpc_error_with_data
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_explicit_program_type
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_polling_until_confirmed
0.00s call     solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_timeout_applied_to_config
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_frozen
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_basic
0.00s setup    solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_invalid_account_error_is_friendly
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_unknown_program_type
0.00s setup    solinpy/tests/test_coverage_boost.py::test_client_sol_and_token_balances_helpers
0.00s teardown solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_invalid_base64
0.00s call     solinpy/tests/test_coverage_boost.py::test_rpc_error_from_transport_default_message
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_with_offset
0.00s setup    solinpy/tests/test_coverage_boost.py::test_rpc_error_from_transport_default_message
0.00s setup    solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_encode_bytes_to_base64
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_insufficient_bytes
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_send_transaction_payload
0.00s teardown solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_with_aliases
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_rpc_error_response
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u8_insufficient_bytes
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_timeout_error
0.00s setup    solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_airdrop_and_account_read
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_invalid_size
0.00s call     solinpy/tests/test_coverage_boost.py::test_client_retryable_rpc_code_path
0.00s teardown solinpy/tests/test_coverage_boost.py::test_client_retries_rpc_error_then_succeeds
0.00s setup    solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_without_aliases
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None-custom problem-Erro RPC ao executar getX: custom problem]
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_with_delegate
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_with_delegate
0.00s setup    solinpy/tests/test_coverage_boost.py::test_client_balance_and_token_methods
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_invalid_cluster
0.00s teardown solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_generate_wallet_returns_valid_keypair
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_native
0.00s call     solinpy/tests/test_token.py::test_get_associated_token_address_matches_program_derivation
0.00s call     solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_generate_wallet_returns_valid_keypair
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_create_airdrop_devnet_success
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_devnet_success
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_frozen
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_with_offset
0.00s teardown solinpy/tests/test_coverage_boost.py::test_mnemonic_import_validation_errors
0.00s teardown solinpy/tests/test_coverage_boost.py::test_client_balance_and_token_methods
0.00s setup    solinpy/tests/test_coverage_boost.py::test_format_context_empty_and_filtered
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_testnet_success
0.00s setup    solinpy/tests/test_token.py::test_get_associated_token_address_matches_program_derivation
0.00s teardown solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_without_aliases
0.00s teardown solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_airdrop_and_account_read
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_explicit_program_type
0.00s call     solinpy/tests/test_coverage_boost.py::test_decode_spl_token_account_all_optional_fields
0.00s setup    solinpy/tests/test_coverage_boost.py::test_mnemonic_import_from_mnemonic_success
0.00s teardown solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_base64_to_bytes
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_custom_lamports
0.00s teardown solinpy/tests/test_coverage_boost.py::test_client_sol_and_token_balances_helpers
0.00s call     solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_decode_base64_to_bytes
0.00s call     solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_send_sol_between_wallets
0.00s teardown solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_send_sol_between_wallets
0.00s teardown solinpy/tests/test_coverage_boost.py::test_mnemonic_import_from_mnemonic_success
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_with_offset
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_polling_until_confirmed
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-Account not found-Conta invalida ou inexistente]
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_devnet_success
0.00s setup    solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_generate_wallet_returns_valid_keypair
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey_insufficient_bytes
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_invalid_account_error_is_friendly
0.00s teardown solinpy/tests/test_token.py::test_send_token_transfer_skips_receiver_ata_creation_when_present
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_with_authorities
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_no_retry_on_fatal_rpc_error
0.00s setup    solinpy/tests/test_token.py::test_send_token_transfer_creates_receiver_ata_when_missing
0.00s teardown solinpy/tests/test_token.py::test_get_associated_token_address_matches_program_derivation
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_with_delegate
0.00s setup    solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_with_aliases
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey
0.00s teardown solinpy/tests/test_coverage_boost.py::test_decode_account_data_fallback_paths
0.00s setup    solinpy/tests/test_coverage_boost.py::test_decode_spl_token_account_all_optional_fields
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-blockhash expired-Blockhash expirado]
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_testnet_success
0.00s teardown solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32601-Method not found-Metodo RPC desconhecido]
0.00s teardown solinpy/tests/test_coverage_boost.py::test_client_http_non_retryable_raises_transport_error
0.00s teardown solinpy/tests/test_wallet.py::test_import_from_json_invalid_format
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_native
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_dict_data
0.00s teardown solinpy/tests/test_wallet.py::test_import_from_json
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_invalid_cluster
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_invalid_size
0.00s setup    solinpy/tests/test_coverage_boost.py::test_derive_slip10_ed25519_path_validation_and_output
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey
0.00s teardown solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_string_data
0.00s setup    solinpy/tests/test_coverage_boost.py::test_mnemonic_import_validation_errors
0.00s setup    solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_timeout_error
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_basic
0.00s teardown solinpy/client/test_client.py::TestRPCRetryAndTimeout::test_insufficient_funds_error_is_friendly
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-Account not found-Conta invalida ou inexistente]
0.00s setup    solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_dict_data
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_account_invalid_size
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_with_authorities
0.00s call     solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_encode_bytes_to_base64
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_retry_on_network_error
0.00s teardown solinpy/tests/test_token.py::test_send_token_transfer_creates_receiver_ata_when_missing
0.00s call     solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_with_aliases
0.00s call     solinpy/client/test_client.py::TestSolanaRPCClient::test_endpoint_resolution
0.00s setup    solinpy/tests/test_wallet.py::test_generate_keypair
0.00s teardown solinpy/tests/test_coverage_boost.py::test_format_context_empty_and_filtered
0.00s teardown solinpy/tests/test_coverage_boost.py::test_decode_spl_token_account_all_optional_fields
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_big_endian
0.00s call     solinpy/tests/test_coverage_boost.py::test_decode_account_data_fallback_paths
0.00s call     solinpy/tests/test_wallet.py::test_generate_keypair
0.00s teardown solinpy/tests/test_wallet.py::test_generate_keypair
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_get_health_success
0.00s call     solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_basic
0.00s setup    solinpy/tests/test_devnet_integration.py::TestDevnetIntegration::test_devnet_send_sol_between_wallets
0.00s teardown solinpy/tests/test_coverage_boost.py::test_derive_slip10_ed25519_path_validation_and_output
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_basic
0.00s teardown solinpy/tests/test_airdrop.py::TestRequestAirdrop::test_airdrop_custom_lamports
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32601-Method not found-Metodo RPC desconhecido]
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[None-custom problem-Erro RPC ao executar getX: custom problem]
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_big_endian
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_pubkey_insufficient_bytes
0.00s setup    solinpy/client/test_client.py::TestSolanaRPCClient::test_get_latest_blockhash
0.00s setup    solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_invalid_size
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_invalid_size
0.00s call     solinpy/tests/test_account_decoder.py::TestGenericAccountDecoding::test_decode_dict_data
0.00s call     solinpy/tests/test_wallet.py::test_import_from_json_file_not_found
0.00s setup    solinpy/tests/test_token.py::test_send_token_transfer_skips_receiver_ata_creation_when_present
0.00s call     solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64
0.00s call     solinpy/tests/test_coverage_boost.py::test_friendly_rpc_message_variants[-32000-blockhash expired-Blockhash expirado]
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_insufficient_bytes
0.00s setup    solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_insufficient_bytes
0.00s setup    solinpy/tests/test_coverage_boost.py::test_decode_account_data_fallback_paths
0.00s call     solinpy/tests/test_coverage_boost.py::test_rpc_config_post_init_without_aliases
0.00s teardown solinpy/tests/test_account_decoder.py::TestBase64Decoding::test_encode_bytes_to_base64
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_basic
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64_big_endian
0.00s teardown solinpy/tests/test_account_decoder.py::TestByteParsing::test_parse_u64
0.00s teardown solinpy/tests/test_account_decoder.py::TestSPLTokenDecoding::test_decode_spl_token_mint_with_authorities
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_get_latest_blockhash
0.00s setup    solinpy/tests/test_wallet.py::test_import_from_json_file_not_found
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_get_health_success
0.00s teardown solinpy/client/test_client.py::TestSolanaRPCClient::test_endpoint_resolution
0.00s teardown solinpy/tests/test_wallet.py::test_import_from_json_file_not_found
======================== 76 passed, 3 skipped in 1.82s =========================
