from ._anvil_designer import mint_partyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import contract_hub as ch
from anvil.js.window import ethers
import anvil.js
import json
import anvil.js
confetti_module = anvil.js.import_from('https://cdn.skypack.dev/canvas-confetti')
confetti = confetti_module.default

class mint_party(mint_partyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.raw_value = 0
    self.input = 0
    self.refresh_page()
    
  def refresh_page(self):
    self.label_2.text = "{} Balance".format(get_open_form().current_network)
    self.party_contract_read= get_open_form().get_contract_read('PARTY')
    self.address = get_open_form().metamask.address
    mint_length = int(self.party_contract_read.MINT_PHASE_LENGTH().toString())
    self.data= {}
    self.data['Days Remaining'] =mint_length - int(self.party_contract_read.day().toString())
    self.data['Referrer'] = get_open_form().referral
    self.data['Mint Rate'] = int(self.party_contract_read.MINT_SCALAR().toString())
    if self.address is None:
      self.button_mint.enabled = False
      self.data['ETH Balance'] = 0
      self.data['PARTY Reserved'] = 0
      self.data['PARTY Balance'] = 0
    else:
      self.button_mint.enabled =True
      self.write_party_contract = get_open_form().get_contract_write("PARTY")
      self.data['ETH Balance'] = int(get_open_form().metamask.provider.getBalance(self.address).toString())
      self.data['PARTY Reserved'] = int(self.party_contract_read.SCHEDULED_MINT(self.address).toString())
      self.data['PARTY Balance'] = int(self.party_contract_read.balanceOf(self.address).toString())
      
    self.target_units = 48000 if self.data['Referrer']is None else 48960
    self.label_eth_balance.text = "{:,.8f}".format(self.data['ETH Balance']/(10**18))
    self.label_party_balance.text = "{:,.8f}".format(self.data['PARTY Reserved']/(10**18))
    self.label_party_minted.text = "{:,.8f}".format(self.data['PARTY Balance']/(10**18))
    self.label_days_left.text = "{} {} left to reserve {:,} PARTY per {} {} deposited into the Liquidity Fund.".format(
        self.data['Days Remaining'], 
        "Days" if self.data['Days Remaining'] >1 else "Day",
        self.target_units,
        self.data['Mint Rate'],  
        get_open_form().current_network
      )
    
    if True:#self.data['Days Remaining']<0:
      self.button_mint.visible=False
      self.custom_1.text_box_1.enabled=False
      self.custom_1.visible=False
      self.label_days_left.text = "Launch Phase is Complete"
      self.is_ready =True#self.party_contract_read.IS_TIME_TO_MINT()
      if self.is_ready:
        
        self.label_4.text = "Reserved PARTY can now be minted."
        self.button_go_to_mint.visible = True
      else:
        self.label_4.text = "Liquidity Pools are being deployed, you may claim your PARTY shortly."
      

  def button_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.input in [None, 0, ""]:
      Notification("You must enter an amount.").show()
      return False
    event_args['sender'].enabled = False
    existing_text = event_args['sender'].text
    sending = event_args['sender'].text
    minting = sending.replace("Reserve", "Reserving")
    event_args['sender'].text =minting
    t = "{:f}".format(self.input)
    try:
      if self.data['Referrer'] is None:
        tx = {'to':get_open_form().contract_data['PARTY']['address'], 'value':ethers.utils.parseEther(t)}
        a = anvil.js.await_promise(get_open_form().metamask.signer.sendTransaction(tx))
      else:
        a = anvil.js.await_promise(self.write_party_contract.scheduleMintWithReferral(self.data['Referrer'], {'value': ethers.utils.parseEther(t)}))
      a.wait()
      confetti()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      event_args['sender'].enabled = True

    

  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    self.raw_value = self.custom_1.raw_value
    self.input = self.custom_1.input
    self.button_mint.enabled=self.check_button_enable()
    self.raw_mintable = self.raw_value * self.target_units / self.data['Mint Rate']
    self.display_mintable = self.raw_mintable / (10**18)
    self.button_mint.text = "Reserve {} PARTY".format(self.display_mintable) if self.raw_value > 0 else "Reserve PARTY"
    
  def check_button_enable(self):
    return all([self.raw_value>0, get_open_form().metamask.address not in [None]])

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    get_open_form().referral_check()


  def claimMintedTokens(self):
    try:
      a = anvil.js.await_promise(self.write_party_contract.claimMintedTokens())
      a.wait()
    except Exception as e:
  
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)

  def button_go_to_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    if get_open_form().metamask.address is None:
      alert("Connect wallet first.")
      return False
    if self.data['PARTY Reserved']>0:
      self.claimMintedTokens()
      get_open_form().menu_click(sender=get_open_form().latest)
    else:
      alert("No PARTY reserved by connected address.")
    

