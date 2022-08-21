import os
import io

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import PySimpleGUI as sg
from PIL import Image
import requests

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    layout1 = [[sg.Text('Please authenticate')],
               [sg.Button('auth')]]

    window = sg.Window('YTPM Auth', layout1)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'auth':
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

            api_service_name = "youtube"
            api_version = "v3"
            client_secrets_file = "client_secret_873611161470-5i6re2pfh3mufd5h8d0kivqhqmc602h2.apps.googleusercontent.com.json"

            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server()
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)

            window.close()

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    pl_list = request.execute()
    pl_items = pl_list["items"]

    layout1 = list(range(25))
    num = 0
    for item in pl_items:
        respo = requests.get(item["snippet"]["thumbnails"]["medium"]["url"])
        pil_image = Image.open(io.BytesIO(respo.content))
        png_bio = io.BytesIO()
        pil_image.save(png_bio, format="PNG")
        png_data = png_bio.getvalue()

        layout1[num] = [[sg.Image(data=png_data, key="-PL-IMG-")], [sg.Button(str(item["snippet"]["title"]), key=item["id"])]]
        num += 1

    layout = [[sg.Column(layout1[ite], element_justification='c') for ite in range(num)]]
    window = sg.Window('Choose a playlist', layout, finalize=True)
    window.bring_to_front()
    playlist_id = ""

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event != sg.WIN_CLOSED:
            playlist_id = window[event].key
            break

    window.close()

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
    )
    selected_playlist = request.execute()



if __name__ == "__main__":
    main()
