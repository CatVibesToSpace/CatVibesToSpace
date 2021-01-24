# Trigger on create for jobs/{create}
# Entry point is download_video
from __future__ import unicode_literals
import youtube_dl
import tempfile
import os

from google.cloud import firestore, storage
import youtube_dl


client = firestore.Client()

storage_client = storage.Client()

DOWNLOAD_BUCKET_NAME = "cat-vibes-to-youtube-downloads"

upload_file_name = "default.mp4"

my_affected_doc = None

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
     if d['status'] == 'finished':
          filename = d['filename']
          download_bucket = storage_client.bucket(DOWNLOAD_BUCKET_NAME)
          new_blob = download_bucket.blob(upload_file_name)
          new_blob.upload_from_filename(filename)

          os.remove(filename)

          global my_affected_doc
          my_affected_doc.update({
               u'download_finished': True
          })



def download_video(event, context):
     """Triggered by a change to a Firestore document.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """

     path_parts = context.resource.split('/documents/')[1].split('/')
     collection_path = path_parts[0]
     document_path = '/'.join(path_parts[1:])

     affected_doc = client.collection(collection_path).document(document_path)


     resource_string = context.resource
     # print out the resource string that triggered the function
     print(f"Function triggered by change to: {resource_string}.")
     # now print out the entire event object
     download_started = event['value']['fields']['download_started']['booleanValue']

     print(type(download_started))
     print(download_started)
     if not download_started:
          #Do the download

          print("starting download")

          id = event['value']['fields']['id']['stringValue']       
          url = event['value']['fields']['youtube_url']['stringValue']

          global upload_file_name

          upload_file_name = id + ".mp4"

          # Update the database to say that the download has started
          affected_doc = client.collection(collection_path).document(document_path)

          print(f'Replacing value: {download_started} --> True')
          affected_doc.update({
               u'download_started': True
          })

          global my_affected_doc

          my_affected_doc = affected_doc

          # Pre-download setup

          #_, temp_local_filename = tempfile.mkstemp(suffix='.mp4')
          ydl_opts = {
          'format': '[filesize<40M]', # File size seems to need to be tweaked - look into it more
          'logger': MyLogger(),
          'progress_hooks': [my_hook],
          'outtmpl': "/tmp/%(title)s",
          'noplaylist': True,

          }


          with youtube_dl.YoutubeDL(ydl_opts) as ydl:
               ydl.download([url])

          
     print(str(event))
