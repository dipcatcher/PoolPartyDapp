from ._anvil_designer import join_poolTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

class join_pool(join_poolTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['pool_data']
    self.read_contract = get_open_form().get_perpetual_pool_contract_read(self.item['pool_address'])
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    print(dir(self.hex_contract_read))
    self.refresh()
  def get_user_data(self):
    a = get_open_form().metamask.address
    data = {}
    if a is None:
      print("No address")
      data['hex balance']=0
      data['pool token balance']=0
      data['allowance']=0
      data['timelocked balance']=0
      data['timelock tokendays record'] = []
      data['timelock record'] = []
      data['has user claimed rewards per period'] =False
    else:
      data['hex balance']=int(self.hex_contract_read.balanceOf(a).toString())
      data['pool token balance'] = int(self.read_contract.balanceOf(a).toString())
      data['allowance']=int(self.hex_contract_read.allowance(self.item['pool_address'],get_open_form().metamask.address).toString())
      data['timelocked balance'] = 0 #int(self.read_contract.userTimelockedBalance(a).toString())
      data['timelock record'] = [int(self.read_contract.userTimelockedBalancePerPeriod(a, n).toString()) for n in range(self.pool_data['current period'])]
      data['timelock tokendays record'] = [int(self.read_contract.userTimelockedTokenDaysePerPeriod(a, n).toString()) for n in range(self.pool_data['current period'])]
      data['has user claimed rewards per period'] = [self.read_contract.hasUserClaimedRewards(a, n) for n in range(self.pool_data['current period'])]
    return data
  def get_pool_data(self):
    data = {}
    data['name']=self.read_contract.name()
    data['liquid supply']=int(self.read_contract.totalSupply().toString())
    data['timelocked supply'] = int(self.read_contract.timelockedSupply().toString())
    data['penalty pool supply']=int(self.read_contract.penaltyPoolSupply().toString())
    data['complete total supply'] = int(self.read_contract.completeTotalSupply().toString())
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
    data['global timelocked token days per period'] = [int(self.read_contract.globalTimelockedTokenDaysPerPeriod(n).toString()) for n in range(data['current period'])]
    data['global time locked tokens per period']= [int(self.read_contract.globalTimelockedTokensPerPeriod(n).toString()) for n in range(data['current period'])]
    data['penalty pool per period'] = [int(self.read_contract.penaltyPoolPerPeriod(n).toString()) for n in range(data['current period'])]
    data['is staking period']=self.read_contract.isStakingPeriod()
    return data
    
  def refresh(self):
    self.pool_data = self.get_pool_data()
    print(self.pool_data)
    if get_open_form().metamask.address is not None:
      
      self.write_contract = get_open_form().get_perpetual_pool_contract_write(self.item['pool_address'])
      self.hex_contract_write = get_open_form().get_contract_write("HEX")
      self.user_data = self.get_user_data()
      for k,v in self.user_data.items():
        self.card_1.add_component(Label(text="{}: {}".format(k,v)))
    
    for k,v in self.pool_data.items():
      self.card_1.add_component(Label(text="{}: {}".format(k,v)))
    
    
    print(dir(self.read_contract))
    self.label_title.text = "Mint ${}".format(self.item['ticker'])
    self.label_schedule.text = "Initial Mint Duration: {} days\nStake Duration: {} days\nReload Duration {} days".format(self.item['initial_mint_duration'],self.item['stake_duration'], self.item['reload_duration'])
    self.label_name.text = self.item['name']
    scan = "https://scan.pulsechain.com/" if get_open_form().button_switch.text =="PLS" else "https://etherscan.io"
    self.link_pool_address.url = "{}/address/{}".format(scan,self.item['pool_address'])
    self.link_pool_address.text = "{}...{}".format(self.item['pool_address'][0:4],self.item['pool_address'][-4:])
    self.label_organizer_share.text = "{:.3f}%".format(self.item['organizer_share']/100)
    self.link_organizer_address.text = "{}...{}".format(self.item['organizer_address'][0:4],self.item['organizer_address'][-4:])
    #self.label_description.text = self.item['description']
  def approve(self, amount):
    try:
      # Call the approve function in the hex write contract
      promise = self.hex_contract_write.approve(self.item['pool_address'], amount)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to approve: ", e)
      result = None
    return result

  def pledgeHex(self, amount):
    try:
      # Call the pledgeHex function in the perpetual pool write contract
      promise = self.write_contract.pledgeHex(amount)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to pledge HEX: ", e)
      result = None
    return result

  def redeemHex(self, amount):
    try:
      # Call redeemHex in the perpetual pool write contract
      promise = self.write_contract.redeemHex(amount)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to redeem HEX: ", e)
      result = None
    return result
  # write the other functions i requested here
  def startTimelock(self, amount, length):
    try:
      promise = self.write_contract.startTimelock(amount, length)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to start timelock: ", e)
      result = None
    return result
  
  def addToTimelock(self, amount, timelockID):
    try:
      promise = self.write_contract.addToTimelock(amount, timelockID)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to add to timelock: ", e)
      result = None
    return result
  
  def endTimelock(self, timelockID):
    try:
      promise = self.write_contract.endTimelock(timelockID)
      result = anvil.js.await_promise(promise)
      result.wait() # Wait for the promise to resolve
    except Exception as e:
      print("An error occurred while trying to end timelock: ", e)
      result = None
    return result
  