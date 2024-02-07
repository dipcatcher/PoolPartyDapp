from ._anvil_designer import manage_poolTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from datetime import date
from anvil.js.window import ethers
class manage_pool(manage_poolTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['pool_data']
    self.contract_write = get_open_form().get_perpetual_pool_contract_write(self.item['pool_address'])
    self.contract_read = get_open_form().get_perpetual_pool_contract_read(self.item['pool_address'])
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    self.hdrn_contract_read = get_open_form().get_contract_read("HDRN")
    self.pending_start = (self.item['current hex day']>self.item['reload phase end']) and not self.item['stake is active']
    self.button_start_stake.enabled = self.pending_start
    self.pending_end = (self.item['current hex day']>self.item['stake end day']) and self.item['stake is active']
    self.button_mint_hdrn.enabled = self.item['stake is active'] and (self.item['current hex day']>self.item['stake start day']+1)
    self.button_start_stake.enabled = self.pending_start
    self.button_end_stake.enabled = self.pending_end
    self.stakeCount = int(self.hex_contract_read.stakeCount(self.item['pool_address']).toString())
    self.get_latest_hdrn_mint()
    stakes = []
    for n in range(self.stakeCount):
      print(n)
      s = self.hex_contract_read.stakeLists(self.item['pool_address'], n)
      stake_data = {"stakeId":s[0],"stakedHearts":s[1], "stakeShares":s[2], "lockedDay":s[3], "stakedDays":s[4], "unlockedDay":s[5], "stakeIndex":n}
      self.stakeId = stake_data['stakeId']
      self.stakeIndex = stake_data['stakeIndex']
      stakes.append(stake_data)
  def get_latest_hdrn_mint(self):
    filter =self.hdrn_contract_read.filters.Transfer(ethers.constants.AddressZero, self.item['pool_address'])
    events = self.hdrn_contract_read.queryFilter(filter, 0, 'latest')
    if events not in [[], None]:
      latestEvent = events[-1]
      print(latestEvent)
      self.latest_run = get_open_form().block_to_time(latestEvent['blockNumber'])
      self.label_hdrn_mint_data.text ="Last date minted: {}".format(self.latest_run.strftime("%m/%d/%Y"))
      self.can_run = self.latest_run.date()<date.today()
    else:
      self.can_run=False
    print(self.can_run)
    
  def button_mint_hdrn_click(self, **event_args):
    stake_index = TextBox(text=self.stakeIndex)
    stake_id = TextBox(text=self.stakeId)
    c = ColumnPanel()
    c.add_component(stake_index)
    c.add_component(stake_id)
    _ = alert(c)
    if _:
      
      a = anvil.js.await_promise(self.contract_write.mintHedron(stake_index.text, stake_id.text))
      a.wait()
      Notification("HDRN Minted").show()

  def button_start_stake_click(self, **event_args):
    a= anvil.js.await_promise(self.contract_write.stakeHEX())
    a.wait()
    Notification("Stake Started").show()

  def button_end_stake_click(self, **event_args):
    stake_index = TextBox(text=self.stakeIndex)
    stake_id = TextBox(text=self.stakeId)
    c = ColumnPanel()
    c.add_component(stake_index)
    c.add_component(stake_id)
    _ = alert(c)
    if _:
      a = anvil.js.await_promise(self.contract_write.endStakeHEX(stake_index.text, stake_id.text))
      a.wait()
      Notification("Stake Ended").show()

  def button_contribute_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


  
