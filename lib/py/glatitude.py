import oauth2client.client
import oauth2client.file
import oauth2client.tools

def auth(key, secret, path='creds_glatitude'):
  storage = oauth2client.file.Storage(path)
  credentials = storage.get()
  if credentials is not None and \
     credentials.client_id == key and \
     credentials.client_secret == secret:
    return credentials
  flow = oauth2client.client.OAuth2WebServerFlow(
    client_id=key,
    client_secret=secret,
    scope='https://www.googleapis.com/auth/latitude.all.best',
    redirect_uri='http://localhost:8080/oauth2callback'
  )
  credentials = oauth2client.tools.run(flow, storage)
