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
    self.data= {}
    if self.address is None:
      self.button_mint.enabled = False
      self.data['ETH Balance'] = 0
      self.data['PARTY Balance'] = 0
      mint_length = int(self.party_contract_read.MINT_PHASE_LENGTH().toString())
      self.data['Days Remaining'] =mint_length - int(self.party_contract_read.day().toString())
      self.data['Mint Multiplier Eligible'] =False
      self.data['Referrer'] = get_open_form().referral
      if get_open_form().current_network =="ETH":
        self.data['Mint Rate'] = 42069
        if self.data['Referrer'] is not None:
          self.data['Mint Rate'] = int(42069*1.0369)
      else:
        scalar = int(self.party_contract_read.MINT_SCALAR().toString())
        self.data['Mint Rate']= scalar / (10**8)
        if self.data['Referrer'] is not None:
          self.data['Mint Rate'] = 1.02 * self.data['Mint Rate']

    else:
      self.button_mint.enabled =True
      self.write_party_contract = get_open_form().get_contract_write("PARTY")
      self.airdrop_record = app_tables.user_record.get(address=q.full_text_match(self.address))
      self.is_eligible = self.airdrop_record is not None
      
      self.data['ETH Balance'] = int(get_open_form().metamask.provider.getBalance(self.address).toString())
      self.data['PARTY Balance'] = int(self.party_contract_read.balanceOf(self.address).toString())
      mint_length = int(self.party_contract_read.MINT_PHASE_LENGTH().toString())
      self.data['Days Remaining'] =mint_length - int(self.party_contract_read.day().toString())
  
      self.data['Mint Multiplier Eligible'] = self.is_eligible
      self.data['Referrer'] = get_open_form().referral
      self.button_mint_multiplier.visible = self.is_eligible
      if get_open_form().current_network =="ETH":
        self.data['Mint Rate'] = 42069+(self.data['Mint Multiplier Eligible'] * 6309)
        if not self.is_eligible:
          if self.data['Referrer'] is not None:
            self.data['Mint Rate'] = int(42069*1.0369)
      else:
        scalar = int(self.party_contract_read.MINT_SCALAR().toString())
        base = scalar / (10**8) 
        self.data['Mint Rate'] = base * 1.15 if self.data['Mint Multiplier Eligible'] else base
        
        if not self.is_eligible:
          if self.data['Referrer'] is not None:
            self.data['Mint Rate'] = self.data['Mint Rate']* 1.0369
      
   
    self.label_eth_balance.text = "{:,.8f}".format(self.data['ETH Balance']/(10**18))
    self.label_party_balance.text = "{:,.8f}".format(self.data['PARTY Balance']/(10**18))
    if get_open_form().current_network =="ETH":
      self.label_days_left.text = "{} {} left to mint {:,} PARTY per 1 ETH.".format(
        self.data['Days Remaining'], 
        "Days" if self.data['Days Remaining'] >1 else "Day",
        self.data['Mint Rate']
      )
    else:
      print(self.data['Mint Rate'])
      print(1/self.data['Mint Rate'])
      units = int(1/self.data['Mint Rate'])
      self.label_days_left.text = "{} {} left to mint 1 PARTY per {} PLS.".format(
        self.data['Days Remaining'], 
        "Days" if self.data['Days Remaining'] >1 else "Day",
        units 
      )
    if self.data['Days Remaining']<0:
      self.button_mint.visible=False
      self.custom_1.text_box_1.enabled=False
      self.label_days_left.text = "Mint Phase is Complete"
    
  def button_mint_multiplier_click(self, **event_args):
    """This method is called when the button is clicked"""
    text = """All users who were eligible for the Maximus Community PARTY Airdrop are able to mint PARTY at a discounted rate. The Mint Multiplier gives minters 6309 extra PARTY per ETH, increasing the mint ratefrom 42,069 to 48,378 PARTY per ETH."""
    alert(text, title="Mint Multiplier Info")

  def button_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.input in [None, 0, ""]:
      Notification("You must enter an amount.").show()
      return False
    event_args['sender'].enabled = False
    existing_text = event_args['sender'].text
    sending = event_args['sender'].text
    minting = sending.replace("Mint", "Minting")
    event_args['sender'].text =minting
    t = "{:f}".format(self.input)
    
    try:
      if self.is_eligible:
        a = anvil.js.await_promise(self.write_party_contract.mintWithMultiplier(json.loads(self.airdrop_record['merkle_proof']), self.airdrop_record['merkle_points'], {'value': ethers.utils.parseEther(t)}))
      else:
        if self.data['Referrer'] is None:
          tx = {'to':get_open_form().contract_data['PARTY']['address'], 'value':ethers.utils.parseEther(t)}
          a = anvil.js.await_promise(get_open_form().metamask.signer.sendTransaction(tx))
        else:
          a = anvil.js.await_promise(self.write_party_contract.mintWithReferral(self.data['Referrer'], {'value': ethers.utils.parseEther(t)}))
        
      a.wait()
      confetti()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)

      '''if "object Object" in str(e):
        event_args['sender'].text = existing_text
        event_args['sender'].enabled = True
        alert('Transaction not completed.')'''
      
    

  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    self.raw_value = self.custom_1.raw_value
    self.input = self.custom_1.input
    
    self.button_mint.enabled=self.check_button_enable()
    self.raw_mintable = self.raw_value * self.data['Mint Rate']
    self.display_mintable = self.raw_mintable / (10**18)
    self.button_mint.text = "Mint {} PARTY".format(self.display_mintable) if self.raw_value > 0 else "Mint PARTY"
    

  def check_button_enable(self):
    return all([self.raw_value>0, get_open_form().metamask.address not in [None]])

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    get_open_form().referral_check()




