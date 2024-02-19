from ._anvil_designer import pool_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..mint_pool import mint_pool
from ..redeem_pool import redeem_pool
from ..diamond_hand import diamond_hand
from ..manage_pool import manage_pool
from ..value_display import value_display
class pool_page(pool_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.mint_page = None
    self.redeem_page = None
    self.dh_page = None
    self.item = properties['pool_data']
    #self.list_page = properties['list_page']
    self.read_contract = get_open_form().get_perpetual_pool_contract_read(self.item['pool_address'])
    self.first = True
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    self.user_data = {}
    self.refresh()
    if self.item['stake is active']:
      self.menu_click(sender=self.button_manage_pool)
    else:
      self.menu_click(sender=self.button_mint)
    #self.get_events()
  def get_events(self):
    deployer_contract_read = self.get_contract_read("POOL_DEPLOYER")
    deployer_abi = contract_data = self.contract_data["POOL_DEPLOYER"]['abi']
    # TODO: return event query results of the input event_name. The event_name should be in the available events from the party_abi.
    #event_names = [event['name'] for event in party_abi if event['type'] == 'event']
    
    #if event_name not in event_names:
       # raise ValueError(f"The event {event_name} is not in the ABI.")
    
    # Query the event logs
    event_filter = party_contract_read.filters("PoolDeployment")
    logs = party_contract_read.queryFilter(event_filter)
    for log in logs:
      print(log)
    
    # Any code you write here will run before the form opens.
  def refresh(self):
    self.label_name.text = self.item['name']
    self.label_symbol.text = self.item['ticker']
    self.label_description.text = app_tables.pool_data.get(ticker=self.item['ticker'])['description']
    self.label_address.text = "{}".format(self.item['pool_address'])
    self.label_organizer.text = "Organizer: ".format(self.item['organizer_address'])
    data_display_values = ['liquid supply',"timelocked supply", "penalty pool supply","complete total supply", "current stake principal" ]
    if self.first:
      self.vd_liquid = value_display(value ="{:,.1f}".format(self.item['liquid supply']/(10**8)), title = "Supply {}".format(self.item['ticker']))
      self.vd_hdrn=value_display(value = "{:,.1f}".format(self.item['hdrn balance']/(10**9)), title = "HDRN in Contract")
      self.vd_com = value_display(value = "{:,.1f}".format(self.item['com balance']/(10**18)), title = "COM in Contract")
      self.vd_hex = value_display(value = "{:,.1f}".format((self.item['hex balance'] + self.item['current stake principal'])/(10**8)), title = "HEX in Contract")
      self.flow_panel_data.add_component(self.vd_liquid)
      self.flow_panel_data.add_component(self.vd_hex)
      self.flow_panel_data.add_component(self.vd_com)
      
      self.flow_panel_data.add_component(self.vd_hdrn)
      self.first=False
    else:
      value ="{:,.1f}".format(self.item['liquid supply']/(10**8))
      title = "Supply {}".format(self.item['ticker'])
      self.vd_liquid.label_value.text = value
      self.vd_liquid.label_title.text = title
      value = "{:,.1f}".format(self.item['com balance']/(10**18))
      title = "COM in Contract"
      self.vd_com.label_value.text = value
      self.vd_com.label_title.text = title
      value = "{:,.1f}".format(self.item['hdrn balance']/(10**9))
      title = "HDRN in Contract"
      self.vd_hdrn.label_value.text = value
      self.vd_hdrn.label_title.text = title
      value = "{:,.1f}".format(self.item['current stake principal']/(10**8))
      title = "Stake Principal HEX"
      self.vd_hex.label_value.text = value
      self.vd_hex.label_title.text = title
      
      
      
    
   
    #self.list_page.refresh()
    #self.pool_data = self.get_pool_data()
    #for k,v in self.pool_data.items():
      #self.item[k]=v
    self.user_data = self.get_user_data()
    
    for k,v in self.user_data.items():
      self.item[k]=v
    
      
      
    #self.label_description.text = self.item['description']
  def get_user_data(self):
    a = get_open_form().metamask.address
    data = {}
    if a is None:
      data['hex balance']=0
      data['pool token balance']=0
      data['allowance']=0
      
    else:
      data['hex balance']=int(self.hex_contract_read.balanceOf(a).toString())
      data['pool token balance'] = int(self.read_contract.balanceOf(a).toString())
      data['allowance']=int(self.hex_contract_read.allowance(get_open_form().metamask.address,self.item['pool_address']).toString())
      
     
    return data
  def get_pool_data(self):
    data = {}
    data['name']=self.read_contract.name()
    data['liquid supply']=int(self.read_contract.totalSupply().toString())
   
    data['current hex day']=int(self.read_contract.getHexDay().toString())
    data['current period']=int(self.read_contract.CURRENT_PERIOD().toString())
    data['current stake principal']=int(self.read_contract.CURRENT_STAKE_PRINCIPAL().toString())
    data['reload phase duration']=int(self.read_contract.RELOAD_PHASE_DURATION().toString())
    data['redemption rate']=int(self.read_contract.HEX_REDEMPTION_RATE().toString())
    data['reload phase start']=int(self.read_contract.RELOAD_PHASE_START().toString())
    data['reload phase end']=int(self.read_contract.RELOAD_PHASE_END().toString())
    data['stake start day']=int(self.read_contract.STAKE_START_DAY().toString())
    data['stake end day']=int(self.read_contract.STAKE_END_DAY().toString())
    data['stake is active']=self.read_contract.STAKE_IS_ACTIVE()
    data['stake length']=int(self.read_contract.STAKE_LENGTH().toString())
    
    data['days until stake end'] = data['stake end day']- data['current hex day']
    
    return data
  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    if event_args['sender'] == self.button_mint:
      self.mint_page = mint_pool(pool_data = self.item, page =self)
      self.display = self.mint_page
    elif event_args['sender']==self.button_redeem:
      self.redeem_page = redeem_pool(pool_data = self.item, page=self)
      self.display = self.redeem_page
    elif event_args['sender']==self.button_manage_pool:
      self.manage_page = manage_pool(pool_data = self.item, page=self)
      self.display =self.manage_page
    for b in self.flow_panel_1.get_components():
      b.role = "outlined" if b==event_args['sender'] else ""
    self.column_panel_actions.clear()
    self.column_panel_actions.add_component(self.display)

  def link_all_pools_click(self, **event_args):
    get_open_form().content_panel.visible=True
    get_open_form().pool_panel.clear()

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    try:
      self.image_logo.source = app_tables.pool_data.get(ticker=self.item['ticker'])['logo']
    except:
      pass


