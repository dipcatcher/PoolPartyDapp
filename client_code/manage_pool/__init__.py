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
    self.refresh()
  def refresh(self):
    if get_open_form().metamask.address is not None:
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
    """require(BONUS_PROCESSING_DEADLINE==0, "Can only inititate once per cycle.");
        require(hex_token.currentDay()>STAKE_END_DAY, "Stake is not complete yet.");
        require(STAKE_IS_ACTIVE==true, "Stake must be active.");"""
    bpd = int(self.contract_read.BONUS_PROCESSING_DEADLINE().toString())
    a = bpd==0
    b = self.item['current hex day']>self.item['stake end day']
    c = self.item['stake is active']
    self.button_start_end.enabled = all([a,b,c])
    """require(BONUSES_READY==false, "Function already ran.");
        require(BONUS_PROCESSING_DEADLINE>0, "Must run startBonusSequence first.");
        require(block.timestamp>BONUS_PROCESSING_DEADLINE, "Must wait until deadline.");"""
    d = bpd > 0
    e = self.contract_read.BONUSES_READY()==False
    chain = get_open_form().current_network
    block = anvil.js.await_promise(get_open_form().providers[chain].getBlock("latest"))
    timestamp = block['timestamp']
    f = timestamp >bpd
    self.label_bpd.text = "Timestamp End Sequence Ready: {}\nCurrent Timestamp: {}".format(bpd, timestamp)
    
    
    self.button_complete_end.enabled = True
    self.button_end_stake.enabled = self.contract_write.BONUSES_READY()
    
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
    self.refresh()

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
      self.refresh()

  def button_contribute_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_start_end_click(self, **event_args):
    stake_index = Label(text="This will start a 6 hour period to mint the final day of hedron and mint COM if available before ending the stake.")
    
    c = ColumnPanel()
    c.add_component(stake_index)
    _ = alert(c)
    if True:
      try:
        a = anvil.js.await_promise(self.contract_write.initiateBonusSequence())
        a.wait()
        Notification("Bonus sequence started").show()
        self.refresh()
      except Exception as e:
        alert(e)
  def button_complete_end_click(self, **event_args):
    stake_index = Label(text="This will record a snapshot of balances for COM and HDRN distribution and make the stake able to end. If stake is small and short, HDRN and COM may be infeasible to claim. Run End Stake next.")
    
    c = ColumnPanel()
    c.add_component(stake_index)
    _ = alert(c)
    if True:
      try:
        a = anvil.js.await_promise(self.contract_write.completeBonusSequence())
        a.wait()
        Notification("Bonus Sequence Ended").show()
        self.refresh()
      except Exception as e:
        alert(e)

  def button_com_start_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
        a = anvil.js.await_promise(self.contract_write.mintStartBonusCom(self.stakeIndex, self.stakeId))
        a.wait()
        Notification("Minted COM").show()
        self.refresh()
    except Exception as e:
      alert(e)

  def button_com_end_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
        a = anvil.js.await_promise(self.contract_write.mintEndBonusCom(self.stakeIndex, self.stakeId))
        a.wait()
        Notification("Minted COM").show()
        self.refresh()
    except Exception as e:
      alert(e)

  def button_claim_bonus_click(self, **event_args):
    try:
        a = anvil.js.await_promise(self.contract_write.claimBonus())
        a.wait()
        Notification("Bonus Sequence Ended").show()
        self.refresh()
    except Exception as e:
      alert(e)


  

