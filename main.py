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
               [sg.Button('Click here to Login')]]

    window = sg.Window('YTPM Auth', layout1)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Click here to Login':
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

        layout1[num] = [[sg.Image(data=png_data, key="-PL-IMG-")],
                        [sg.Button(str(item["snippet"]["title"]), key=item["id"]+" "+str(item["contentDetails"]["itemCount"]))]]
        num += 1

    layout = [[sg.Column(layout1[ite], element_justification='c') for ite in range(num)]]
    window = sg.Window('Choose a playlist', layout, finalize=True)
    window.bring_to_front()
    playlist_id = ""
    playlist_count = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event != sg.WIN_CLOSED:
            txt = window[event].key
            playlist_id = txt.split()[0]
            playlist_count = txt.split()[1]
            break

    window.close()

    layout = [[sg.Text("Checking the videos in the playlist. Please wait")],
        [sg.ProgressBar(playlist_count, orientation='h', size=(50,20), border_width=4, key='-PROGRESS_BAR-', bar_color=("deep sky blue", "snow"))],
              [sg.Text("0/"+playlist_count, key='-PROGRESS_TEXT-')]
    ]

    window = sg.Window("Loading", layout, finalize=True)
    loading_progress = 0

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
    )
    selected_playlist = request.execute()
    cont = True
    nextToken = ""
    while cont:
        if "nextPageToken" in selected_playlist:
            nextToken = selected_playlist["nextPageToken"]
        else:
            cont = False

        for sp_item in selected_playlist["items"]:
            loading_progress += 1
            window['-PROGRESS_BAR-'].update(loading_progress)
            window['-PROGRESS_TEXT-'].update(str(loading_progress) + "/" + str(playlist_count))

            request = youtube.videos().list(
                part="contentDetails",
                id=sp_item["snippet"]["resourceId"]["videoId"]
            )
            res = request.execute()
            if res["pageInfo"]["totalResults"] == 0:
                print(sp_item["snippet"]["title"] + " ==== " + sp_item["snippet"]["resourceId"][
                    "videoId"] + " ==== " + sp_item["id"])
            elif res["pageInfo"]["totalResults"] > 0:
                if "regionRestriction" in res["items"][0]["contentDetails"]:
                    if "blocked" in res["items"][0]["contentDetails"]["regionRestriction"]:
                        for block in res["items"][0]["contentDetails"]["regionRestriction"]["blocked"]:
                            if block == "PH":
                                print(sp_item["snippet"]["title"] + " ==== " + sp_item["snippet"]["resourceId"][
                                    "videoId"] + " ==== " + sp_item["id"])

        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            pageToken=nextToken,
            playlistId=playlist_id
        )
        selected_playlist = request.execute()

    window.close()





if __name__ == "__main__":
    main()
