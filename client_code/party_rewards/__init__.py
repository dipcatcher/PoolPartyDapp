from ._anvil_designer import party_rewardsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import anvil.http
class party_rewards(party_rewardsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.contract_read = get_open_form().get_contract_read("PARTY")
    self.party_address = self.contract_read.address
    self.is_connected = get_open_form().metamask.address is not None
    #self.button_record_snapshot.visible = self.is_snapshot_ready()
    if self.is_connected:
      self.contract_write = get_open_form().get_contract_write("PARTY")
    self.refresh()
    for _ in dir(get_open_form().get_contract_read("PARTY")):
      if "(" in _:
        print(_)
  def is_snapshot_ready(self):
    days_since_last = int(self.contract_read.day().toString())-int(self.contract_read.LATEST_SNAPSHOT_DAY().toString())
    print(days_since_last)
    return days_since_last>14
  def refresh(self):
    #self.get_assets_list()
    self.data = self.get_data()
    pending_reward_list = []
    for asset in self.get_assets_list()['result']:
      d = {}
      for k, v in asset.items():
        d[k] = v
      
      pending_reward_list.append(d)
    self.repeating_panel_1.items = pending_reward_list
    #for k,v in self.data.items():
      #self.add_component(Label(text="{}, {}".format(k,v)))
  def get_assets_list(self):
    #api_url = "https://scan.v4.testnet.pulsechain.com/api?module=account&action=tokenlist&address={}".format(self.party_address)
    #r = anvil.http.request(api_url, json=True)
    #alert(r)
    sample = {
  "message": "OK",
  "result": [
    {
      "balance": "1354992345234523452345235",
      "contractAddress": "0x0000000000000000000000000000000000000000",
      "decimals": "18",
      "name": "Example Token",
      "symbol": "ET",
      "type": "ERC-20"
    },
    {
      "balance": "12345234523452345",
      "contractAddress": "0x0000000000000000000000000000000000000001",
      "decimals": "18",
      "name": "Example ERC-721 Token",
      "symbol": "ET7",
      "type": "ERC-721"
    }
  ],
  "status": "1"
}
    return sample
  def get_data(self):
    data = {}
    address = get_open_form().metamask.address
    data['current snapshot id'] = int(self.contract_read.getCurrentSnapshotId().toString())
    data['latest snapshot day'] = int(self.contract_read.LATEST_SNAPSHOT_DAY().toString())
    data['current day'] = int(self.contract_read.day().toString())
    data['current supply']=int(self.contract_read.totalSupply().toString())
    data['earnings record'] = []
    data['user earnings record']= []
    data['user balance record'] = []
    data['total supply at']=[]
    for p in range(data['current snapshot id']):
      p=p+1
      
      data['total supply at'].append(int(self.contract_read.totalSupplyAt(p).toString()))
      if self.is_connected:
        data['user balance record'].append(int(self.contract_read.balanceOfAt(address,p).toString()))
        '''for l in self.get_assets_list():
          data['user earnings record'].append(int(self.contract_read.getEarningsDetails(address,l,p).toString()))
        '''
    data['current period pending earnings']=int(get_open_form().get_contract_read("HEX").balanceOf(self.contract_read.address).toString())
    data['reward distribution contract address'] = self.contract_read.REWARD_DISTRIBUTION_CONTRACT_ADDRESS()
    return data
  def record_snapshot(self, **event_args):
      try:
        a = anvil.js.await_promise(self.contract_write.recordSnapshot())
        a.wait()
        Notification("snapshot recorded").show()
        
      except Exception as e:
        raise e
        try:
          alert(e.original_error.reason)
        except:
          alert(e.original_error.message)
        return False
      self.refresh()
  def claim_rewards(self, start, end):
    self.reward_distribution_write = get_open_form().get_contract_write("REWARD_DISTRIBUTION")
    a = anvil.js.await_promise(self.reward_distribution_write.claimRewards(start, end))
    a.wait()

  def button_process_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.party = get_open_form().get_contract_write("PARTY")
      
      a = anvil.js.await_promise(self.party.processAsset(self.text_box_1.text))
      a.wait()
      alert("Contract Processed")
      self.text_box_1.text = None
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e)

  def button_claim_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.rd = get_open_form().get_contract_write("REWARD_DISTRIBUTION")
      last_period = int(self.text_box_period.text)
      first_period = last_period
      a = anvil.js.await_promise(self.rd.claimRewards(self.text_box_claim_contract.text, first_period, last_period))
      a.wait()
      alert("rewards claimed")
      self.text_box_claim_contract.text = None
      self.text_box_period.text = None
    except Exception as e:
      try:
        alert(e.original_error.reason)
      except:
        alert(e)



 
  
      
