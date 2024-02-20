from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def ref_log(referrer):
  current_referrer = get_referrer()
  if current_referrer is None:
    anvil.server.cookies.local['referrer'] = referrer
    return referrer
  else:
    return current_referrer
  
@anvil.server.callable
def get_referrer():
  return anvil.server.cookies.local.get("referrer", None)

@anvil.server.callable
def reset():
  anvil.server.cookies.local.clear()

@anvil.server.callable
def new_pool(chain, address, ticker, description, logo=None):
  app_tables.pool_data.add_row(address=address, ticker=ticker, logo=logo, description=description, chain=chain)

