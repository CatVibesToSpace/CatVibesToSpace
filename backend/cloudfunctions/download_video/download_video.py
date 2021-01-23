# Trigger on create for jobs/{create}
# Entry point is download_video
from google.cloud import firestore



client = firestore.Client()

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
          
          url = event['value']['fields']['youtube_url']['stringValue']

          # DOWNLOAD CODE GOES HERE


          # Update the database
          affected_doc = client.collection(collection_path).document(document_path)

          print(f'Replacing value: {download_started} --> True')
          affected_doc.set({
               u'download_started': True
          })
          
     print(str(event))
