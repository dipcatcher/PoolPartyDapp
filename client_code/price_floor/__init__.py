from ._anvil_designer import price_floorTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class price_floor(price_floorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.custom_1.label_1.text = "PARTY"
    self.raw_value = 0
    self.network = "PLS"
    self.refresh()
    # Any code you write here will run before the form opens.

  def button_burn_click(self, **event_args):
    """This method is called when the button is clicked"""
    al = alert("Are you sure you want to {}?".format(self.button_burn.text), buttons=[("Yes", True), ("Cancel", False)])
    if al:
      try:
        self.party_contract_write = get_open_form().get_contract_write("PARTY")
        a = anvil.js.await_promise(self.party_contract_write.exercisePriceFloor(self.raw_value))
        a.wait()
        
      except Exception as e:
        try:
          alert(e.original_error.reason)
        except:
          alert(e.original_error.message)
        return False
      get_open_form().menu_click(sender=get_open_form().latest)
  def check_button_enable(self):
    criteria = []
    criteria.append(get_open_form().metamask.address is not None)
    criteria.append(self.raw_value>0)
    if get_open_form().metamask.address is None:
      balance = 0
    else:
      balance = self.data['PARTY Balance']
    criteria.append(balance>=self.raw_value)
    return all(criteria)
  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    self.raw_value = self.custom_1.raw_value
    self.input = self.custom_1.input
    self.button_burn.enabled=self.check_button_enable()
    self.raw_burnable= self.raw_value 
    self.display_burnable = self.raw_burnable / (10**18)
    self.button_burn.text = "Burn {:,.2f} PARTY to redeem {:.8f} {}.".format(self.display_burnable, self.display_burnable * self.data['Ratio']/(10**8), self.network) if self.raw_value > 0 else "Burn PARTY"
  def refresh(self):
    self.party_contract_read= get_open_form().get_contract_read('PARTY')
    ratio = int(self.party_contract_read.SCALED_PRICE_FLOOR_RATIO().toString())
    
    description = "{:.8f} {} per PARTY Burnt".format(ratio/(10**8), get_open_form().button_switch.text)
    text = "33% of the {} used to mint PARTY is held in the contract and can be redeemed at any time at the rate of {}. This means if the market price of PARTY goes below that threshold, PARTY gets burnt instead of sold due to arbitrage. ".format(self.network, description)
    self.label_days_left.text = text
    self.address = get_open_form().metamask.address
    self.data= {}
    self.data['Ratio']=ratio
    if self.address is None:
      self.button_burn.enabled = False
      self.data['PARTY Balance'] = 0
      self.data['ETH Balance'] = 0
    else:
      self.data['ETH Balance']=int(get_open_form().metamask.provider.getBalance(self.address).toString())
      self.data['PARTY Balance'] = int(self.party_contract_read.balanceOf(self.address).toString())
    self.label_party_balance.text = "{:,.8f} PARTY".format(self.data['PARTY Balance']/(10**18))
    self.label_eth_balance.text  = "{:,.8f} ETH".format(self.data['ETH Balance']/(10**18))