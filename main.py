import os
import io

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import PySimpleGUI as sg
from PIL import Image
import requests
import pyperclip


class Table(sg.Table):
    def _RightClickMenuCallback(self, event):
        self.user_event = event
        self.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
        self.TKRightClickMenu.grab_release()

    def position(self, event):
        region = self.Widget.identify('region', event.x, event.y)
        if region == 'heading':
            row = -1
        elif region == 'cell':
            row = int(self.Widget.identify_row(event.y)) - 1
        elif region == 'separator':
            row = None
        else:
            row = None
        col_identified = self.Widget.identify_column(event.x)
        if col_identified:
            column = int(self.Widget.identify_column(event.x)[1:]) - 1 - int(self.DisplayRowNumbers is True)
        else:
            column = None
        return row, column


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
working_directory = os.getcwd()


def main():
    layout1 = [[sg.Text('Please authenticate. Browse to your client secret json file then click login')],
               [sg.InputText(key="-FILE_PATH-"), sg.FileBrowse(initial_folder=working_directory, file_types=(("JSON Files", "*.json"),), key="-BROWSE-")],
               [sg.Button('Click here to Login')]]

    window = sg.Window('YT API Auth', layout1, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Click here to Login':
            if values["-FILE_PATH-"] == "":
                sg.Popup('Browse to your secret json file first before logging in', keep_on_top=True)
                continue
            else:
                os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

                api_service_name = "youtube"
                api_version = "v3"
                client_secrets_file = values["-FILE_PATH-"]

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
                        [sg.Button(str(item["snippet"]["title"]),
                                   key=item["id"] + " " + str(item["contentDetails"]["itemCount"]))]]
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
              [sg.ProgressBar(playlist_count, orientation='h', size=(50, 20), border_width=4, key='-PROGRESS_BAR-',
                              bar_color=("deep sky blue", "snow"))],
              [sg.Text("0/" + playlist_count, key='-PROGRESS_TEXT-')]
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
    data = []
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
                data.append([sp_item["snippet"]["title"],
                             "https://www.youtube.com/watch?v=" + str(sp_item["snippet"]["resourceId"][
                                                                          "videoId"]), sp_item["id"]])
            elif res["pageInfo"]["totalResults"] > 0:
                if "regionRestriction" in res["items"][0]["contentDetails"]:
                    if "blocked" in res["items"][0]["contentDetails"]["regionRestriction"]:
                        for block in res["items"][0]["contentDetails"]["regionRestriction"]["blocked"]:
                            if block == "PH":
                                data.append([sp_item["snippet"]["title"],
                                             "https://www.youtube.com/watch?v=" + str(sp_item["snippet"]["resourceId"][
                                                                                          "videoId"]), sp_item["id"]])

        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            pageToken=nextToken,
            playlistId=playlist_id
        )
        selected_playlist = request.execute()

    window.close()

    headings = ["Title", "Link", "Video ID"]
    right_click_menu = ['&Right', ['Copy']]

    layout = [
        [Table(data, headings=headings, expand_x=True, expand_y=True, enable_events=True, auto_size_columns=True, display_row_numbers=True,
               justification='center', right_click_menu=right_click_menu, key='-TABLE-')],
        [sg.Button("Open playlist video removal window", key="del"),
         sg.Text("You can right click any field to copy the text")]
    ]
    window = sg.Window("All unavailable videos in your playlist", layout, finalize=True, resizable=True, size=(900,400))
    table = window["-TABLE-"]

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Copy":
            e = table.user_event
            row, col = position = table.position(e)
            if None not in position and row >= 0:
                text = data[row][col]
                print(text)
                pyperclip.copy(text)
        elif event == "del":
            layout2 = [
                [sg.Text('Video ID'), sg.Input(key='_IN_')],
                [sg.Button("Remove", key="rem"),
                 sg.Text("Enter the Video ID of the video you wish to remove from your playlist", key="rem_status")]
            ]
            window = sg.Window("Remove video from playlist", layout2, finalize=True)
            while True:
                event, values = window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "rem":
                    window['rem_status'].update("Removing...")
                    request = youtube.playlistItems().delete(
                        id=values["_IN_"]
                    )
                    test = request.execute()
                    window['rem_status'].update("Success!")

            window.close()
    window.close()


if __name__ == "__main__":
    main()
