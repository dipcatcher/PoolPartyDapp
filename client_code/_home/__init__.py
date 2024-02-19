from ._anvil_designer import _homeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from datetime import datetime
from ..nft_display import nft_display
from .. import contract_hub as ch
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False
#pages

from ..stake_party import stake_party
from ..airdrop import airdrop
from ..nft_claim import nft_claim
from ..create_stake_pool import create_stake_pool
from ..ticker_auctions import ticker_auctions
from ..pool_list import pool_list
from ..party_rewards import party_rewards
from ..pool_page import pool_page
from ..buy_party import buy_party
from ..user_wallet import user_wallet
from anvil.js.window import ethers

pulsechain_url = "http://127.0.0.1:8545"#"https://rpc.v4.testnet.pulsechain.com"
ethereum_url ="https://rpc.v4.testnet.pulsechain.com"#  "https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"

class _home(_homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.activate_default_providers()
    self.nameclaim_contract = self.get_contract_read("NAMECLAIM")
    

  def activate_default_providers(self):
    self.default_network = "PLS"
    self.current_network=self.default_network
    urls = {"PLS":pulsechain_url, "ETH":ethereum_url}
    self.providers = {}
    self.providers['ETH'] = ethers.providers.JsonRpcProvider(urls["ETH"])
    self.providers["PLS"]= ethers.providers.JsonRpcProvider(urls["PLS"])
    self.contract_data = ch.contract_data()
  
  def events_catalog(self, event_name, from_block = 0, to_block = "latest"):
    party_contract_read = self.get_contract_read("PARTY")
    party_abi = contract_data = self.contract_data["PARTY"]['abi']
    # TODO: return event query results of the input event_name. The event_name should be in the available events from the party_abi.
    event_names = [event['name'] for event in party_abi if event['type'] == 'event']
    
    if event_name not in event_names:
        raise ValueError(f"The event {event_name} is not in the ABI.")
    
    # Query the event logs
    event_filter = party_contract_read.filters[event_name]()
    logs = party_contract_read.queryFilter(event_filter, fromBlock=from_block, toBlock=to_block)
    
    # Process the logs to extract useful information (if needed)
    processed_logs = [log.args for log in logs]  # Replace with your own logic if necessary
    
    return processed_logs
  def get_contract_read(self, ticker):
    chain = "PLS"
    contract_data = self.contract_data[ticker]
    return ethers.Contract(contract_data['address'], contract_data['abi'], self.providers[chain])
  def get_perpetual_pool_contract_write(self, address):
    return ethers.Contract(address, ch.contract_data()['PERPETUAL_POOL']['abi'],self.metamask.signer)
  def get_perpetual_pool_contract_read(self, address):
    chain = "PLS"
    return ethers.Contract(address, ch.contract_data()['PERPETUAL_POOL']['abi'],self.providers[chain])
      
  def get_contract_write(self, ticker):
    
    contract_data = self.contract_data[ticker]
    return ethers.Contract(contract_data['address'], contract_data['abi'],self.metamask.signer)
  def button_switch_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.connected_chain in [1]:
      self.current_network = "ETH" 
    elif self.connected_chain in [369, 31337]:
      self.current_network = "PLS"
      
    '''c = confirm("You are currently connected to {}.".format(self.current_network),title="Choose Network",buttons=[("Ethereum", True), ("Pulsechain", False)])
    if c:
      chain_id = "0x1"
    else:
      chain_id = "0x171"
    try:
      a = ethereum.request({
                'method': 'wallet_switchEthereumChain',
                'params': [{ "chainId": chain_id }] 
            })
      b = anvil.js.await_promise(a)
      
    except Exception as e:
      raise e
      alert("Connect to the network you want in your wallet and refresh the page.")'''
    self.metamask.update_signer()
    self.metamask_connect()
    self.menu_click(sender=self.latest)    
    
    # Any code you write here will run before the form opens.

  def menu_click(self, **event_args):
    self.content_panel.clear()
    not_yet =[]# [self.link_create_stake_pool,  self.button_pools]
    if event_args['sender'] in not_yet:
      alert("The '{}' feature will be available when testnet Stage 2 begins.".format(event_args['sender'].text))
      return False
    self.latest = event_args['sender']
    
    if event_args['sender'] == self.link_stake:
      self.page = stake_party()
    elif event_args['sender'] == self.link_mint_nft:
      self.page = nft_claim()
    elif event_args['sender'] == self.link_ticker_auctions:
      self.page = ticker_auctions()
    elif event_args['sender'] == self.link_claim:
      self.page = airdrop()
    elif event_args['sender'] == self.link_create_stake_pool:
      self.page = create_stake_pool()

    elif event_args['sender']==self.button_pools:
      
      self.content_panel.add_component(Label(align="center",text="Loading Pools...", icon="https://media.giphy.com/media/fphXG8dDcRHVavls9o/giphy.gif", role='headline'))
      
      if "goto" in event_args:
        self.page = pool_list(goto=event_args['goto'])
      else:
        self.page = pool_list()
      self.content_panel.clear()
    elif event_args['sender']==self.link_party_rewards_manage:
      self.page = party_rewards()
    
    elif event_args['sender']==self.link_wallet:
      self.page = user_wallet()
    
  
    
    if len(self.pool_panel.get_components())>0:
      if 'is_btn' not in event_args:
        if self.content_panel.visible ==False:
          self.pool_panel.clear()
          self.content_panel.visible = True
    
    self.content_panel.add_component(self.page)

  def link_disclaimer_click(self, **event_args):
    """This method is called when the link is clicked"""
    text = '''
    You are responsible for your actions, no one else.
    '''
    alert(text)

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    self.menu_click(sender=self.link_claim)
  def check_merkle(self):
    data =app_tables.pool_party_merkle.search()#app_tables.party_merkle_host.get(name="Supply Merkle")['proofs']
    self.contract_read = self.get_contract_read("PARTY")
    total = 0
    for r in data:
      verify= self.contract_read.verifyInitialSupplyPoints(r['merkle_proof'], r['address'], r['party_mintable'])
      if verify==False:
        print(r)
      total+=int(r['party_mintable'])
    print(total/(10**18))


  def metamask_connect(self, **event_args):
    self.connected_chain = self.metamask.provider.getNetwork()['chainId']
    print(self.connected_chain)
    self.button_switch.visible = True
    if self.connected_chain==1:
      self.button_switch.text = "ETH" 
    elif self.connected_chain in [369, 943, 31337]:
      self.button_switch.text = "PLS"
    self.menu_click(sender=self.latest, is_btn=True)
    if len(self.pool_panel.get_components())>0:
      print("OK")
      self.pool_panel.get_components()[0].refresh()
      self.pool_panel.get_components()[0].display.refresh()
  def link_switch_network_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def block_to_time(self, block_number):
    # Convert the block number to a block'chain
    chain = self.button_switch.text
    block = anvil.js.await_promise(self.providers[chain].getBlock(block_number))
    
    timestamp = block['timestamp']
    
    dt_object = datetime.fromtimestamp(timestamp)
    
    return dt_object

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if ethereum is not None:
      ethereum.request(
        dict(method='wallet_addEthereumChain',
        params=[
          {
            'chainId': '0x3AF',  # 31337 in hexadecimal
            'chainName': 'PulseChain Testnet V4',
            'nativeCurrency': {
              'name': 'tPLS',
              'symbol': 'tPLS',
              'decimals': 18,
            },
            'rpcUrls': ['https://rpc.v4.testnet.pulsechain.com'],
          },
        ],
      ))
    else:
      print('MetaMask is not installed. Please install it and try again.')
  def abbreviate_number(self, number):
    """
    Abbreviates a number based on its order of magnitude.
    - K for thousands
    - M for millions
    - B for billions
    - T for trillions
    Returns a string with the abbreviated number.
    """
    if number < 1000:
        return str(number)
    elif number < 1_000_000:  # Thousands
        return f"{number / 1_000:.3f}K"
    elif number < 1_000_000_000:  # Millions
        return f"{number / 1_000_000:.3f}M"
    elif number < 1_000_000_000_000:  # Billions
        return f"{number / 1_000_000_000:.3f}B"
    else:  # Trillions
        return f"{number / 1_000_000_000_000:.3f}T"
  def button_buy_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    alert(buy_party(), buttons=[])


  