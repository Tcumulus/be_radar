from generate import generateMap
from datetime import datetime, timedelta
from firebase_admin import credentials, initialize_app, storage
import os
from dotenv import load_dotenv

load_dotenv()
key = {
  "type": "service_account",
  "project_id": "beradar-fba3d",
  "private_key_id": os.environ["KEYID"],
  "private_key": os.environ["KEY"].replace("\\n", "\n"),
  "client_email": os.environ["EMAIL"],
  "client_id": os.environ["ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ["URL"]
}

# input
utcOffset = 2

def fetchImagery():
  now = datetime.now()
  now = now - timedelta(minutes=10) #15 minutes of caution
  now = now - (now - datetime.min) % timedelta(minutes=5) # rounding down 5 minutes

  cred = credentials.Certificate(key)
  initialize_app(cred, {"storageBucket": "beradar-fba3d.appspot.com"})
  bucket = storage.bucket()

  def upload(name, path):
    blob = bucket.blob(name)
    blob.upload_from_filename(path)
    os.remove(path)
    print(f"Finished Uploading: {name}")

  def delete(x, mode):
    # iterate over all files in storage
    iterator = bucket.list_blobs(prefix=mode)
    response = iterator._get_next_page_response()
    try:
      for i in range(x):
        blob = bucket.blob(response["items"][i]["name"])
        blob.delete()
    except:
      print("error while deleting files")

  with open("lastDate.txt", "r") as file:
    lastDate = file.read()
    lastDate = datetime.strptime(lastDate, "%Y-%m-%d %H:%M:%S")

  # calculate number of frames to generate
  deltaTime = now - lastDate
  x = int((deltaTime.total_seconds() / 60) / 5)
  x = 13 if x > 13 else x

  delete(x, "light")
  delete(x, "dark")

  print("Finished Deleting")
  
  for i in range(x):
    date = now - timedelta(minutes=i*5) # interval of 5 minutes
    files = generateMap(date.strftime("%Y-%m-%d"), date.hour, date.minute, utcOffset)
    upload(files[0][0], files[0][1])
    upload(files[1][0], files[1][1])

  with open("lastDate.txt", "w") as file:
    file.write(now.strftime("%Y-%m-%d %H:%M:%S"))

fetchImagery()