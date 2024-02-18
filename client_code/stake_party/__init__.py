from ._anvil_designer import stake_partyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
import anvil.js
from anvil.js.window import ethers
import datetime
confetti_module = anvil.js.import_from('https://cdn.skypack.dev/canvas-confetti')
confetti = confetti_module.default
class stake_party(stake_partyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selection = []
    self.deployment_date = datetime.datetime(2024, 2,19)
    
    for p in app_tables.table_1.get(name='yield_tree_proofs')['data']:
      y = p['yield_scalar']/(10**8)
  
      apy = 365*y/p['days']
     
      yield_display = "{:.2f}% Yield, {:.2f}% APY".format(y*100, apy*100)
      display = "{:,} days ({} years) earning {}".format(p['days'], int(p['days']/365) if p['days']>=365 else "{:.2f}".format( p['days']/365), yield_display)
      format_proof = [p['days'], json.loads(p['proof']), p['yield_scalar']]
      self.selection.append((display, format_proof))
    self.drop_down_days.items = self.selection
    self.custom_1.label_1.text = "PARTY"
    self.refresh()
  def refresh(self):
    self.party_contract_read= get_open_form().get_contract_read('PARTY')
    self.current_day = int(self.party_contract_read.day().toString())
    self.address = get_open_form().metamask.address
    self.data= {}
    if self.address is None:
      self.button_stake.enabled = False
      self.data['Staked PARTY Balance'] = 0
      self.data['PARTY Balance'] = 0
    else:
      
      self.write_party_contract = get_open_form().get_contract_write("PARTY")
      
      self.all_stakes = []
      num_stakes = int(self.party_contract_read.STAKER_NUMBER_STAKES(self.address).toString())
      amount_staked = 0
      projected_yield = 0
      for n in range(num_stakes):
        l = self.party_contract_read.STAKER_LOG(self.address, n)
        ld = {}
        ld['Principal']=int(l[1].toString())/(10**18)
        ld['End Day']=int(l[2].toString())
        ld['Days Remaining']=ld['End Day'] - self.current_day
        ld['Yield']=int(l[3].toString())/(10**18)
        ld['End Value'] = ld['Yield'] + ld['Principal']
        ld['started']=l[4]
        ld['ended']=l[5]
        ld['id']=n
        ld['Principal'] = "{:,.2f}".format(ld['Principal'])
        ld['Yield'] = "{:,.2f}".format(ld['Yield'])
        ld['End Value'] = "{:,.2f}".format(ld['End Value'])
        ld['End Day'] = (self.deployment_date + datetime.timedelta(days=ld['End Day'])).strftime("%m/%d/%Y")
        ld['Days Remaining'] = "{:,}".format(ld['Days Remaining'])
        self.all_stakes.append(ld)
        if ld['ended']==False:
          amount_staked += int(l[1].toString())
          projected_yield +=int(l[3].toString())
      if len(self.all_stakes)>0:
        if len(self.all_stakes)<self.data_grid_1.rows_per_page:
          self.data_grid_1.show_page_controls=False
        else:
          self.data_grid_1.show_page_controls=True
        self.data_grid_1.visible=True
        self.label_stake_record.visible=True
        self.repeating_panel_1.items=self.all_stakes
      else:
        self.data_grid_1.visible = False
      self.data['Staked PARTY Balance'] =amount_staked
      self.data['PARTY Balance'] = int(self.party_contract_read.balanceOf(self.address).toString())
      self.label_party_balance.text = "{:,.8f} PARTY".format(self.data['PARTY Balance']/(10**18))
      self.label_staked_party_balance.text = "{:,.8f} PARTY".format(self.data['Staked PARTY Balance']/(10**18))
      
  def button_stake_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].enabled = False
    existing_text = event_args['sender'].text
    sending = event_args['sender'].text
    minting = sending.replace("Stake", "Staking")
    event_args['sender'].text =minting
    t = "{:f}".format(self.input)
    
    try:
      
      a = anvil.js.await_promise(self.write_party_contract.startStake(ethers.utils.parseEther(t), self.drop_down_days.selected_value[0] , json.loads(json.dumps(self.drop_down_days.selected_value[1])),self.drop_down_days.selected_value[2]))
      a.wait()
      confetti()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      
      if "object Object" in str(e):
        event_args['sender'].text = existing_text
        event_args['sender'].enabled = True
      try:
        alert(e.original_error.reason)
      except:
        alert(e.original_error.message)

  def custom_1_text_change(self, **event_args):
    """This method is called when the text box changes"""
    self.raw_value = self.custom_1.raw_value
    self.input = self.custom_1.input
    self.button_stake.enabled=self.check_button_enable()
    self.raw_stakable= self.raw_value 
    self.display_stakable = self.raw_stakable / (10**18)
    self.button_stake.text = "Stake {:,.2f} PARTY".format(self.display_stakable) if self.raw_value > 0 else "Stake PARTY"
    
  def check_button_enable(self):
    a= all([get_open_form().metamask.address is not None,self.drop_down_days.selected_value not in [None], self.input>0])
    if a:
      self.label_yield.text = "In {:,} days you will mint {:,.2f} PARTY.".format(self.drop_down_days.selected_value[0], 
                                                                 self.input*(1+self.drop_down_days.selected_value[2]/(10**8)) )
    else:
      self.label_yield.text = None
    return a
  def drop_down_days_change(self, **event_args):
    """This method is called when an item is selected"""
    
    self.custom_1_text_change()


    