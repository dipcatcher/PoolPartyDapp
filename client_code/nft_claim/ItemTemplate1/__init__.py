from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_1.text ="${}".format(self.item['Name'])
    bg = "#10E25B33"
    fg = "#10E25B"
    if self.item['Is Minted']:
      self.button_claim.role = "link-mm"
      self.button_claim.icon = "fa:check"
      self.button_claim.foreground=fg
      self.button_claim.background = bg
      self.button_claim.text = "Minted"
    #self.button_claim.enabled = not self.item['Is Minted']
    #self.button_claim.role = "link-mm" if self.item['Is Minted'] else "filled"

    # Any code you write here will run before the form opens.

  def button_claim_click(self, **event_args):
    """This method is called when the button is clicked"""
    #mintFromNameclaim(string memory ticker)
    if self.item['Is Minted']:
      nft_id = get_open_form().get_contract_read("NAME_NFT").NAME_ID(self.item['Name']).toString()
      alert("NFT ID: {}\nWith this NFT you are able to deploy a Pool Party stake pool with the ticker name ${}.".format(nft_id, self.item['Name']), title="Your NFT")
    else:
      self.write_contract = get_open_form().get_contract_write("PARTY")
      a = anvil.js.await_promise(self.write_contract.mintFromNameclaim(self.item['Name']))
      a.wait()
      get_open_form().menu_click(sender=get_open_form().latest)

  

    

