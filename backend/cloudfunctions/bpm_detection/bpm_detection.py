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

def get_bpm(event, context):
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
    bpm_started = event['value']['fields']['bpm_started']['booleanValue']

    print(type(bpm_started))
    print(bpm_started)
    if not bpm_started:
        # Do the download

        print("starting download")

        id = event['value']['fields']['id']['stringValue']

        # Update the database to say that the download has started
        affected_doc = client.collection(collection_path).document(document_path)

        print(f'Replacing value: {bpm_started} --> True')
        affected_doc.set({
            u'bpm_started': True
        })

        global my_affected_doc

        my_affected_doc = affected_doc
        temp_local_filename = "/tmp/" + id + ".mp4"
        # Pre-download setup
        blob = storage_client.bucket(DOWNLOAD_BUCKET_NAME).get_blob(id+".mp4")
        blob.download_to_filename(temp_local_filename)
        # _, temp_local_filename = tempfile.mkstemp(suffix='.mp4')
        bpm = get_file_bpm(temp_local_filename)

        affected_doc.set({
            u'bpm_finished': True,
            u'bpm': bpm
        })
        os.remove(temp_local_filename)
        
    print(str(event))

def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            return 0
    return beats_to_bpm(beats, path)
