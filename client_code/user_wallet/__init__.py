from ._anvil_designer import user_walletTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import ethers
import datetime
from ..value_display import value_display
class user_wallet(user_walletTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.party_contract_read = get_open_form().get_contract_read("PARTY")
    #self.party_contract_write = get_open_form().get_contract_write("PARTY")
    self.nft_contract_read = get_open_form().get_contract_read('NAME_NFT')
    self.current_day  = int(self.party_contract_read.day().toString())
    self.address = get_open_form().metamask.address
    self.refresh()
  def refresh(self):
    self.data = {}
    if self.address is None:
      self.data['Liquid Balance'] = 0
      self.data['Staked Balance'] = 0
      self.data['Nametag NFTs'] = []
      self.data['Future Yield'] = 0
    else:
      self.data['Liquid Balance'] = int(self.party_contract_read.balanceOf(self.address).toString())
      s,y, all_stakes = self.get_staked_balance(self.address)
      self.data['Staked Balance'] = s
      self.data['Future Yield'] = y
      self.data['Nametag NFTs'] = self.get_nfts_by_owner(self.address)
      
    liquid_party_text = "{:,.4f}".format(self.data['Liquid Balance']/(10**18))
    staked_party_text = "{:,.4f}".format(self.data['Staked Balance']/(10**18))
    future_party = "{:,.4f} PARTY".format(self.data['Future Yield']/(10**18))
    label_map = {"Liquid PARTY": liquid_party_text}
    label_map['Staked PARTY'] = staked_party_text
    #label_map['Future PARTY Yield']= future_party
    
    for k,v in label_map.items():
      
      vd = value_display(value=v, title=k)
      vd.label_title.font_size=9
      vd.label_value.bold=True
      vd.label_value.font_size=14
      vd.role='card'
      self.flow_panel_1.add_component(vd)
    
    
    
    if self.data['Nametag NFTs'] == []:
      self.card_1.visible = False
    else:
      for nft in self.data['Nametag NFTs']:
        nft_id = int(self.nft_contract_read.NAME_ID(nft).toString())
        print(nft_id)

        row = app_tables.ticker_nfts.get(nft_id=nft_id)
        if row is None:
          anvil.server.call('generate_image', nft, nft_id)
        
        
        #url = "https://testpoolpartynft.anvil.app/_/api/image/{}".format(nft_id)
        c=ColumnPanel(role='raised-card')
        c.add_component(Image(source=row['image'], role='card'))
        self.card_1.add_component(c)
        

    self.snapshot_data = self.get_snapshot_data()
    self.repeating_panel_1.items = self.snapshot_data['record']
  def get_snapshot_data(self):
    data = {}
    data['current snapshot id'] = int(self.party_contract_read.getCurrentSnapshotId().toString())
    data['latest snapshot day'] = int(self.party_contract_read.LATEST_SNAPSHOT_DAY().toString())
    data['current day'] = int(self.party_contract_read.day().toString())
    data['current supply']=int(self.party_contract_read.totalSupply().toString())
    data['earnings record'] = []
    data['user earnings record']= []
    data['user balance record'] = []
    data['total supply at']=[]
    data['record'] = []
    
    for p in range(data['current snapshot id']):
      _ = {}
      
      p=p+1
      _['Snapshot Period'] = p
      _['Supply']=int(self.party_contract_read.totalSupplyAt(p).toString())
      if self.address is not None:
        _['Balance'] = int(self.party_contract_read.balanceOfAt(self.address, p).toString())
        _['Earnings Details'] = []
      else:
        _['Balance']=0
        _['Earnings Details']=[]
      # TODO: query the AssetProcessed event for period p and return a list of AssetProcessed events
      # Create a filter to get logs for the mintWithReferral event where the referrer is the given address
      event_filter = self.party_contract_read.filters.AssetProcessed(None, p)  # Replace with the actual event name and indexed parameters if different
  
      # Query the event logs from the contract
      logs = self.party_contract_read.queryFilter(event_filter)
      for log in logs:
        args = log['args']
        asset = args[0]
        if self.address is not None:
          earnings = int(self.party_contract_read.getEarningsDetails(self.address, asset, p).toString())
          earning_detail = {}
          earning_detail['Asset']=asset
          earning_detail['Amount']=earnings
          _['Earnings Details'].append(earning_detail)
        
        
      data['record'].append(_)
      
      
      
    data['reward distribution contract address'] = self.party_contract_read.REWARD_DISTRIBUTION_CONTRACT_ADDRESS()
    return data
  def get_staked_balance(self, address):
    self.all_stakes = []
    num_stakes = int(self.party_contract_read.STAKER_NUMBER_STAKES(address).toString())
    amount_staked = 0
    projected_yield = 0
    for n in range(num_stakes):
      l = self.party_contract_read.STAKER_LOG(address, n)
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
      self.deployment_date= datetime.datetime(2023, 9,25)
      ld['End Day'] = (self.deployment_date + datetime.timedelta(days=ld['End Day'])).strftime("%m/%d/%Y")
      ld['Days Remaining'] = "{:,}".format(ld['Days Remaining'])
      self.all_stakes.append(ld)
      if ld['ended']==False:
        amount_staked += int(l[1].toString())
        projected_yield +=int(l[3].toString())
    return amount_staked, projected_yield, self.all_stakes
  
  def get_nfts_by_owner(self, address):
    contract = get_open_form().get_contract_read("NAME_NFT")
    balance = int(contract.balanceOf(address).toString())
    tickers = []
    for n in range(balance):
      token_id = contract.tokenOfOwnerByIndex(address, n)
      tickers.append(contract.ID_NAME(token_id))
    return tickers
      
