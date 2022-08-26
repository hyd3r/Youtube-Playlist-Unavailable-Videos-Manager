# Donate
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=VC5HQFERW6276)

# Description
Getting tired of your youtube playlist having multiple videos that are unavailable (ex. privated videos, deleted videos or restricted video in your country)?

![firefox_c](https://user-images.githubusercontent.com/42913116/186098771-c4869d4d-0910-4f43-b8a8-9d05658dc1d2.png)

Youtube's tools for playlists are horrendous, you can't even see all the unavailable videos in your list so you can replace it. Sometimes a video looks normal in the playlist but if you opened it, it'll show it's unavailable

I have alot of videos in YT playlist because I use youtube for my music. Every other week, some music gets suddenly unavailable. So I made an app to replace the missing videos.

This app checks every video in your playlist for videos that are restricted in your region, privated by the uploader, deleted because of copyright.

It uses the Youtube API v3 and you need to login to the youtube account that owns the playlist

It then displays the video title, url link (so you can search it in the google or in waybackmachine to know the original title), and the video ID for the playlist (important for removing a video in a playlist)

I also added a way to remove a video from a playlist using the 'video ID' provided

# Video showcase
[![Showcase](http://i3.ytimg.com/vi/Kyv4HjHCtXs/hqdefault.jpg)](https://www.youtube.com/watch?v=Kyv4HjHCtXs)


# Instructions
Youtube API has a daily quota limit. It's hard to reach it if you're the only user with a couple of videos, but with multiple users and a ton of videos in their playlist, it'll fill up fast. The user should generate their own client ID key. For now atleast

* Generate API Keys. For instructions on how, see [below section](#Generating-API-key).
* Download, or clone this repository
* Download [Python](https://www.python.org/downloads/). (Make sure to check `Add to PATH`)
* Open a Command Prompt
* Navigate to where the `main.py` is located and type `cd (PASTE DIRECTORY HERE)`
* Then type `main.py` to run (If there is an error, search in google for how to add python to PATH)
* On the first screen, browse to your Client ID you downloaded earlier, then choose your region from the dropdown then click login
* Google login will open and make sure to login the gmail you entered in `Test Users` in `OAuth Consent Screen`
* Choose a playlist you want to check for unavailable videos
* When done, a table will show the video title, url link and video ID(Copy this to the button below if you want to remove it from your playlist)
* Normally you search for the video title to replace it, but if it is Deleted or Privated, you can copy the url link to google or the waybackmachine. It will show you its title before it got deleted or privated

# Generating API key
- Go to the [Google Developer's Console](https://console.developers.google.com/).
  You will need to login with a Google account.
- You should see something like below. Click on the `Select a project`.
- Select `NEW PROJECT` in the popup.
- You will be asked to give it a name. It doesn't matter what name you choose,
  so long as it means something to you. For the purposes of this tutorial, I am
  going to call it `yt-pl-u-c`.
- Click on `create`.
- Click `select project`.
- In the left bar there should be something that says `APIs and Services`. Hover
  over it and click `Library` when it expands.
- In the search box search for the `YouTube Data API v3`. When it comes up as a
  result, click it.
- Click `Enable`.
- When the page loads, click `Create Credentials` in the top right corner.
- Make sure the `YouTube Data API v3` is the selected API.
- You need to select that the API will be accessing `User Data`.
- Click `Next`.
- Fill in information about the `OAuth Consent Screen`. This is the screen that
  pops up for users when they need to allow access to this app, so provide a
  user friendly name and your contact info.
  Make sure to leaving in "Testing" mode, and add your email, and the email of
  anyone else you want to use this as "Test users":
- Click `Save and Continue`.
- Now select scopes. For this app you only need the `YouTube Read Only Scope`.
  - Click `Add or Remove Scopes`. Filter for `youtube.force-ssl`. Check it and
    click `Update`.
- Your Scopes should looks like this:

- Click `Save and Continue`.
- For the `Application Type`, select `Desktop App`, give it any name you want.
- Click `Create`.
- It may take some time, but for me took just a few seconds.
- You should then get a `Client ID`. Download this as you will need to browse to it before logging in the app

You are done creating your API Key (The Client ID).
