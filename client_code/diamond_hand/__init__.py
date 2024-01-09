from ._anvil_designer import diamond_handTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class diamond_hand(diamond_handTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['pool_data']
    self.custom_1.label_1.text = self.item['ticker']
    self.custom_1_copy.label_1.text = self.item['ticker']
    self.write_contract = get_open_form().get_perpetual_pool_contract_write(self.item['pool_address'])
    self.custom_1.label_1.text = self.item['ticker']
    self.custom_1_copy.label_1.text = self.item['ticker']
    
    for r in dir(self.write_contract):
      self.add_component(Label(text=r))
    
    for k,v in self.item.items():
      self.add_component(Label(text="{}: {}".format(k,v)))
    self.refresh()
  def refresh(self):
    try:
      percent = self.item['timelock tokendays record'][-1]/self.item['global timelocked token days per period'][-1]
    except:
      percent=0
    hdrn_rewards = self.item['hdrn balance'] * percent
    token_rewards= self.item['penalty pool supply']*percent
    self.stake_period_data = []
    self.stake_period_data.append({"Period":1, "HDRN Rewards":hdrn_rewards/(10**9), "Penalty Rewards": token_rewards/(10**8)})
    self.repeating_panel_1.items = self.stake_period_data
    # Any code you write here will run before the form opens.

  def button_timelock_click(self, **event_args):
    """This method is called when the button is clicked"""
    amount = self.custom_1.input
    a = anvil.js.await_promise(self.write_contract.timelockTokens(self.custom_1.raw_value))
    a.wait()
    Notification("Timelocked _ tokens").show()

  def button_early_unlock_click(self, **event_args):
    """This method is called when the button is clicked"""
    amount = self.custom_1_copy.input
    a = anvil.js.await_promise(self.write_contract.earlyUnlockTokens(self.custom_1_copy.raw_value))
    a.wait()
    Notification("Early Unlocked").show()


