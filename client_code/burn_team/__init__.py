from ._anvil_designer import burn_teamTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers
class burn_team(burn_teamTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.custom_1.label_1.text = "TEAM"
    self.team_contract_read = get_open_form().get_contract_read("TEAM")
    self.party_contract_read = get_open_form().get_contract_read("PARTY")
   
    
    self.party_contract_write = None
    self.team_contract_write = None
  def refresh(self):
    if get_open_form().metamask.address is None:
      self.balance = 0
      self.approval = 0
      self.party_balance=0
    else:
      self.party_contract_write =  get_open_form().get_contract_write("PARTY")
      self.team_contract_write = get_open_form().get_contract_write("TEAM")
      self.balance = int(self.team_contract_read.balanceOf(get_open_form().metamask.address).toString())
      self.party_balance=int(self.party_contract_read.balanceOf(get_open_form().metamask.address).toString())
      spender=get_open_form().contract_data['PARTY']['address']
      self.approval = int(self.team_contract_read.allowance(get_open_form().metamask.address, spender).toString())
    self.label_team_balance.text = "{:,.8f}".format(self.balance/(10**8))
    self.label_party_balance.text = "{:,.8f}".format(self.party_balance/(10**18))
    self.label_approved_team.text = "{:,.8f}".format(self.approval/(10**8))
    
    
  # Any code you write here will run before the form opens.

  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    if self.custom_1.text_box_1.text is None:
      self.button_approve.text = "Approve"
      self.button_approve.visible = False
      self.button_mint.text = "Burn"
      return False
    self.input_text = self.custom_1.text_box_1.text or 0
    self.input_value = ethers.utils.parseUnits(str(self.input_text), 8)
    
    a = self.balance>=int(self.input_value.toString())
    self.is_valid = all([a])
    self.is_allowed = self.approval >=int(self.input_value.toString())
    
    print(self.approval, int(self.input_value.toString()))
    if self.is_allowed:
      self.button_approve.visible=False
      self.label_is_approved.visible=True
      self.label_is_approved.text = "Approved {} TEAM".format(self.approval/(10**8))
      
    else:
      self.button_approve.visible = True
      self.button_approve.text = "Approve {} TEAM".format(self.input_text)
      self.label_is_approved.visible=False
      self.button_approve.visible=True
    self.button_mint.text = "Burn {} TEAM".format(self.input_text)
    print(self.is_valid, self.is_allowed)
  
    self.button_mint.enabled= not self.button_approve.visible

  def form_show(self, **event_args):
    self.refresh()

  def button_approve_click(self, **event_args):
    """This method is called when the button is clicked"""
    spender =get_open_form().contract_data['PARTY']['address']
    try:
      a=anvil.js.await_promise(self.team_contract_write.approve(spender, self.input_value))
      a.wait()
      self.refresh()
      self.custom_1_text_change()
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        raise e

  def button_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.button_mint.text = "Burning..."
      self.button_mint.enabled=False
      a=anvil.js.await_promise(self.party_contract_write.mintWithTeam(self.input_value))
      a.wait()
      
      get_open_form().menu_click(sender=get_open_form().link_burn_team)
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        raise e
      self.button_mint.text = "Burn"
      self.button_mint.enabled=True
      

      


    

