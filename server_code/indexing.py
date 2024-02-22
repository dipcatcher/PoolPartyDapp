import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from web3 import Web3
import json

urls={"PLS":"https://rpc.pulsechain.com", "ETH":"https://eth-mainnet.g.alchemy.com/v2/dPnz2_vCX25Sr6ADV6EktoAORb67ryzm"}
def getw3(chain):
  w3 = Web3(Web3.HTTPProvider(urls[chain]))
  return w3

'''token = app_tables.tokens.get(ticker="TEAM")
  contract_address= token['address']
  contract_abi=token['abi']
  # Create contract instance
  w3=getw3(chain)
  contract = w3.eth.contract(address=contract_address, abi=contract_abi)'''

@anvil.server.background_task
def check_pool(chain, address):
  print(chain, address)
  abi = app_tables.contract.get(name="PERPETUAL_POOL")['abi']
  pool = app_tables.pool_data.get(address=address, chain=chain)
  
  w3=getw3(chain)
  contract = w3.eth.contract(address=address, abi=abi)
  data = {"RELOAD_PHASE_START":contract.functions.RELOAD_PHASE_START().call(),
          "RELOAD_PHASE_END":contract.functions.RELOAD_PHASE_END().call(),
          "STAKE_START_DAY":contract.functions.STAKE_START_DAY().call(),
          "STAKE_END_DAY":contract.functions.STAKE_END_DAY().call(), 
          "STAKE_LENGTH":contract.functions.STAKE_LENGTH().call(), 
          "STAKE_IS_ACTIVE":contract.functions.STAKE_IS_ACTIVE().call(), 
          "CURRENT_STAKE_PRINCIPAL":contract.functions.CURRENT_STAKE_PRINCIPAL().call(), 
          "latest_update":int(w3.eth.blockNumber)
         }
  pool.update(**data)
  re = data
  re['chain']=chain
  re['address']=address
  re['ticker']=pool['ticker']
  return  re

@anvil.server.background_task
def check_pools():
  pools = app_tables.pool_data.search()
  indexed_data = {"PLS": {}, "ETH":{}}
  for pool in pools:
    data = check_pool( pool['chain'], pool['address'])
    indexed_data[pool['chain']][pool['ticker']] =data
  app_tables.indexed_data.get(name='pool_list').update(data=indexed_data)
    
  
@anvil.server.callable
def run_check_pools():
  anvil.server.launch_background_task('check_pools')

