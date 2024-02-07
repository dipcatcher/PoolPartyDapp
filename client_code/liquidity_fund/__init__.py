from ._anvil_designer import liquidity_fundTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..value_display import value_display

class liquidity_fund(liquidity_fundTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
  def refresh(self):
    self.party_contract_read = get_open_form().get_contract_read("PARTY")
    chain =get_open_form().current_network
    buy_side = {"title":"{} Deposited".format(chain)}
    p = get_open_form().providers[chain]
    amt = int(p.getBalance(get_open_form().contract_data["PARTY"]['address']).toString())
    if chain =="PLS":
      buy_side['value'] = "{:,}".format(int(amt/(10**18)))
    else:
      buy_side['value']="{:,.4f}".format(amt/(10**18))
    self.flow_panel_1.add_component(value_display(**buy_side))

    sell_side = {"title":"PARTY"}
    total_mintable = int(self.party_contract_read.TOTAL_PARTY_SCHEDULED_TO_MINT().toString())
    initial_supply = int(self.party_contract_read.INITIAL_SUPPLY().toString())
    team_mint = int(self.party_contract_read.MINTED_WITH_TEAM().toString())
    airdrop = total_mintable/10

    lf = total_mintable - (initial_supply + team_mint)
    lf_depositors = lf

    total =lf_depositors + lf + airdrop + team_mint + initial_supply
    
    
    num_party = total_mintable-initial_supply
    sell_side['value'] = "{:,}".format(int(num_party/(10**18)))
    self.flow_panel_1.add_component(value_display(**sell_side))
    