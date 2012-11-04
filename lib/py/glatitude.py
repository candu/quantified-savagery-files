import datetime
import oauth2client.client
import oauth2client.file
import oauth2client.tools

def auth(key, secret, path='creds_glatitude'):
  storage = oauth2client.file.Storage(path)
  def _validateCredentials(c):
    if c is None:
      return False
    if c.client_id != key or c.client_secret != secret:
      return False
    return datetime.datetime.now() < c.token_expiry
  credentials = storage.get()
  if _validateCredentials(credentials):
    return credentials
  flow = oauth2client.client.OAuth2WebServerFlow(
    client_id=key,
    client_secret=secret,
    scope='https://www.googleapis.com/auth/latitude.all.best',
    redirect_uri='http://localhost:8080/oauth2callback'
  )
  return oauth2client.tools.run(flow, storage)
