from ._anvil_designer import create_stake_poolTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from .. import contract_hub as ch
import anvil.image
class create_stake_pool(create_stake_poolTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address = get_open_form().metamask.address
    self.zero_address = "0x0000000000000000000000000000000000000000"
    self.organizer_address =self.zero_address
    self.uploaded_image=None
    self.organizer_fee = 0
    if self.address is not None:
      self.user_ticker = self.get_nfts_by_owner(self.address)
    else:
      self.user_ticker = []
    '''filter = get_open_form().get_contract_read("PARTY").filters.MintNameNFT(self.address)
    logs = anvil.js.await_promise(get_open_form().metamask.provider.getLogs({
      "fromBlock": 0, 
      "toBlock": 'latest',
      "address": get_open_form().contract_data['PARTY']['address'],
      'topics': filter.topics
    }))
    for log in logs:
      l = get_open_form().get_contract_read("PARTY").interface.parseLog(log)['args']
      
      self.user_ticker.append(l[1])
    '''
    
    self.drop_down_tickers.items = [(f"${t}", t) for t in self.user_ticker]
    self.input = {}
    self.input['organizer_address']=self.zero_address
    self.input['organizer_fee'] = 0
    self.numbers_map = {"initial_mint_length":self.text_box_initial_mint_length,
                       "ongoing_mint_length": self.text_box_ongoing_mint_length,
                       "stake_length":self.text_box_stake_length,
                       "organizer_fee": self.text_box_organizer_fee}
    

    # Any code you write here will run before the form opens.
  def get_nfts_by_owner(self, address):
    contract = get_open_form().get_contract_read("NAME_NFT")
    balance = int(contract.balanceOf(address).toString())
    tickers = []
    for n in range(balance):
      token_id = contract.tokenOfOwnerByIndex(address, n)
      tickers.append(contract.ID_NAME(token_id))
    return tickers
  def link_get_ticker_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().menu_click(sender=get_open_form().link_ticker_auction)
  def validate(self):
    strings = [self.text_area_description, self.text_box_name]
    incomplete = []
    for s in strings:
      if s.text in [None, ""]:
        s.role = 'input-error'
        incomplete.append(s)
      else:
        s.role = ""

    numbers = [self.text_box_initial_mint_length, 
               self.text_box_ongoing_mint_length,
               self.text_box_stake_length]
    for s in numbers:
      is_blank = s.text in [None, ""]
      if any([is_blank, (s.text or 0) < 0]):
        s.role='input-error'
        incomplete.append(s)
      else:
        s.role=""
    
    self.drop_down_tickers.role = 'input-error' if self.drop_down_tickers.selected_value in [None] else ""
    return len(incomplete)==0

  
  def button_deploy_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].enabled=False
    if self.validate():
      if self.uploaded_image is None:
        self.uploaded_image=app_tables.ticker_nfts.get(name=self.input['ticker'])['image']
        self.image_logo.source=self.uploaded_image
      name_nft_read = get_open_form().get_contract_read("NAME_NFT")
      ticker_id = int(name_nft_read.NAME_ID(self.input['ticker']).toString())
      write_contract= get_open_form().get_contract_write("POOL_DEPLOYER")
      read_contract=get_open_form().get_contract_read("POOL_DEPLOYER")
      #getApproved
      deployer_address = get_open_form().contract_data['POOL_DEPLOYER']['address']
      is_approved = name_nft_read.getApproved(ticker_id) == deployer_address
      if not is_approved:
        try:
          approval = anvil.js.await_promise(get_open_form().get_contract_write("NAME_NFT").approve(deployer_address, ticker_id))
          approval.wait()
        except Exception as e:
          try:
            alert(e.original_error.reason)
          except:
            alert(e.original_error.message)
          event_args['sender'].enabled=True
          return False
         
      try:
        a = anvil.js.await_promise(write_contract.deployPool(self.input['ticker'], self.input['initial_mint_length'], self.input['stake_length'], self.input['ongoing_mint_length'],
                                                                                      self.input['name'], self.input['organizer_fee']*100, self.input['organizer_address']))
        a.wait()
        
        Notification("Pool Deployed Succesfully").show()
      except Exception as e:
          try:
            alert(e.original_error.reason)
          except:
            alert(e.original_error.message)
          event_args['sender'].enabled=True
          return False
      address = read_contract.POOL_RECORD(self.input['ticker'])
      
      
      anvil.server.call('new_pool', address, self.input['ticker'], self.uploaded_image)
      get_open_form().menu_click(sender = get_open_form().button_pools, goto = self.input['ticker'])
    else:
      self.button_deploy.enabled=True
      
      
  def text_box_name_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.input['name'] = self.text_box_name.text
    if self.text_box_name.text in [None, ""]:
      event_args['sender'].role = 'input-error'
    else:
      event_args['sender'].role = ''

  def drop_down_tickers_change(self, **event_args):
    """This method is called when an item is selected"""
    self.input['ticker'] = event_args['sender'].selected_value
    event_args['sender'].role = 'input-error' if event_args['sender'].selected_value in [None] else ""
  def number_entry_change(self, **event_args):
    for k,v in self.numbers_map.items():
      if v==event_args['sender']:
        group=k
    requirements = [event_args['sender'].text in [None, "", 0]]
    if group =='stake_length':
      if not requirements[0]:
        requirements.append(int(event_args['sender'].text)>5555)
    elif group =='organizer_fee':
      requirements=[(event_args['sender'].text or 0) >99]
    
    
    self.input[group]=int(event_args['sender'].text or 0)
    event_args['sender'].text=self.input[group]
    event_args['sender'].role = 'input-error' if any(requirements) else ''

  def text_box_organizer_address_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.input['organizer_address']=event_args['sender'].text
    event_args['sender'].role = 'input-error' if event_args['sender'].text in ['', None] else ''

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.image_logo.source = file
    self.uploaded_image = anvil.image.generate_thumbnail(file, 800)
    

  def check_box_organizer_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.column_panel_organizer.visible = self.check_box_organizer.checked
    if not self.column_panel_organizer.visible:
      self.text_box_organizer_address.text = None
      self.text_box_organizer_fee.text = None
      self.organizer_fee = 0
      self.organizer_address = self.zero_address
      self.input['organizer_address']=self.zero_address
      self.input['organizer_fee'] = 0

  def text_area_description_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass
        

    

    