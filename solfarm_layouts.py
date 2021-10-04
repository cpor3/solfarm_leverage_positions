from construct import Bytes, Padding, Int64ul, Int32ul, Int8ul, Struct
from construct.core import BytesInteger, Flag

VAULT_LAYOUT = Struct(
    Padding(8),
    "authority" / Bytes(32),
    "token_program" / Bytes(32),
    "pda_token_account" / Bytes(32),
    "pda" / Bytes(32),
    "nonce" / Int8ul,
    "info_nonce" / Int8ul,
    "reward_a_nonce" / Int8ul,
    "reward_b_nonce" / Int8ul,
    "swap_to_nonce" / Int8ul,
    "total_vault_balance" / Int64ul,
    "info_account" / Bytes(32),
    "lp_token_account" / Bytes(32),
    "lp_token_mint" / Bytes(32),
    "reward_a_account" / Bytes(32),
    "reward_b_account" / Bytes(32),
    "swap_to_account" / Bytes(32),
    "total_vlp_shares" / Int64ul
)

MINT_LAYOUT = Struct(
  "mintAuthorityOption" / Int32ul,
  "mintAuthority" / Bytes(32),
  "supply" / Int64ul,
  "decimals" / Int8ul,
  "initialized" / Flag,
  "freezeAuthorityOption" / Int32ul,
  "freezeAuthority" / Bytes(32)
)

LENDING_OBLIGATION_LAYOUT = Struct(
  "version" / Int8ul,
  "lastUpdateSlot" / Struct("slot" / Int64ul, "stale" / Flag),
  "lendingMarket" / Bytes(32),
  "owner" / Bytes(32),
  "borrowedValue" / BytesInteger(16),
  "vaultShares" / Int64ul, 
  "lpTokens" / Int64ul, 
  "coinDeposits" / Int64ul, 
  "pcDeposits" / Int64ul, 
  "depositsMarketValue" / BytesInteger(16),
  "lpDecimals" / Int8ul,
  "coinDecimals" / Int8ul,
  "pcDecimals" / Int8ul,
  "depositsLen" / Int8ul,
  "borrowsLen" / Int8ul,
  Padding(160)
)