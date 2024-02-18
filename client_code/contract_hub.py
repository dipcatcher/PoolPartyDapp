import anvil.server
from anvil.tables import app_tables

# old party 0x2498e8059929e18e2a2cED4e32ef145fa2F4a744

def contract_data():
  contract_data = {}
  contract_data['NAMECLAIM']     = {'address':"0x8b39b9b6fEe1854a585321fBd3b2BAB49cFB2359", "abi":[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"burner","type":"address"},{"indexed":False,"internalType":"string","name":"name","type":"string"}],"name":"Claim","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ConvertPoints","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"flusher","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Flush","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"minter","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"CLAIM_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"IS_ACTIVE","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTING_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"NAME_CLAIMER_AIRDROP_POINTS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"NAME_OWNERS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"_checkName","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"activate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"activator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"ticker_name","type":"string"}],"name":"claimName","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"convertToAirdropPoints","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"donezo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"flush","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token_contract_address","type":"address"}],"name":"flush_erc20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"flusher","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"name","type":"string"}],"name":"unavailable","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]}
  contract_data['PARTY'] = {}
  contract_data['NAME_NFT'] = {}
  contract_data['POOL_DEPLOYER'] = {}
  contract_data['REWARD_DISTRIBUTION'] = {}
  contract_data['PARTY']['address']="0x1757a98c1333B9dc8D408b194B2279b5AFDF70Cc"
  contract_data['REWARD_DISTRIBUTION']['address']="0x2BD787434c527C13Dc633557b7Bc40247F8e50f7"
  contract_data['NAME_NFT']['address']="0x4220758a30619786163bE50311b6a42ea239751B"
  contract_data['POOL_DEPLOYER']['address']="0x6484EB0792c646A4827638Fc1B6F20461418eB00"
  contract_data['HEX']={}
  contract_data['HEX']['address']="0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39"
  contract_data['PERPETUAL_POOL']={}
  contract_data['HDRN']={'address':"0x3819f64f282bf135d62168C1e513280dAF905e06"}
  contract_data['TEAM']={'address':"0xB7c9E99Da8A857cE576A830A9c19312114d9dE02"}
  contracts = app_tables.contract.search()
  for c in contracts:
    contract_data[c['name']]['abi']=c['abi']
  return contract_data

