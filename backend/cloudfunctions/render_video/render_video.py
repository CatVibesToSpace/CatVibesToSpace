# Trigger on update for jobs/{job}
# Entry point is render_video

import tempfile
import os

from google.cloud import firestore, storage

import ffmpeg

client = firestore.Client()

storage_client = storage.Client()

ASSETS_BUCKET_NAME = "cat-vibes-to-assets"
DOWNLOAD_BUCKET_NAME = "cat-vibes-to-youtube-downloads"
DISTRIBUTION_BUCKET_NAME = "cat-vibes-to-distribution"

def render_video(event, context):


    # Get the document in firestore that has been updated
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    affected_doc = client.collection(collection_path).document(document_path)
    
    id = event['value']['fields']['id']['stringValue']

    encoding_started = event['value']['fields']['encoding_started']['booleanValue']
    download_finished = event['value']['fields']['download_finished']['booleanValue']
    bpm_finished = event['value']['fields']['bpm_finished']['booleanValue']
    

    if (not encoding_started) and download_finished and bpm_finished:

        affected_doc.update({
            u'encoding_started': True
        })

        temp_local_cat_filename = "/tmp/cat.mp4"
        temp_local_input_filename = "/tmp/input.mp4"
        temp_local_output_filename = "/tmp/" + id + ".mp4"
        
        # Get the cat mp4
        cat_mp4_blob = storage_client.bucket(ASSETS_BUCKET_NAME).get_blob("cat.mp4")
        cat_mp4_blob.download_to_filename(temp_local_cat_filename)

        print(f"downloaded cat mp4 to { temp_local_cat_filename }")

        # Get the input mp4
        input_mp4_blob = storage_client.bucket(DOWNLOAD_BUCKET_NAME).get_blob(id + ".mp4")
        input_mp4_blob.download_to_filename(temp_local_input_filename)

        print(f"downloaded input mp4 to { temp_local_input_filename }")

        # Get the bpm
        bpm = float(event['value']['fields']['bpm']['doubleValue'])
        print(f"bpm is { bpm }")


        # Apply ffmpeg
        print("starting render")
        
        
        
        looping = ffmpeg.input(temp_local_cat_filename)#, stream_loop = -1) # Import tom as a looping stream, tom is 426x240
        looping = ffmpeg.filter(looping, "colorkey", color="0x52f21f", similarity=0.3, blend=0) # This green I got myself from the tom video
        looping = ffmpeg.filter(looping, "loop", loop=10)
        stream = ffmpeg.input(temp_local_input_filename, ss=90, t=25) # Get start at 20s in and make the clip 20s
        video = stream.video
        audio = stream.audio

        looping = ffmpeg.filter(looping, "setpts", "{}*PTS".format(118 /bpm))


        video = ffmpeg.filter(video, 'scale', 1280,720) # Resize to 720p
        video = ffmpeg.overlay(stream, looping, shortest=1, y = "0")
        stream = ffmpeg.output(video, audio, temp_local_output_filename).overwrite_output()
        stream.run()

        print("render finished")

        

        print("uploading result")

        distribution_bucket = storage_client.bucket(DISTRIBUTION_BUCKET_NAME)
        upload_blob = distribution_bucket.blob(id + ".mp4")
        upload_blob.upload_from_filename(temp_local_output_filename)

        print("result uploaded")
        
        # Get the download url

        # Make the blob public

        upload_blob.make_public()
        download_url = upload_blob.public_url

        affected_doc.update({
            u'encoding_finished': True,
            u'url' : download_url
        })

        # Clean up by deleting all the temp files

        os.remove(temp_local_cat_filename)
        os.remove(temp_local_input_filename)
        os.remove(temp_local_output_filename)

        print("cleaned up")