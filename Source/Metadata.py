import requests
import re
import eyed3  # module for editing mp3 metadata tags
import os
import get_auth_token
from functions import remove_non_ascii, remove_special_characters
from datetime import datetime
from ColourText import format_text  # a function I made to color and format text using ascii escape codes
from check_internet import check_internet

GENIUS_TOKEN = get_auth_token.get_token()

if GENIUS_TOKEN is None:
    print('Please create the auth_token.txt file inside the Source folder and put in a Genius Token.')
    exit()


# function to clean a given string for the genius api search
def clean_song_name(song_name=""):
    problem_strings = ["Feat", "FT", "HD", "Lyrics", "Official", "Audio", "Video"]
    song_name = song_name.lower()

    pattern = r"\[.*?\]"
    song_name = re.sub(pattern, "", song_name)

    pattern = r"\(.*?\)"
    song_name = re.sub(pattern, "", song_name)

    for problem_sting in problem_strings:
        while song_name.find(problem_sting.lower()) != -1:
            song_name = song_name.replace(problem_sting.lower(), " ")

    while song_name.find("_") != -1:
        song_name = song_name.replace("_", " ")

    song_name = " ".join(song_name.split())  # remove whitespace

    return song_name


# takes in a song file name, searches genius.com for the metadata, and updates the mp3 file.
def get_metadata(song_file, art_option=0):
    if check_internet():  # check for an internet connection.
        print(format_text("Searching [italic][bright yellow]Genius.com[reset] for metadata\n"))

        song_file = os.path.normpath(song_file)

        # get the cleaned basename for the file, minus the file extension
        song_base_name = os.path.basename(song_file)
        song_base_name = clean_song_name(song_base_name[0:-4])

        # set the log level for eyed3 to Error to avoid spamming the console
        eyed3.log.setLevel("ERROR")

        # load in and Init an audio tag
        audio = eyed3.load(song_file)

        if audio.tag is None:
            audio.initTag()

        # search genius.com using the cleaned file name. Using the api token for authorization
        query = {"q": f"{song_base_name}",
                 "text_format": "plain"}

        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

        base_url = "https://api.genius.com/"

        # getting the request back in a json format
        data = requests.get(f"https://api.genius.com/search/", params=query, headers=headers).json()

        found_song = None

        # search through the array of 'hits' from the search request
        for hit in data['response']['hits']:
            title = remove_non_ascii(hit['result']['title'])
            artist = remove_non_ascii(hit['result']['primary_artist']['name'])

            # look for either the artist's name or the song name in the song name we used for the search
            if song_base_name.lower().find(remove_special_characters(artist.lower())) != -1 or \
                    song_base_name.lower().find(remove_special_characters(title.lower())) != -1:

                # if we can find either we can assume that we found the correct song and set 'found_song' to our
                # search hit
                found_song = hit

                print(format_text(f"Found: [bright yellow][italic]'{title}' by '{artist}'[reset]"))
                break
            else:
                print(format_text(f"Couldn't find anything for [bright yellow][italic]{song_base_name}[reset]\n"))
                return

            # if the search was successful, and we have found a hit
        if found_song:
            song_id = found_song['result']['id']  # get the id of the song which we'll use for another search
            artist = remove_non_ascii(
                found_song['result']['primary_artist']['name'])  # get the artist name from the search hit

            # run another search to get the sing data from genius using the id
            song_data = requests.get(f"{base_url}songs/{song_id}?text_format=plain", headers=headers).json()
            song_data = song_data['response']['song']
            # print(song_data)

            if song_data['album']:  # if the album data is set
                album = remove_non_ascii(song_data['album']['name'])
                album_artist = remove_non_ascii(song_data['album']['artist']['name'])

                if art_option == 0:  # if this is 0 then get the url for the album art rather than the song art image
                    art_url = song_data['album']['cover_art_url']
                    if art_url is None:  # in the case that there is no album art get the song art url
                        art_url = song_data['song_art_image_url']
                else:  # if art_option is set to 1 (or anything other than 0) get the song art image
                    art_url = song_data['song_art_image_url']
                    if art_url is None:  # if there is no song art, get the album art
                        art_url = song_data['album']['cover_art_url']

            else:  # in the case that there is no album data
                art_url = song_data['song_art_image_url']
                album = song_data['title']
                album_artist = artist

            # get the title of the song
            title = song_data['title']

            # get the year it was released
            if song_data['release_date']:
                date_str = song_data['release_date']
                year = datetime.strptime(date_str, '%Y-%m-%d').year
            elif song_data['release_date_for_display']:
                date_str = song_data['release_date_for_display']
                year = date_str[-4:]
            else:
                year = ""

            # remove old tag data
            audio.tag.remove(song_file)
            # remove old song/album art
            for img in audio.tag.images:
                audio.tag.images.remove(img.description)

            # update tags
            audio.tag.artist = remove_non_ascii(artist)
            audio.tag.album = remove_non_ascii(album)
            audio.tag.album_artist = remove_non_ascii(album_artist)
            audio.tag.year = year
            audio.tag.release_date = year
            audio.tag.title = remove_non_ascii(title)

            print(format_text(f"\nTitle: [italic][bright yellow]{title}[reset]"
                              f"\nArtist: [italic][bright yellow]{artist}[reset]"
                              f"\nAlbum: [italic][bright yellow]{album}[reset]"
                              f"\nAlbum-artist: [italic][bright yellow]{album_artist}[reset]"
                              f"\nYear: [italic][bright yellow]{year}[reset]\n")
                  )

            # get file extension for the album/art image
            extension = os.path.splitext(art_url)[1]
            extension = extension[1:]

            # came across a few cases were extension came out like png?127838, so this is here to remove everything
            # from the ? forward
            if extension.find("?") != -1:
                extension = extension[0: extension.find("?")]

            # webp images refuse to save for some reason, so if the extension is webp, try and get the album cover
            # art which is usually a png or jpeg
            if extension in ["webp", "WEBP"]:
                art_url = song_data['album']['cover_art_url']
                extension = os.path.splitext(art_url)[1]
                extension = extension[1:]

            # get the image as a request
            r2 = requests.get(art_url)
            # save the request content to the file
            audio.tag.images.set(3, r2.content, f'image/{extension}')

            # save for the various tag versions
            audio.tag.save(version=(2, 3, 0))
            audio.tag.save(version=(1, None, None))
            audio.tag.save()

            print("Done!")
        else:
            return None
    else:
        print("Offline. Cannot run search")


def getSongsList():
    file_path = os.path.normpath(input("Please enter a folder path: "))

    return [(str(file_path) + "\\" + file) for file in os.listdir(file_path) if file.endswith(".mp3")]


os.system("cls")

for song in getSongsList():
    get_metadata(song)

os.system("pause")
