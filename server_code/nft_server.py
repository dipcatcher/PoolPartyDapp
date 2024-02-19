import anvil.server
import anvil.http
import Pool_Party_image_generator
@anvil.server.callable
def generate_image(string, nft_id, chain):
  anvil.server.launch_background_task('generate_image_task', string, nft_id, chain)

@anvil.server.background_task
def generate_image_task(string, nft_id, chain):
  Pool_Party_image_generator.ServerModule1.generate_image(string, nft_id, chain)
  