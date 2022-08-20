import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import PySimpleGUI as sg

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
    response = request.execute()

    layout = [[sg.Text('Some text on Row 1')],
              [sg.Text('Enter something on Row 2'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window('Youtube Playlist Manager', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Ok':
            request = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                pageToken="EAAaB1BUOkNPZ0g",
                playlistId="PLGDnnSanD6iiJGSPEQgmP4AWpO1Dx9RHK"
            )
            response = request.execute()
            print(response)

    window.close()



if __name__ == "__main__":
    main()