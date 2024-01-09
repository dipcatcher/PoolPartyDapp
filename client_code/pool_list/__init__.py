from ._anvil_designer import pool_listTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..pool_page import pool_page
class pool_list(pool_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    self.current_hex_day = int(self.hex_contract_read.currentDay().toString())
    self.contract = get_open_form().get_contract_read("POOL_DEPLOYER")
    pool_deploy_events = anvil.js.await_promise(self.contract.queryFilter('PoolDeployment'))
    '''event PoolDeployment(string ticker, uint256 initial_mint_duration, 
                        uint256 stake_duration, 
                        uint256 reload_duration,
                        string name, 
                        uint256 organizer_share, address organizer_address, address pool_address);'''
    self.all_active_pools = []
    self.all_staked_pools = []
    for e in pool_deploy_events: 
      pool_data = {}
      pool_data['ticker'] = e['args'][0]
      pool_data['initial_mint_duration']= int(e['args'][1].toString())
      pool_data['stake_duration']= int(e['args'][2].toString())
      pool_data['reload_duration']= int(e['args'][3].toString())
      pool_data['name']= e['args'][4]
      pool_data['organizer_share']= int(e['args'][5].toString())
      pool_data['organizer_address']= e['args'][6]
      pool_data['pool_address']= e['args'][7]
      for k,v in self.get_pool_data(pool_data['pool_address']).items():
        pool_data[k] = v
      if not pool_data["can join now"]:
        self.all_staked_pools.append(pool_data)
      else:
        self.all_active_pools.append(pool_data)
      
      if "goto" in properties:
        ticker = properties['goto']
        if ticker ==pool_data['ticker']:
          target_pool_data = pool_data
    if "goto" in properties:
  
      self.clear()
      self.add_component(pool_page(pool_data =target_pool_data ))
    else:
      self.repeating_panel_1.items=self.all_active_pools
      self.repeating_panel_is_staked.items = self.all_staked_pools
    # Any code you write here will run before the form opens.
  def get_pool_data(self, pool_address):
    data = {}
    self.read_contract = get_open_form().get_perpetual_pool_contract_read(pool_address)
    data['name']=self.read_contract.name()
    data['liquid supply']=int(self.read_contract.totalSupply().toString())
    data['timelocked supply'] = int(self.read_contract.timelockedSupply().toString())
    data['penalty pool supply']=int(self.read_contract.penaltyPoolSupply().toString())
    data['complete total supply'] = int(self.read_contract.completeTotalSupply().toString())
    data['hdrn balance'] = int(get_open_form().get_contract_read("HDRN").balanceOf(pool_address).toString())
    data['current hex day']=int(self.read_contract.getHexDay().toString())
    data['current period']=int(self.read_contract.CURRENT_PERIOD().toString())
    data['current stake principal']=int(self.read_contract.CURRENT_STAKE_PRINCIPAL().toString())
    data['reload phase duration']=int(self.read_contract.RELOAD_PHASE_DURATION().toString())
    data['redemption rate']=int(self.read_contract.HEX_REDEMPTION_RATE().toString())
    data['reload phase start']=int(self.read_contract.RELOAD_PHASE_START().toString())
    data['reload phase end']=int(self.read_contract.RELOAD_PHASE_END().toString())
    data['stake start day']=int(self.read_contract.STAKE_START_DAY().toString())
    
    data['can join now'] = self.current_hex_day<=data['reload phase end']
    data['stake end day']=int(self.read_contract.STAKE_END_DAY().toString())
    data['stake is active']=self.read_contract.STAKE_IS_ACTIVE()
    data['stake length']=int(self.read_contract.STAKE_LENGTH().toString())
    data['global timelocked token days per period'] = [int(self.read_contract.globalTimelockedTokenDaysPerPeriod(n).toString()) for n in range(data['current period']+1)]
    data['global time locked tokens per period']= [int(self.read_contract.globalTimelockedTokensPerPeriod(n).toString()) for n in range(data['current period']+1)]
    data['penalty pool per period'] = [int(self.read_contract.penaltyPoolPerPeriod(n).toString()) for n in range(data['current period']+3)]
    data['is staking period']=self.read_contract.isStakingPeriod()
    data['days until stake end'] = data['stake end day']- data['current hex day']
    return data
