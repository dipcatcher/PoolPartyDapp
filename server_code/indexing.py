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
  h=app_tables.contract.get(name="HEX")
  
  w3=getw3(chain)
  contract = w3.eth.contract(address=address, abi=abi)
  hex_contract = w3.eth.contract(address=h['address'], abi=h['abi'])
  
  data = {"RELOAD_PHASE_START":contract.functions.RELOAD_PHASE_START().call(),
          "RELOAD_PHASE_END":contract.functions.RELOAD_PHASE_END().call(),
          "STAKE_START_DAY":contract.functions.STAKE_START_DAY().call(),
          "STAKE_END_DAY":contract.functions.STAKE_END_DAY().call(), 
          "STAKE_LENGTH":contract.functions.STAKE_LENGTH().call(), 
          "STAKE_IS_ACTIVE":contract.functions.STAKE_IS_ACTIVE().call(), 
          "CURRENT_STAKE_PRINCIPAL":contract.functions.CURRENT_STAKE_PRINCIPAL().call(), 
          "latest_update":int(w3.eth.blockNumber),
          'RELOAD_PHASE_DURATION':contract.functions.RELOAD_PHASE_DURATION().call(),
          "STAKE_LENGTH":contract.functions.STAKE_LENGTH().call()
          
         }
  

  hdrn = app_tables.contract.get(name="HDRN")
  com = app_tables.contract.get(name="COM")
  
  data['hdrn balance'] = w3.eth.contract(address=hdrn['address'], abi= hdrn['abi']).functions.balanceOf(address).call()
  data['com balance'] =  w3.eth.contract(address=com['address'], abi= com['abi']).functions.balanceOf(address).call()
  data['hex balance'] = hex_contract.functions.balanceOf(address).call()
  data['name']=contract.functions.name().call()
  data['liquid supply']=contract.functions.totalSupply().call()
  data['current hex day']=contract.functions.getHexDay().call()
  data['current period']=contract.functions.CURRENT_PERIOD().call()
  data['current stake principal']=contract.functions.CURRENT_STAKE_PRINCIPAL().call()
  data['redemption rate']=contract.functions.HEX_REDEMPTION_RATE().call()
  data['days until stake end'] = data['STAKE_END_DAY']- data['current hex day']
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
  l = len(pools)
  n=1
  anvil.server.task_state = "{} of {} collected...".format(n, l)
  for pool in pools:
    
    data = check_pool( pool['chain'], pool['address'])
    indexed_data[pool['chain']][pool['ticker']] =data
    anvil.server.task_state = "{} of {} collected...".format(n, l)
    n+=1
  print('done')
  app_tables.indexed_data.get(name='pool_list').update(data=indexed_data)
  anvil.server.task_state = "DONE"
    
  
@anvil.server.callable
def run_check_pools():
  return anvil.server.launch_background_task('check_pools')

@anvil.server.callable
def run_check_pool(chain, address):
  return check_pool(chain, address)