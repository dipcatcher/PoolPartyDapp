from ._anvil_designer import value_displayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class value_display(value_displayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_title.text = properties['title']
    self.label_value.text = properties['value']

    # Any code you write here will run before the form opens.
