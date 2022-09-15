from generate import generateMap
from datetime import datetime, timedelta
from firebase_admin import credentials, initialize_app, storage
import os

# input
utcOffset = 2

def fetchImagery():
  now = datetime.now()
  now = now - timedelta(minutes=15) #15 minutes of caution
  now = now - (now - datetime.min) % timedelta(minutes=5) # rounding down 5 minutes

  cred = credentials.Certificate("src/hooks/firebase/key.json")
  initialize_app(cred, {"storageBucket": "beradar-fba3d.appspot.com"})
  bucket = storage.bucket()

  def upload(name, path):
    blob = bucket.blob(name)
    blob.upload_from_filename(path)
    os.remove(path)

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



  with open("src/hooks/fetch/lastDate.txt", "r") as file:
    lastDate = file.read()
    lastDate = datetime.strptime(lastDate, "%Y-%m-%d %H:%M:%S")

  # calculate number of frames to generate
  deltaTime = now - lastDate
  x = int((deltaTime.total_seconds() / 60) / 5)
  x = 13 if x > 13 else x
  print(x)

  delete(x, "light")
  delete(x, "dark")
  
  for i in range(x):
    date = now - timedelta(minutes=i*5) # interval of 5 minutes
    [name, path] = generateMap(date.strftime("%Y-%m-%d"), date.hour, date.minute, utcOffset, "light")
    upload(name, path)
    [name, path] = generateMap(date.strftime("%Y-%m-%d"), date.hour, date.minute, utcOffset, "dark")
    upload(name, path)

  with open("src/hooks/fetch/lastDate.txt", "w") as file:
    file.write(now.strftime("%Y-%m-%d %H:%M:%S"))

fetchImagery()