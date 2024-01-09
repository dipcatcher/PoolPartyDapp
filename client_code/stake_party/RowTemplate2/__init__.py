from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    days_remaining=int(self.item['Days Remaining'].replace(",",""))
    self.button_end_stake.visible = days_remaining<0 and not self.item['ended']
    self.label_days_remaining.visible = not self.button_end_stake.visible
    if days_remaining<0:
      self.label_days_remaining.text = "Stake Complete"
    else:
      self.label_days_remaining.text = days_remaining
  def button_end_stake_click(self, **event_args):
    self.write_party_contract = get_open_form().get_contract_write("PARTY")
    try:
      self.button_end_stake.enabled=False
      a = anvil.js.await_promise(self.write_party_contract.endStake(self.item['id']))
      self.button_end_stake.text = "Ending stake..."
      a.wait()
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      self.button_end_stake.enabled=True
      self.button_end_stake.text = "end stake"
      return False

    get_open_form().menu_click(sender=get_open_form().latest)
    
    

