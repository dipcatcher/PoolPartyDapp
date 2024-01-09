import anvil.server
import anvil.http
@anvil.server.callable
def generate_image(string, nft_id):
  anvil.server.launch_background_task('generate_image_task', string, nft_id)

@anvil.server.background_task
def generate_image_task(string, nft_id):
  url = "https://nftimagegenerator.anvil.app/_/api/generate/{}/{}".format(string, nft_id)
  anvil.http.request(url, method="POST")