from ._anvil_designer import pool_listTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..pool_page import pool_page
import time
class pool_list(pool_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.props = properties
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    self.current_hex_day = int(self.hex_contract_read.currentDay().toString())
    self.contract = get_open_form().get_contract_read("POOL_DEPLOYER")
    self.pools = app_tables.indexed_data.get(name="pool_list")['data']
    self.refresh_display()
  def refresh_display(self):
    t0 = time.time()
    pool_deploy_events = anvil.js.await_promise(self.contract.queryFilter('PoolDeployment'))
    t1=time.time()
    print(t1-t0)
  
    '''event PoolDeployment(string ticker, uint256 initial_mint_duration, 
                        uint256 stake_duration, 
                        uint256 reload_duration,
                        string name, 
                        uint256 organizer_share, address organizer_address, address pool_address);'''
    self.all_active_pools = []
    self.all_staked_pools = []
    for e in pool_deploy_events: 
      _=time.time()
      pool_data = {}
      pool_data['ticker'] = e['args'][0]
      pool_data['initial_mint_duration']= int(e['args'][1].toString())
      pool_data['stake_duration']= int(e['args'][2].toString())
      pool_data['reload_duration']= int(e['args'][3].toString())
      pool_data['name']= e['args'][4]
      pool_data['organizer_share']= int(e['args'][5].toString())
      pool_data['organizer_address']= e['args'][6]
      pool_data['pool_address']= e['args'][7]
      __ = time.time()
      for k,v in self.get_pool_data(pool_data['pool_address'], pool_data['ticker']).items():
        pool_data[k] = v
      ___=time.time()
      print("event",__-_)
      print("query",___-__)
      if not pool_data["can join now"]:
        self.all_staked_pools.append(pool_data)
      else:
        self.all_active_pools.append(pool_data)
      
      if "goto" in self.props:
        ticker = self.props['goto']
        if ticker ==pool_data['ticker']:
          target_pool_data = pool_data
     
      print("event",__-_)
      print("query",___-__)
    t2=time.time()
    if "goto" in self.props:
  
      self.clear()
      self.add_component(pool_page(pool_data =target_pool_data ))
    else:
      self.repeating_panel_1.items=self.all_active_pools
      self.repeating_panel_is_staked.items = self.all_staked_pools
    t3=time.time()
    print(t2-t1)
    print(t3-t2)
    
    # Any code you write here will run before the form opens.
  def get_pool_data(self, pool_address, ticker):
    data = {}
   
    
    
    '''
    data['name']=self.read_contract.name()
    data['liquid supply']=int(self.read_contract.totalSupply().toString())
    data['hdrn balance'] = int(get_open_form().get_contract_read("HDRN").balanceOf(pool_address).toString())
    data['com balance'] = int(get_open_form().get_contract_read("COM").balanceOf(pool_address).toString())
    data['hex balance'] = int(get_open_form().get_contract_read("HEX").balanceOf(pool_address).toString())
    data['current hex day']=int(self.read_contract.getHexDay().toString())
    data['current period']=int(self.read_contract.CURRENT_PERIOD().toString())
    
    data['reload phase duration']=int(self.read_contract.RELOAD_PHASE_DURATION().toString())
    data['redemption rate']=int(self.read_contract.HEX_REDEMPTION_RATE().toString())
    data['reload phase start']=int(self.read_contract.RELOAD_PHASE_START().toString())
    
    data['stake start day']=int(self.read_contract.STAKE_START_DAY().toString())
    data['stake end day']=int(self.read_contract.STAKE_END_DAY().toString())
    data['stake is active']=self.read_contract.STAKE_IS_ACTIVE()
    data['stake length']=int(self.read_contract.STAKE_LENGTH().toString())
    data['days until stake end'] = data['stake end day']- data['current hex day']'''
    try:
      #p = app_tables.pool_data.get(chain = get_open_form().current_network, address=pool_address)
      p = self.pools[get_open_form().current_network][ticker]
      data['current stake principal']=p['CURRENT_STAKE_PRINCIPAL']
      data['reload phase end']=p['RELOAD_PHASE_END']
      data['can join now'] = self.current_hex_day<=data['reload phase end']
      data['stake is active']=p['STAKE_IS_ACTIVE']
      data['reload phase start']=p['RELOAD_PHASE_START']
      
      print(data)
      print(p)
      for k,v in p.items():
        data[k]=v
    except Exception as e:
      print(e)
      self.read_contract = get_open_form().get_perpetual_pool_contract_read(pool_address)
      data['current stake principal']=int(self.read_contract.CURRENT_STAKE_PRINCIPAL().toString())
      data['reload phase end']=int(self.read_contract.RELOAD_PHASE_END().toString())
      data['can join now'] = self.current_hex_day<=data['reload phase end']
    
    

    
    return data

  def button_refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].text = "Collecting Data..."
    event_args['sender'].enabled=False
    task = anvil.server.call('run_check_pools')
    while task.get_state() != "DONE":
      time.sleep(1)
      event_args['sender'].text = task.get_state()
     
    self.pools = app_tables.indexed_data.get(name="pool_list")['data']
    self.refresh_display()
    #get_open_form().menu_click(sender=get_open_form().latest)
    
