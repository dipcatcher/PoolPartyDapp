from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import ethers
import anvil.js
import datetime
import time
from ...nft_display import nft_display
def timestampDifference(unix_timestamp_now, unix_timestamp_end):
    # Convert Unix timestamps to datetime objects
    start_time = datetime.datetime.fromtimestamp(unix_timestamp_now)
    end_time = datetime.datetime.fromtimestamp(unix_timestamp_end)

    # Calculate the time difference
    time_difference = end_time - start_time
    
    # Extract hours, minutes, and seconds from the time difference
    days = time_difference.days
    hours = (days * 24) + (time_difference.seconds // 3600)
    minutes = (time_difference.seconds % 3600) // 60
    seconds = time_difference.seconds % 60
    

    # Format the time difference as a string
    time_difference_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"

    return time_difference_string
class RowTemplate5(RowTemplate5Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.custom_1.string = self.item['ticker']
    self.party_contract=get_open_form().get_contract_read("PARTY")
    self.refresh_time_remaining()
    self.refresh_auction_data()
    self.counter = 0
    
  def recollect_auction_data(self):
    auction_data = self.party_contract.TICKER_AUCTION_DATABASE(self.item['ticker'])

    auction = {}
    auction['ticker']=self.item['ticker']
    auction["lastBidTimestamp"]=auction_data[0].toNumber()
    auction["firstBidTimestamp"]=auction_data[1].toNumber()
    auction["auctionEndTimestamp"]=auction_data[2].toNumber()
    auction["controller"]=auction_data[3]
    auction["bidAmount"]=int(auction_data[4].toString())
    auction["auctionStarted"]=auction_data[5]
    auction["auctionEnded"]=auction_data[6]
    self.item = auction
  def refresh_auction_data(self):
    self.label_current_bid.text ="{:,.10f}".format(self.item['bidAmount']/(10**18))
    if self.item['auctionEnded']:
      self.button_1.text = 'auction complete'
      
    
  def refresh_time_remaining(self):
    currentBlock = get_open_form().providers[get_open_form().current_network].getBlockNumber()
    try:
      blockTimestamp = get_open_form().providers[get_open_form().current_network].getBlock(currentBlock).timestamp
    except:
      return False
    
    
    if blockTimestamp>self.item['auctionEndTimestamp']:
      self.label_time_remaining.text = "Auction Done"
      self.timer_1.interval = 0
      self.button_1.text = "finalize"
    else:
      self.label_time_remaining.text = timestampDifference(blockTimestamp, self.item['auctionEndTimestamp'])
    
  
    # Any code you write here will run before the form opens.

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    
    self.refresh_time_remaining()
    self.counter +=1
    if self.counter>5:
      self.recollect_auction_data()
      self.refresh_auction_data()
      self.counter=0

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if event_args['sender'].text =='bid':
      
      self.panel_bid.visible = not self.panel_bid.visible
      if self.panel_bid.visible:
        self.recollect_auction_data()
        self.refresh_auction_data()
        self.text_box_bid.label_1.text="PARTY"
        increment = int(self.item['bidAmount']/20) +1
        self.raw_min_bid = increment+self.item['bidAmount']+(10**18)
        print(self.raw_min_bid)
        #self.minimum_bid = float(self.raw_min_bid / (10**18))
        self.minimum_bid = ethers.utils.formatUnits(self.raw_min_bid+(10**18))
        print(self.minimum_bid)
        self.link_minimum_bid.text = "{} PARTY".format(self.minimum_bid)
        self.label_timestamp.text = self.item['auctionEndTimestamp']
        self.label_2.text = self.item['controller']
    elif event_args['sender'].text =='finalize':
      event_args['sender'].enabled = False
      self.write_contract = get_open_form().get_contract_write("PARTY")
      try:
        a = anvil.js.await_promise(self.write_contract.endAuction(self.item['ticker']))
        a.wait()
      except Exception as e:
        try:
          alert(e.original_error.reason)
        except:
          alert(e.original_error.message)
      self.name_nft_contract = get_open_form().get_contract_read("NAME_NFT")
      name_id = self.name_nft_contract.NAME_ID(self.item['ticker']).toNumber()
      try:
        anvil.server.call('generate_image',self.item['ticker'], name_id, get_open_form().current_network )
      except Exception as e:
        raise e
        Notification("NFT image failed to save, no worries it will be regenerated.").show()
      self.recollect_auction_data()
      self.refresh_auction_data()
        
        
      get_open_form().menu_click(sender=get_open_form().latest)
    elif event_args['sender'].text =='auction complete':
      self.name_nft_contract = get_open_form().get_contract_read("NAME_NFT")
      name_id = self.name_nft_contract.NAME_ID(self.item['ticker']).toNumber()
      owner = self.name_nft_contract.ownerOf(name_id)
      text = f"Owner: {owner}\nNFT ID: {name_id}\nPARTY Burnt: {int(self.item['bidAmount']/(10**18)):,}"
      cp = ColumnPanel()
      cp.add_component(Label(text=text))
      cp.add_component(Image(source=app_tables.ticker_nfts.get(chain=get_open_form().current_network, name=self.item['ticker'])['image']))
      alert(cp, title='Auction Details')
      

  def text_box_bid_change(self, **event_args):
    self.input = self.text_box_bid.input
    print((self.text_box_bid.raw_value,self.raw_min_bid))
    if self.text_box_bid.raw_value<self.raw_min_bid:
      event_args['sender'].role = 'input-error'
    else:
      event_args['sender'].role = ""

  def button_submit_bid_click(self, **event_args):
    self.write_contract = get_open_form().get_contract_write("PARTY")
    self.recollect_auction_data()
    if self.item['bidAmount']>self.text_box_bid.raw_value:
      _ = alert("A new bid exceeds your bid, try again")
      self.recollect_auction_data()
      self.refresh_auction_data()
      self.panel_bid.visible = False
      self.text_box_bid.text = None
      self.button_1_click(sender=self.button_1)
      return False
    try:
      
      a = anvil.js.await_promise(self.write_contract.bid(self.item['ticker'], self.text_box_bid.raw_value))
      a.wait()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)

  def link_minimum_bid_click(self, **event_args):
    """This method is called when the link is clicked"""
   
    self.text_box_bid.text_box_1.text = self.minimum_bid
    self.text_box_bid.text_box_1_change(sender=self.text_box_bid.text_box_1)
    self.text_box_bid_change(sender=self.text_box_bid)

  def button_refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.recollect_auction_data()
    self.refresh_auction_data()
    self.panel_bid.visible = False
    self.text_box_bid.text = None
    self.button_1_click(sender=self.button_1)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(self.item['auctionEndTimestamp'])

  



    

  
    

        

      

