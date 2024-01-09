from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class RowTemplate10(RowTemplate10Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_claim_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.rd_contract_write=get_open_form().get_contract_write("REWARD_DISTRIBUTION")
    try:
      event_args['sender'].enabled=False
      event_args['sender'].text = "claiming..."
      a = anvil.js.await_promise(self.rd_contract_write.claimReward(self.item['Asset'], self.item['Snapshot Period'], self.item['Snapshot Period']))
      a.wait()
      event_args['sender'].text = "claimed"
      event_args['sender'].icon = "fa:check"
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      event_args['sender'].enabled=True
      event_args['sender'].text = "claim"
      

