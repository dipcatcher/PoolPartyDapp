from ._anvil_designer import ticker_auctionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers
class ticker_auctions(ticker_auctionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.party_contract_read = get_open_form().get_contract_read("PARTY")
    self.text_box_bid.label_1.text = "PARTY"
    self.refresh_list()
  
  def text_box_search_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.text_box_search.text = self.text_box_search.text.upper()
    if " " in self.text_box_search.text:
      self.text_box_search.text = self.text_box_search.text.replace(" ", "")
    has_lowercase= False
    for c in self.text_box_search.text:
      if c.islower():
        has_lowercase = True
    if has_lowercase:
      self.label_error.text = "Nametags must only have capital letters or numbers."
      self.label_error.visible= True
      self.text_box_search.role = 'input-error'
    else:
      self.label_error.text = "Nametags must only have capital letters or numbers."
      self.label_error.visible= False
      self.text_box_search.role = ''

  def button_claim_click(self, **event_args):
    if get_open_form().metamask.address is None:
      self.nameclaim_contract = get_open_form().get_contract_read("NAMECLAIM")
      self.party_contract = get_open_form().get_contract_read("PARTY")
    a = self.nameclaim_contract.NAME_OWNERS(self.text_box_search.text) =="0x0000000000000000000000000000000000000000"
    auction_record = self.party_contract.TICKER_AUCTION_DATABASE(self.text_box_search.text)
    b = auction_record[5]==False
    is_available = all([a,b])
    try:
      is_valid = self.nameclaim_contract._checkName(self.text_box_search.text)
      if all([is_available, is_valid]):
        self.column_panel_results.visible = True
        self.label_name.text = self.text_box_search.text
        self.button_available.text = 'Start Auction'
        self.button_available.icon = 'fa:bolt'
        self.button_available.foreground=''
        self.button_available.enabled=True
      else:
        self.column_panel_results.visible = True
        self.label_name.text = self.text_box_search.text
        self.button_available.text = 'Unavailable'
        self.button_available.enabled=False
        self.button_available.foreground='red'
        self.button_available.icon = 'fa:times'
    except Exception as e:
      if 'reason="Exceeds allowed length"' in str(e):
        alert('Name must be less than 10 characters.')
        is_valid=False
        self.column_panel_results.visible=False
        self.label_name.text = None
        self.button_available.text="Start Auction"
  def refresh_list(self):
    if get_open_form().metamask.address is not None:
      self.party_contract = get_open_form().get_contract_write("PARTY")
      self.nameclaim_contract = get_open_form().get_contract_write("NAMECLAIM")
    auction_start_events = anvil.js.await_promise(get_open_form().get_contract_read("PARTY").queryFilter('AuctionStarted'))
    all_tickers = [ase['args'][0] for ase in auction_start_events]
    all_auctions = []
    active_auctions = []
    for ticker in all_tickers:
      auction_data = self.party_contract_read.TICKER_AUCTION_DATABASE(ticker)
      '''uint256 lastBidTimestamp;
            uint256 firstBidTimestamp;
            uint256 auctionEndTimestamp;
            address controller;
            uint256 bidAmount;
            bool auctionStarted;
            bool auctionEnded;'''
      auction = {}
      auction['ticker']=ticker
      auction["lastBidTimestamp"]=auction_data[0].toNumber()
      auction["firstBidTimestamp"]=auction_data[1].toNumber()
      auction["auctionEndTimestamp"]=auction_data[2].toNumber()
      auction["controller"]=auction_data[3]
      auction["bidAmount"]=int(auction_data[4].toString())
      auction["auctionStarted"]=auction_data[5]
      auction["auctionEnded"]=auction_data[6]
      if not auction['auctionEnded']:
        active_auctions.append(auction)
      all_auctions.append(auction)
    self.all_auctions = all_auctions
    self.active_auctions = active_auctions
    self.select_group()
  def select_group(self):
    b = self.check_box_1.checked
    data= self.all_auctions if b else self.active_auctions
    self.repeating_panel_1.items = data
  def button_available_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    if get_open_form().metamask.address is None:
      alert('You must connect your wallet and mint to claim a name.')
    else:
      is_available = self.nameclaim_contract.NAME_OWNERS(self.text_box_search.text) =="0x0000000000000000000000000000000000000000"
      is_valid = self.nameclaim_contract._checkName(self.text_box_search.text)
      valid_bid = True
      print(self.input)
      bid_amount = int(self.input*10**18)
      print(bid_amount)
      if app_tables.ticker_nfts.get(name=self.text_box_search.text) is None:
        pass
        #anvil.server.call('generate_image',self.text_box_search.text )
      if all([is_available, is_valid, valid_bid]):
        try:
          
          a = anvil.js.await_promise(get_open_form().get_contract_write("PARTY").startAuction(self.text_box_search.text, bid_amount))
          self.button_available.text = 'Starting Auction'
          self.button_available.icon = ''
          self.button_available.enabled=False
          a.wait()
          self.column_panel_results.visible=False
          self.text_box_bid.text = None
          self.text_box_search.text = None
          
          try:
            pass
            #anvil.server.call('alert_claim', self.text_box_search.text, get_open_form().address)
          except:
            pass
          self.button_available.text = 'Succesfully Started'
          self.button_available.icon = 'fa:check'
          self.button_available.foreground='green'
          
          #self.refresh_my_names()
          self.refresh_list()
          #get_open_form().current_form.refresh()
        except Exception as e:
          try:
            alert(e.original_error.reason)
          except:
            alert(e.original_error.message)

  def text_box_bid_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.input = self.text_box_bid.input

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.select_group()

  
    

  

  



