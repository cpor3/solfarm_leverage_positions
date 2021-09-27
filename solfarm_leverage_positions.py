from solfarm_layouts import VAULT_LAYOUT, LENDING_OBLIGATION_LAYOUT
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solfarm_vaults import Solfarm_Vault
import base64

SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com'
SOLFARM_LEVERAGE_PROGRAM_ID = 'Bt2WPMmbwHPk36i4CRucNDyLcmoGdC7xEdrVuxgJaNE6'

def main():
    """
    Solana Python API built on the JSON RPC API:
    https://github.com/michaelhly/solana-py

    """

    # Public Key with a Solfarm RAY-SOL Leverage Position
    user_public_key = 'F7oXPREyRXFYUCPA12Z33pmdCFfAJtBeHhFhQFeJRYAp' 
    print('public key:', user_public_key)

    # RAY-USDT vault
    vault = Solfarm_Vault.RayUsdtVault
    vault_account = '1ZpdBUTiDLTUe3izSdYfRXSf93fpJPmoKtA5bFjGesS' # RAY-USDT account, from https://gist.github.com/therealssj/c6049ac59863df454fb3f4ff19b529ee#file-solfarm_ray_vault-json-L816
    LP_decimals = 6

    # Get vault info
    solana = Client(SOLANA_ENDPOINT)
    vault_raw_data = solana.get_account_info(vault_account, commitment='confirmed')
    vault_decoded_data = VAULT_LAYOUT.parse(base64.b64decode(vault_raw_data['result']['value']['data'][0]))
    total_vault_balance = vault_decoded_data.total_vault_balance / (10 ** LP_decimals)
    total_vault_shares = vault_decoded_data.total_vlp_shares
    print('total_vault_balance:', total_vault_balance)
    print('total_vlp_shares:', total_vault_shares)
    
    # Find user farm account
    seeds = [bytes(PublicKey(user_public_key)), bytearray(8), bytearray([vault,0,0,0,0,0,0,0])]
    program_id = PublicKey(SOLFARM_LEVERAGE_PROGRAM_ID)
    user_farm_address, nonce = PublicKey.find_program_address(seeds=seeds, program_id=program_id)
    print('user_farm_address:', user_farm_address)
    
    # Find user obligation account [0, 1, 2]
    obligation_index = 0
    seeds = [bytes(PublicKey(user_public_key)), bytes(user_farm_address), bytearray([obligation_index,0,0,0,0,0,0,0])]
    user_obligation_address, nonce = PublicKey.find_program_address(seeds=seeds, program_id=program_id)
    print('user_obligation_address:', user_obligation_address)

    # Get user shares and tokens
    user_leverage_raw_data = solana.get_account_info(user_obligation_address, commitment='confirmed') 
    user_leverage_decoded_data = LENDING_OBLIGATION_LAYOUT.parse(base64.b64decode(user_leverage_raw_data['result']['value']['data'][0]))
    user_leverage_LP_shares = user_leverage_decoded_data.vaultShares
    user_leverage_LP_tokens = total_vault_balance * (user_leverage_LP_shares / total_vault_shares)
    print('user_leverage_LP_shares:', user_leverage_LP_shares)
    print('user_leverage_LP_tokens:', user_leverage_LP_tokens)

    # Coin and pc deposits
    coin_decimals = user_leverage_decoded_data.coinDecimals
    pc_decimals = user_leverage_decoded_data.pcDecimals
    user_coin_deposits = user_leverage_decoded_data.coinDeposits / (10 ** coin_decimals)
    user_pc_deposits = user_leverage_decoded_data.pcDeposits / (10 ** pc_decimals)
    print('user_coin_deposits:', user_coin_deposits)
    print('user_pc_deposits:', user_pc_deposits)

if __name__ == '__main__':
    main()