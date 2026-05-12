# Structured Test Report

Source: tests_individual_report.md

## solinpy/client/test_client.py - TestSolanaRPCClient - test_endpoint_resolution

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._resolve_cluster_url
- What: (no docstring found)
- Result:
  - mainnet_endpoint: https://api.mainnet-beta.solana.com
  - custom_endpoint: https://meu-rpc.com

## solinpy/client/test_client.py - TestSolanaRPCClient - test_get_health_success

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_health
- What: (no docstring found)
- Result:
  - result: ok

## solinpy/client/test_client.py - TestSolanaRPCClient - test_get_latest_blockhash

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_latest_blockhash
- What: (no docstring found)
- Result:
  - blockhash: 8xYz...abc

## solinpy/client/test_client.py - TestSolanaRPCClient - test_retry_on_network_error

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._call
- What: (no docstring found)
- Result:
  - exception: Falha de comunicação ao executar getHealth após 2 tentativas. [método=getHealth | contexto=endpoint=https://api.devnet.solana.com | causa=<urlopen error connection refused>]
  - expected_calls: 2

## solinpy/client/test_client.py - TestSolanaRPCClient - test_rpc_error_response

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._raise_rpc_error
- What: (no docstring found)
- Result:
  - exception: Falha inesperada ao executar getHealth. [método=getHealth | contexto=endpoint=https://api.devnet.solana.com | causa=Requisição RPC inválida. Verifique os parâmetros enviados. [código RPC=-32600 | método=getHealth]]

## solinpy/client/test_client.py - TestSolanaRPCClient - test_send_transaction_payload

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.send_transaction
- What: (no docstring found)
- Result:
  - signature: 5sig...
  - method: sendTransaction
  - encoding: base64
  - maxRetries: 5

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_insufficient_funds_error_is_friendly

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.send_transaction
- What: (no docstring found)
- Result:
  - exception: Falha inesperada ao executar sendTransaction. [método=sendTransaction | contexto=tx_size=15, max_retries=5, endpoint=https://api.devnet.solana.com | causa=Saldo insuficiente ao executar sendTransaction. Verifique se a conta tem SOL suficiente para taxas e valor da operação. [código RPC=-32000 | método=sendTransaction | contexto=tx_size=15, max_retries=5]]

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_invalid_account_error_is_friendly

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_balance
- What: (no docstring found)
- Result:
  - exception: Falha inesperada ao executar getBalance. [método=getBalance | contexto=address=bad-account, endpoint=https://api.devnet.solana.com | causa=Parâmetros inválidos ao executar getBalance. Revise os valores enviados. [código RPC=-32602 | método=getBalance | contexto=address=bad-account]]

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_no_retry_on_fatal_rpc_error

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._call
- What: (no docstring found)
- Result:
  - exception: Falha inesperada ao executar getHealth. [método=getHealth | contexto=endpoint=https://api.devnet.solana.com | causa=Requisição RPC inválida. Verifique os parâmetros enviados. [código RPC=-32600 | método=getHealth]]
  - sleep_calls: 0

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_retry_exhausted_on_network_error

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._call
- What: (no docstring found)
- Result:
  - exception: Falha de comunicação ao executar getHealth após 3 tentativas. [método=getHealth | contexto=endpoint=https://api.devnet.solana.com | causa=refused]
  - sleep_calls: 2
  - urlopen_calls: 3

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_retry_on_http_429

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._call
- What: (no docstring found)
- Result:
  - result: ok
  - urlopen_calls: 3
  - sleep_calls: 2

## solinpy/client/test_client.py - TestRPCRetryAndTimeout - test_timeout_applied_to_config

- File: [solinpy/client/test_client.py](solinpy/client/test_client.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCConfig.timeout
- What: (no docstring found)
- Result:
  - timeout: 5.0

## solinpy/tests/test_account_decoder.py - TestBase64Decoding - test_decode_base64_to_bytes

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_base64_to_bytes
- What: (no docstring found)
- Result:
  - result: hello world

## solinpy/tests/test_account_decoder.py - TestBase64Decoding - test_decode_invalid_base64

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_base64_to_bytes
- What: (no docstring found)
- Result:
  - exception: Falha ao decodificar base64: Incorrect padding

## solinpy/tests/test_account_decoder.py - TestBase64Decoding - test_encode_bytes_to_base64

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_bytes_to_base64
- What: (no docstring found)
- Result:
  - result: dGVzdA==

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_pubkey

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_pubkey_from_bytes
- What: (no docstring found)
- Result:
  - result: So11111111111111111111111111111111111111112

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_pubkey_insufficient_bytes

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_pubkey_from_bytes
- What: (no docstring found)
- Result:
  - exception: Dados insuficientes para pubkey: precisa de 32 bytes, disponível 5

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u64

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u64_from_bytes
- What: (no docstring found)
- Result:
  - result: 1000000000

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u64_big_endian

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u64_from_bytes
- What: (no docstring found)
- Result:
  - result: 1000000000

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u64_insufficient_bytes

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u64_from_bytes
- What: (no docstring found)
- Result:
  - exception: Dados insuficientes para u64: precisa de 8 bytes, disponível 5

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u32

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u32_from_bytes
- What: (no docstring found)
- Result:
  - result: 4294967295

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u32_insufficient_bytes

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u32_from_bytes
- What: (no docstring found)
- Result:
  - exception: Dados insuficientes para u32: precisa de 4 bytes, disponível 2

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u8

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u8_from_bytes
- What: (no docstring found)
- Result:
  - result: 255

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_u8_insufficient_bytes

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_u8_from_bytes
- What: (no docstring found)
- Result:
  - exception: Dados insuficientes para u8: precisa de 1 byte, disponível 0

## solinpy/tests/test_account_decoder.py - TestByteParsing - test_parse_with_offset

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: parse_pubkey_from_bytes
- What: (no docstring found)
- Result:
  - result: So11111111111111111111111111111111111111112

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_account_basic

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - program: SPL Token
  - amount: 1000000000
  - state: initialized
  - is_native: False

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_account_with_delegate

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - program: SPL Token
  - delegate: None

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_account_frozen

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - state: frozen

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_account_native

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - program: SPL Token
  - amount: 1000000000

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_account_invalid_size

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - exception: Dados SPL Token inválidos: esperado 72 bytes, recebido 9

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_mint_basic

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_mint
- What: (no docstring found)
- Result:
  - program: SPL Token Mint
  - supply: 1000000000
  - decimals: 9
  - is_initialized: True

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_mint_with_authorities

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_mint
- What: (no docstring found)
- Result:
  - mint_authority: 11111111111111111111111111111111
  - freeze_authority: 11111111111111111111111111111111

## solinpy/tests/test_account_decoder.py - TestSPLTokenDecoding - test_decode_spl_token_mint_invalid_size

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_mint
- What: (no docstring found)
- Result:
  - exception: Dados Mint SPL Token inválidos: esperado 82 bytes, recebido 9

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_decode_dict_data

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: jsonParsed
  - parsed_data:
    - key: value

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_decode_string_data

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: raw
  - encoding: string

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_decode_base64_string

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: raw
  - encoding: bytes

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_auto_detect_spl_token

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: raw
  - encoding: bytes

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_auto_detect_spl_token_mint

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: SPL Token Mint

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_explicit_program_type

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: System Program
  - data_length: 9

## solinpy/tests/test_account_decoder.py - TestGenericAccountDecoding - test_unknown_program_type

- File: [solinpy/tests/test_account_decoder.py](solinpy/tests/test_account_decoder.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - program: raw
  - data_hex: 736f6d652064617461

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_create_airdrop_devnet_success

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: create_airdrop
- What: Testa solicitação via create_airdrop com sucesso.
- Result:
  - signature: fake_signature_create
  - confirmed: True
  - balance: 1000000000

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_devnet_success

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa solicitação de airdrop na devnet com sucesso.
- Result:
  - signature: fake_signature_123
  - confirmed: True
  - balance: 1000000000

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_testnet_success

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa solicitação de airdrop na testnet com sucesso.
- Result:
  - signature: fake_signature_456
  - confirmed: True
  - balance: 2000000000

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_invalid_cluster

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa se ValueError é levantado para clusters inválidos.
- Result:
  - exception: Airdrop disponível apenas para 'devnet' ou 'testnet'. Recebido: 'mainnet'

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_custom_lamports

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa solicitação de airdrop com quantidade customizada de lamports.
- Result:
  - signature: fake_signature_789
  - confirmed: True
  - balance: 500000000

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_timeout_error

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa se TimeoutError é levantado quando o airdrop não é confirmado.
- Result:
  - exception: Airdrop não foi confirmado dentro do timeout de 0.1s. Assinatura: fake_signature_timeout

## solinpy/tests/test_airdrop.py - TestRequestAirdrop - test_airdrop_polling_until_confirmed

- File: [solinpy/tests/test_airdrop.py](solinpy/tests/test_airdrop.py)
- Status: PASSED
- Duration: 0.00 s
- Target: request_airdrop
- What: Testa que a função faz polling até o airdrop ser confirmado.
- Result:
  - signature: fake_signature_polling
  - confirmed: True
  - balance: 1000000000
  - call_count: 5

## solinpy/tests/test_coverage_boost.py - test_rpc_config_post_init_with_aliases

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCConfig.__post_init__
- What: (no docstring found)
- Result:
  - cluster: devnet
  - max_retries: 7
  - base_delay: 0.25
  - timeout: 10.0

## solinpy/tests/test_coverage_boost.py - test_rpc_config_post_init_without_aliases

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCConfig.__post_init__
- What: (no docstring found)
- Result:
  - cluster: devnet
  - max_retries: 4
  - base_delay: 0.5
  - retries: 4
  - backoff_factor: 0.5

## solinpy/tests/test_coverage_boost.py - test_format_context_empty_and_filtered

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: _format_context
- What: (no docstring found)
- Result:
  - empty: 
  - filtered: a=1

## solinpy/tests/test_coverage_boost.py - test_rpc_error_str_without_details

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCError.__str__
- What: (no docstring found)
- Result:
  - string: plain

## solinpy/tests/test_coverage_boost.py - test_rpc_error_from_rpc_error_with_data

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCError.from_rpc_error
- What: (no docstring found)
- Result:
  - code: None
  - context:
    - request_id: 1
    - rpc_data: {'k': 'v'}
  - string: Método RPC desconhecido em getX. Verifique o nome da operação. [método=getX | contexto=request_id=1, rpc_data={'k': 'v'}]

## solinpy/tests/test_coverage_boost.py - test_rpc_error_from_transport_default_message

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: RPCError.from_transport_error
- What: (no docstring found)
- Result:
  - string: Falha de comunicação ao executar getX. Verifique o endpoint e tente novamente. [método=getX | causa=boom]

## solinpy/tests/test_coverage_boost.py - test_client_retryable_rpc_code_path

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient._is_retryable
- What: (no docstring found)
- Result:
  - retryable: True

## solinpy/tests/test_coverage_boost.py - test_client_retries_rpc_error_then_succeeds

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_health
- What: (no docstring found)
- Result:
  - result: ok
  - sleep_calls: 1

## solinpy/tests/test_coverage_boost.py - test_client_http_non_retryable_raises_transport_error

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_health
- What: (no docstring found)
- Result:
  - exception: Falha HTTP ao executar getHealth. Verifique o endpoint configurado. [método=getHealth | contexto=endpoint=https://api.devnet.solana.com | causa=HTTP Error 400: Bad Request]

## solinpy/tests/test_coverage_boost.py - test_client_balance_and_token_methods

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_balance / get_token_accounts_by_owner
- What: (no docstring found)
- Result:
  - balance: 123
  - token_accounts: [{'id': 1}]
  - first_call: ('getBalance', ['address'], {'address': 'address'})
  - second_call: ('getTokenAccountsByOwner', ['owner', {'programId': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'}, {'encoding': 'jsonParsed', 'commitment': 'confirmed'}], {'address': 'owner'})

## solinpy/tests/test_coverage_boost.py - test_client_sol_and_token_balances_helpers

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: SolanaRPCClient.get_sol_balance / get_token_balances
- What: (no docstring found)
- Result:
  - sol_balance: 2.5
  - token_balances: [{'mint': 'Mint1', 'amount': 4.2, 'decimals': 6}]

## solinpy/tests/test_coverage_boost.py - test_mnemonic_import_from_mnemonic_success

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: import_from_mnemonic
- What: (no docstring found)
- Result:
  - pubkey_1: HAgk14JpMQLgt6rVgv7cBQFJWFto5Dqxi472uT3DKpqk
  - pubkey_2: HAgk14JpMQLgt6rVgv7cBQFJWFto5Dqxi472uT3DKpqk
  - same_pubkey: True

## solinpy/tests/test_coverage_boost.py - test_mnemonic_import_validation_errors

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: import_from_mnemonic
- What: (no docstring found)
- Result:
  - errors: [{'input': '123', 'exception': 'Mnemonic must be a string'}, {'input': 'too short', 'exception': 'Invalid mnemonic length: must be 12, 18 or 24 words'}, {'input': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon invalid', 'exception': 'Invalid mnemonic: checksum or wordlist mismatch'}]

## solinpy/tests/test_coverage_boost.py - test_derive_slip10_ed25519_path_validation_and_output

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: _derive_slip10_ed25519
- What: (no docstring found)
- Result:
  - errors: [{'path': "x/44'/501'/0'/0'", 'exception': "Derivation path must start with 'm'"}, {'path': "m/44'/501'/0'/0", 'exception': "Ed25519 derivation requires hardened indices (e.g., 0')"}]
  - key_len: 32

## solinpy/tests/test_coverage_boost.py - test_decode_spl_token_account_all_optional_fields

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_spl_token_account
- What: (no docstring found)
- Result:
  - delegate: 11111111111111111111111111111111
  - state: unknown(7)
  - is_native: True
  - native_amount: 999
  - close_authority: SysvarRent111111111111111111111111111111111

## solinpy/tests/test_coverage_boost.py - test_decode_account_data_fallback_paths

- File: [solinpy/tests/test_coverage_boost.py](solinpy/tests/test_coverage_boost.py)
- Status: PASSED
- Duration: 0.00 s
- Target: decode_account_data
- What: (no docstring found)
- Result:
  - unknown:
    - program: raw
    - data: 12345
    - encoding: unknown
  - mint_fallback:
    - program: raw
    - data_hex: 73686f7274
    - data_length: 5
    - encoding: bytes

## solinpy/tests/test_devnet_integration.py - TestDevnetIntegration - test_devnet_airdrop_and_account_read

- File: [solinpy/tests/test_devnet_integration.py](solinpy/tests/test_devnet_integration.py)
- Status: SKIPPED
- Duration: 0.00 s
- Target: Devnet integration run
- What: (no docstring found)
- Result:
  - wallet: GseYkvXZ572qoJnPZ3mzebZXdMjgCoF5JAeMbDTmjCkd
  - source: funded-wallet
  - signature: 59hybunCCVd2woa4t4EtTtnC5a6MpKTLKwPGvyxFgERbRzqXa9ZHPXxUowo1sdZQTan4UoEfCTFgd4xEsqxmAYhN
  - confirmed: True
  - balance_lamports: 100000000
  - balance_sol: 0.1

## solinpy/tests/test_devnet_integration.py - TestDevnetIntegration - test_devnet_send_sol_between_wallets

- File: [solinpy/tests/test_devnet_integration.py](solinpy/tests/test_devnet_integration.py)
- Status: SKIPPED
- Duration: 0.00 s
- Target: Devnet integration run
- What: (no docstring found)
- Result:
  - sender: DRsudJVgb6YmVWRc2eJ1XmxXFsTAa2gzufrPXikAPnU8
  - receiver: 4fNDSPnkLQgXRcMfyLDiLMXbBtM9dEX9MHvE4GcPU3VQ
  - funding_source: funded-wallet
  - signature: 52Xj5usvrau1dMdsSqTQfW7UG8iTeaNfKgotSQxmUYDfp9PVU3q3GykLx9ajbrroeoT6ko3cvzArLwK8muFubXBx
  - sender_before: 100000000
  - sender_after: 89995000
  - receiver_before: 0
  - receiver_after: 10000000
  - transferred_lamports: 10000000

## solinpy/tests/test_devnet_integration.py - TestDevnetIntegration - test_generate_wallet_returns_valid_keypair

- File: [solinpy/tests/test_devnet_integration.py](solinpy/tests/test_devnet_integration.py)
- Status: SKIPPED
- Duration: 0.00 s
- Target: WalletManager.generate_keypair
- What: (no docstring found)
- Result:
  - public_key: QnnNEpmPCEWhaexBh48TzNN2uvtMgMmh14hee7M5UqC
  - secret_key_bytes: 64 bytes

## solinpy/tests/test_token.py - test_get_associated_token_address_matches_program_derivation

- File: [solinpy/tests/test_token.py](solinpy/tests/test_token.py)
- Status: PASSED
- Duration: 0.00 s
- Target: get_associated_token_address
- What: (no docstring found)
- Result:
  - derived: 6Sg2uXn8Y2PbHJTn2diEAoLLyDkaUJypqB2v5h9p8aq7
  - expected: 6Sg2uXn8Y2PbHJTn2diEAoLLyDkaUJypqB2v5h9p8aq7
  - matches: True

## solinpy/tests/test_token.py - test_send_token_transfer_creates_receiver_ata_when_missing

- File: [solinpy/tests/test_token.py](solinpy/tests/test_token.py)
- Status: PASSED
- Duration: 0.00 s
- Target: send_token_transfer
- What: (no docstring found)
- Result:
  - signature: tx-sig
  - receiver_ata_created: True
  - sender_ata: 11111111111111111111111111111111
  - receiver_ata: SysvarRent111111111111111111111111111111111

## solinpy/tests/test_token.py - test_send_token_transfer_skips_receiver_ata_creation_when_present

- File: [solinpy/tests/test_token.py](solinpy/tests/test_token.py)
- Status: PASSED
- Duration: 0.00 s
- Target: send_token_transfer
- What: (no docstring found)
- Result:
  - signature: tx-sig-2
  - receiver_ata_created: False
  - sender_ata: 11111111111111111111111111111111
  - receiver_ata: SysvarRent111111111111111111111111111111111

## solinpy/tests/test_wallet.py - test_generate_keypair

- File: [solinpy/tests/test_wallet.py](solinpy/tests/test_wallet.py)
- Status: PASSED
- Duration: 0.00 s
- Target: WalletManager.generate_keypair
- What: Test if a valid keypair is generated.
- Result:
  - public_key: GwhaCEWG9DKGYM31WTzTmWx15iqcJq9KHKUWnk7v3uTu
  - secret_len: 64

## solinpy/tests/test_wallet.py - test_import_from_json

- File: [solinpy/tests/test_wallet.py](solinpy/tests/test_wallet.py)
- Status: PASSED
- Duration: 0.00 s
- Target: WalletManager.import_from_json
- What: Test importing a keypair from a generated JSON file.
- Result:
  - original_pubkey: 6SKwxWwp6avnnP1uNeSGvus4dcSq4NejEXKA1zMYEEcq
  - imported_pubkey: 6SKwxWwp6avnnP1uNeSGvus4dcSq4NejEXKA1zMYEEcq

## solinpy/tests/test_wallet.py - test_import_from_json_file_not_found

- File: [solinpy/tests/test_wallet.py](solinpy/tests/test_wallet.py)
- Status: PASSED
- Duration: 0.00 s
- Target: WalletManager.import_from_json
- What: Test if the proper error is raised when file is missing.
- Result:
  - exception: File not found: non_existent_path.json

## solinpy/tests/test_wallet.py - test_import_from_json_invalid_format

- File: [solinpy/tests/test_wallet.py](solinpy/tests/test_wallet.py)
- Status: PASSED
- Duration: 0.00 s
- Target: WalletManager.import_from_json
- What: Test if ValueError is raised for non-list JSON.
- Result:
  - exception: Invalid JSON format: expected a list of bytes
