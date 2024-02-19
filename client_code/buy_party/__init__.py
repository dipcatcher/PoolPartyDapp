from ._anvil_designer import buy_partyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class buy_party(buy_partyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_1.url = "https://widget.piteas.io/#/swap?inputCurrency=PLS&outputCurrency=0x4581AF35199BBde87a89941220e04E27ce4b0099&theme=dark&exactField=input&exactAmount=10000000"
    self.link_1_copy.url = "https://swap.defillama.com/?chain=ethereum&from=0x0000000000000000000000000000000000000000&to=0x4581AF35199BBde87a89941220e04E27ce4b0099"

    # Any code you write here will run before the form opens.
