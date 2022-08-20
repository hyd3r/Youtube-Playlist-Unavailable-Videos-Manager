import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_873611161470-5i6re2pfh3mufd5h8d0kivqhqmc602h2.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        pageToken="EAAaB1BUOkNPZ0g",
        playlistId="PLGDnnSanD6iiJGSPEQgmP4AWpO1Dx9RHK"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()