from ._anvil_designer import max_text_boxTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import ethers
class max_text_box(max_text_boxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.raw_value = 0
    self.input=0
    self.label_1.text = get_open_form().current_network

    # Any code you write here will run before the form opens.

  def text_box_1_change(self, **event_args):
    if self.text_box_1.text in [None, "0", 0]:
      self.text_box_1.role = 'input-error'
      self.input = 0
      self.raw_value = 0
    else:
      self.text_box_1.role=None
      self.input = self.text_box_1.text
     
      if self.label_1.text in ["PARTY", "ETH", "PLS"]:
        t = str(self.input)
        self.raw_value = int(ethers.utils.parseEther(t).toString())
      else:
        t = '{:.8f}'.format(self.input)
        self.raw_value = int(ethers.utils.parseUnits(t, 8).toString())
        
    self.raise_event('text_change')
    
    


  

