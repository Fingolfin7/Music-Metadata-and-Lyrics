import requests
import get_auth_token
from functions import remove_non_ascii
from check_internet import check_internet
from ColourText import format_text
from SongsDict import SongDict
from bs4 import BeautifulSoup

MUSIX_TOKEN = get_auth_token.get_token()['Musixmatch']

if not MUSIX_TOKEN:
    exit()

# a class containing a dictionary with all the saved lyrics from previous searches
song_dict = SongDict()


def search_song_lyrics(song_name="", song_artist=""):
    def online_search():

        # use the song and artist names to search genius.com
        query = {
            "apikey": MUSIX_TOKEN,
            "q_artist": song_artist,
            "q_track": song_name
        }
        try:
            # get the results as a json file
            data = requests.get(f"https://api.musixmatch.com/ws/1.1/", params=query).json()

            lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]

            # if the lyrics are found, add them to the dictionary and return them
            if lyrics:
                song_dict.save_to_dict(song_artist, song_name, lyrics)
                return lyrics
        except KeyError:
            print(format_text(f"Lyrics for [bright yellow][italic]'{song_name}' by '{song_artist}'[reset] not found.\n"))
            return None
        except requests.exceptions.ConnectionError:
            print(format_text(f"Couldn't connect to the internet. Check your connection and try again.\n"))
            z
        return None


    # offline search. search the dictionary object for song lyrics
    def offline_search():
        for artist_key in song_dict.dict:  # loop through artists
            if artist_key.lower().find(song_artist.lower()) != -1:  # if artist name is found in key
                for song in song_dict.dict[artist_key]:  # loop through song keys in  artist dict
                    if song.lower().find(song_name.lower()) != -1:  # if a song name is found in song key
                        print(format_text(f"Found: [bright yellow][italic]'{song}' by"
                                          f" '{artist_key}'[reset]"))
                        return song_dict.dict[artist_key][song]
        return None

    # first try an offline search
    song_artist = remove_non_ascii(song_artist)
    song_name = remove_non_ascii(song_name)
    offline_search = offline_search()

    if offline_search is not None:
        return offline_search

    # if nothing is found, and there is an internet connection, do an online search
    elif check_internet() and offline_search is None:
        count = 0
        print(format_text("Searching [italic][bright yellow]Genius.com[reset] for lyrics"))

        while count < 3:  # Try online search 3 times before doing an offline search
            value = online_search()
            if not value:
                print(format_text(f"[italic][bright red]Try {count + 1} failed.[reset]\n"))
                count += 1
            else:
                return value

    # if nothing was found from the offline and online searches
    print(format_text(f"Lyrics for [bright yellow][italic]'{song_name}' by '{song_artist}'[reset] not found.\n"))

    # if the song isn't found, search for the artist and print a list of the available song lyrics
    for artist_key in song_dict.dict:
        if artist_key.lower().find(song_artist.lower()) != -1:
            print(format_text(f"Songs from [bright yellow][italic]{artist_key}[reset]"))

            index = 0
            for found_song in song_dict.dict[artist_key]:
                print(format_text(f"[bright yellow][italic]{index + 1}. {found_song}[reset]"))
                index += 1
            print()
    return None


def main():
    import os
    os.system("cls")
    while True:
        input_song = input("Enter song name: ")
        input_artist = input("Enter song artist: ")
        print("")
        print(search_song_lyrics(input_song, input_artist))
        input()


if __name__ == "__main__":
    main()
