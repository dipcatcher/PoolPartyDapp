from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
  def refresh(self):
    address = self.parent.parent.parent.parent.item['pool_address']
    self.read_contract = get_open_form().get_perpetual_pool_contract_read(address)
    self.hasUserClaimedRewards  =  self.read_contract.hasUserClaimedRewards(get_open_form().metamask.address, self.item['Period'])
    #self.button_claim.enabled=self.hasUserClaimedRewards
    filter = self.read_contract.filters.EndCompletedTimelock()

    events =self.read_contract.queryFilter(filter, 0, 'latest')
    print(events)
    for e in events:
      print(e)
  def button_claim_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    address = self.parent.parent.parent.parent.item['pool_address']
    self.write_contract = get_open_form().get_perpetual_pool_contract_write(address)
    try:
      a = anvil.js.await_promise(self.write_contract.endCompletedTimelock(self.item['Period']))
      a.wait()
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)

  def form_show(self, **event_args):
    """This method is called when the data row panel is shown on the screen"""
    self.refresh()

    