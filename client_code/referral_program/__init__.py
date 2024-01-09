from ._anvil_designer import referral_programTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import navigator, ethers
import anvil.http
class referral_program(referral_programTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.

  def link_new_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.column_panel_generate.remove_from_parent()
    self.column_panel_generate.visible = True
    if get_open_form().metamask.address is not None:
      self.text_box_new_address.text = get_open_form().metamask.address
    a=alert(self.column_panel_generate, title="Create Referral Link",large=True, buttons=[("Submit", True), ("Cancel", False)])
    if a:
      address = self.text_box_new_address.text
      try:
        checksummed = ethers.utils.getAddress(address)
        self.link_ref.text = "{}/#?ref={}".format(anvil.server.get_app_origin(),checksummed)
        self.column_panel_3.visible = True
        self.text_box_new_address.text = None
        tweet_text = "Get a 3.69% Minting Multiplier for $PARTY, the official token of Pool Party, with this link!\n\nPARTY holders earn real yield in $HEX with the option to stake and earn more PARTY! 🪩 \n\nJoin the PARTY 😎👇{}".format(self.link_ref.text)
        t = anvil.http.url_encode(tweet_text)
        self.link_tweet.url = "https://twitter.com/intent/tweet?text={}".format(t)
      except:
        Notification("Invalid Address format. Try again.").show()
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    a = get_open_form().metamask.address
    if a is not None:
      checksummed = ethers.utils.getAddress(a)
      self.link_ref.text = "{}/#?ref={}".format(anvil.server.get_app_origin(),checksummed)
        
      tweet_text = "Get a 3.69% Minting Multiplier for $PARTY, the official token of Pool Party, with this link!\n\nPARTY hlders earn real yield in $HEX with the option to stake and earn more PARTY! 🪩 \n\nJoin the PARTY 😎👇{}".format(self.link_ref.text)
      t = anvil.http.url_encode(tweet_text)
      self.link_tweet.url = "https://twitter.com/intent/tweet?text={}".format(t)
    else:
      self.column_panel_3.visible = False
  def link_ref_click(self, **event_args):
    """This method is called when the link is clicked"""
    navigator.clipboard.writeText(event_args['sender'].text)
    Notification("Link copied to clipboard!").show()



