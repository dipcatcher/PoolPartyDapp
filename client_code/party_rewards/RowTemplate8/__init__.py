from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.balance = int(self.item['balance'])/(10**int(self.item['decimals']))
    self.title = "{} ({})".format(self.item['name'], self.item['symbol'])
    self.label_balance.text = "{:,.4f}".format(self.balance)
    self.label_balance.tooltip = self.balance
    self.label_name.text= self.title
   

    # Any code you write here will run before the form opens.

  def button_process_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.party = get_open_form().get_contract_write("PARTY")
      
      a = anvil.js.await_promise(self.party.processAsset(self.item['contractAddress']))
      a.wait()
      alert('success')
      self.visible=False
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e)
    

