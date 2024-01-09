from ._anvil_designer import nft_claimTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
class nft_claim(nft_claimTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.nft_contract_read=get_open_form().get_contract_read("NAME_NFT")
    if get_open_form().metamask.address is not None:
      self.collect_users_names()
    else:
      self.label_content.text = "If you claimed names during the Ticker Name Claim phase, connect your wallet to mint them as NFTs which can be utilized for your pools or to list on NFT marketplaces."
      self.data_grid_1.visible = False

    # Any code you write here will run before the form opens.
  def collect_users_names(self):
    all_claim_events =anvil.js.await_promise(get_open_form().get_contract_read("NAMECLAIM").queryFilter('Claim', get_open_form().metamask.provider.blockNumber - 1000000, "latest"))
    claimed_list = []
    all_claimed_list = []
    for e in all_claim_events:
      _ = {"Owner": e['args'][0], "Name":e['args'][1], "Is Minted":True}
      all_claimed_list.append(_)
      if e['args'][0]==get_open_form().metamask.address:
        if int(self.nft_contract_read.NAME_ID(e['args'][1]).toString()) ==0:
          _['Is Minted'] = False
        claimed_list.append(_)
    if len(claimed_list) ==0:
      self.label_content.text = "No ticker names claimed by this address during the Ticker Name Claim phase found."
      self.data_grid_1.visible = False
    self.repeating_panel_2.items = claimed_list
    