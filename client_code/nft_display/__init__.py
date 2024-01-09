from ._anvil_designer import nft_displayTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class nft_display(nft_displayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    h = '''<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=Poppins&display=swap');
</style>
  <style>
    .image-container {
      position: relative;
      width: 100%;
      max-width: 300px;
    }

    .overlay-text {
    font-family: 'Plus Jakarta Sans', sans-serif;
      position: absolute;
      top: 66%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
      font-size: 28px;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
  </style>
</head>
<canter>
  <div class="image-container">
    <img src="your_image_url" alt="" style="width:100%;">
    <div class="overlay-text">*STRING*</div>
  </div>
</center>
</html>'''.replace("your_image_url", app_tables.media.get(name="template")['media'].get_url()).replace("*STRING*", self.string )
    self.column_panel_1.clear()
    self.column_panel_1.add_component(HtmlTemplate(html=h))

