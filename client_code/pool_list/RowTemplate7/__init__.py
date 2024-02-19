from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...join_pool import join_pool
from ...pool_page import pool_page
class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
  def refresh_display(self):
    
    self.label_length.text = "{} days".format(self.item['stake_duration'])
    self.label_organizer_fee.text = "{}%".format(self.item['organizer_share']/100)
    print(dir(self.item['ticker']))
    self.label_ticker.text = self.item['ticker']
    
    self.label_pooled_hex.text = "{:,.2f}".format((int(get_open_form().get_contract_read("HEX").balanceOf(self.item['pool_address']).toString())+ self.item['current stake principal'])/(10**8))
    try:
      self.image_1.source = app_tables.pool_data.get(ticker=self.item['ticker'], chain=get_open_form().current_network)['logo']
    except:
      pass
  def link_join_click(self, **event_args):
    self.pool_page = pool_page(pool_data = self.item, list_page = self)
    get_open_form().pool_panel.clear()
    get_open_form().pool_panel.add_component(self.pool_page)
    get_open_form().content_panel.visible = False

    
  def refresh(self):
    self.refresh_display()

  def button_open_pool_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def form_show(self, **event_args):
    """This method is called when the data row panel is shown on the screen"""
    self.refresh_display()

