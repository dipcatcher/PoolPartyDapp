from ._anvil_designer import redeem_poolTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers
class redeem_pool(redeem_poolTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['pool_data']
    self.page = properties['page']
    self.read_contract = get_open_form().get_perpetual_pool_contract_read(self.item['pool_address'])
    self.hex_contract_read = get_open_form().get_contract_read("HEX")
    self.custom_1.label_1.text =self.item['ticker']
    print(self.item)
    self.refresh()
    #self.item={'ticker': 'JESUS', 'initial_mint_duration': 12, 'stake_duration': 100, 'reload_duration': 5, 'name': 'Lord and Savior', 'organizer_share': 100, 'organizer_address': '0x2848e510C6FA6424b623708F8478Db1047BF769C', 'pool_address': '0x862D348383AE8DbcEd4BF2E703815E97D0909FEb', 'liquid supply': 0, 'timelocked supply': 0, 'penalty pool supply': 0, 'complete total supply': 0, 'current hex day': 1317, 'current period': 0, 'current stake principal': 0, 'reload phase duration': 5, 'redemption rate': 100000000, 'reload phase start': 1316, 'reload phase end': 1328, 'stake start day': 0, 'stake end day': 0, 'stake is active': False, 'stake length': 100, 'global timelocked token days per period': [], 'global time locked tokens per period': [], 'penalty pool per period': [], 'is staking period': False}
    # Any code you write here will run before the form opens.

  def refresh_above(self):
    self.page.refresh()
    self.item = self.page.item
  def refresh(self):
    self.label_pool_token_balance_display.text = "{} Balance".format(self.item['ticker'])
    self.label_mint_token.text = "Redeem {}".format(self.item['ticker'])
    self.button_mint.text = "Redeem {}".format(self.item['ticker'])
    if self.item['current period']==0:
      dur = self.item['initial_mint_duration']
    else:
      dur = self.item['reload_duration']
    days_remaining = dur-(self.item['current hex day'] - self.item['reload phase start'])
    self.mint_rate_formatted = self.item['redemption rate']/(10**8)
    
    self.label_days_left.text = "{} days remaining to redeem {} HEX per {} burnt.".format(days_remaining, self.mint_rate_formatted, self.item['ticker'])
    if days_remaining<0:
      self.button_mint.enabled=False
      self.custom_1.text_box_1.enabled=False
      self.label_days_left.text = "Redemption phase is over."
    if get_open_form().metamask.address is not None:
      self.hex_balance = int(self.hex_contract_read.balanceOf(get_open_form().metamask.address).toString())
      self.token_balance = int(self.read_contract.balanceOf(get_open_form().metamask.address).toString())
      self.label_hex_balance.text = "{:,.2f}".format(self.hex_balance/(10**8))
      self.label_token_balance.text = "{:,.2f}".format(self.token_balance/(10**8))
  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    self.raw_value = self.custom_1.raw_value
    self.input = self.custom_1.input
    self.input_amount = ethers.utils.parseUnits(str(self.raw_value), 8)

    self.button_mint.enabled=self.check_button_enable()
    self.formatted_mintable = self.mint_rate_formatted*self.input 
    self.raw_mintable = int(self.raw_value*self.mint_rate_formatted)
    self.button_mint.text = "Redeem {} {}".format(self.formatted_mintable, self.item['ticker']) if self.raw_value > 0 else "Redeem"
    
    if self.token_balance>0:
      self.button_mint.enabled = True
  def check_button_enable(self):
    return all([self.raw_value>0, get_open_form().metamask.address not in [None]])

  def button_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      print(self.raw_value)
      a = anvil.js.await_promise(get_open_form().get_perpetual_pool_contract_write(self.item['pool_address']).redeemHEX(self.raw_value))
      a.wait()
      self.custom_1.text_box_1.text = None
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
    self.refresh_above()
    self.refresh()
