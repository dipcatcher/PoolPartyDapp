from ._anvil_designer import days_staked_boxTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class days_staked_box(days_staked_boxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.current = None

    # Any code you write here will run before the form opens.

  def text_box_1_change(self, **event_args):
    
    entry = event_args['sender'].text
    print(entry)
    if entry>36500 or entry<0 or entry in ['', None]:
      event_args['sender'].role="input-error"
      
    else:
      event_args['sender'].role=""
    if entry in [None, ""]:
      pass
    else:
      if "." in str(entry):
        
        entry = str(entry).split(".")[0]
        print(entry)
      event_args['sender'].text = int(entry)
      self.days_staked = int(entry)
      

