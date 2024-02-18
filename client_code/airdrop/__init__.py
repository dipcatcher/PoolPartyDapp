from ._anvil_designer import airdropTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import json
confetti_module = anvil.js.import_from('https://cdn.skypack.dev/canvas-confetti')
confetti = confetti_module.default

class airdrop(airdropTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
 
  def refresh(self):
    self.party_contract = get_open_form().get_contract_read("PARTY")
    if get_open_form().metamask.address is None:
      self.label_status.text = "Connect to metamask to see airdrop eligibility."
      return False
    self.airdrop_record = app_tables.pool_party_merkle.get(address=q.full_text_match(get_open_form().metamask.address))
    self.is_eligible = self.airdrop_record is not None
    self.did_claim = self.party_contract.HAS_REDEEMED_INITIAL_SUPPLY_POINTS(get_open_form().metamask.address)
    abbr_add="{}...{}".format(get_open_form().metamask.address[0:4], get_open_form().metamask.address[-4:])
    
    if self.is_eligible:
      if self.did_claim:
          self.label_status.text = "{} has already claimed.".format(abbr_add)
      else:
          self.label_status.text = "You are eligible to claim {:,.4f} PARTY".format(self.airdrop_record['party_mintable']/(10**18))
          self.button_1.visible=True
    else:
      self.label_status.text = "{} is not eligible for the airdrop.".format(abbr_add)
  def form_show(self, **event_args):
    self.refresh()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].enabled=False
    self.party_contract_write = get_open_form().get_contract_write("PARTY")
    try:
      #proof=json.loads(self.airdrop_record['merkle_proof'])
      a = anvil.js.await_promise(self.party_contract_write.redeemInitialSupplyPoints(self.airdrop_record['merkle_proof'], self.airdrop_record['party_mintable']))
      a.wait()
      confetti()
      self.label_status.text = "Airdrop Claim Success!"
    except Exception as e:
     
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)
      event_args['sender'].enabled=True

  def link_add_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = 'PARTY'
        tokenDecimals = 18
        tokenImage = anvil.server.get_app_origin()+'/_/theme/party%20small.svg'
        print(tokenImage)

        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': get_open_form().contract_data['PARTY']['address'], 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='PARTY Token Added'
      except Exception as e:
        print(e)
      

    