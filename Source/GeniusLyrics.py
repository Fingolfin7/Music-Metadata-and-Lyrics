import requests
import get_auth_token
from functions import remove_non_ascii
from check_internet import check_internet
from ColourText import format_text
from SongsDict import SongDict
from bs4 import BeautifulSoup

GENIUS_TOKEN = get_auth_token.get_token()

if GENIUS_TOKEN is None:
    print('Please create the auth_token.txt file inside the Source folder and put in a Genius Token.')
    exit()

# a class containing a dictionary with all the saved lyrics from previous searches
song_dict = SongDict()


def search_song_lyrics(song_name="", song_artist=""):
    def online_search():

        # use the song and artist names to search genius.com
        query = {"q": f"{song_name} {song_artist}",
                 "text_format": "plain"}
        title = ""
        artist = ""
        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

        base_url = "https://api.genius.com/"

        # get the results as a json file
        data = requests.get(f"https://api.genius.com/search/", params=query, headers=headers).json()

        found_song = None

        # searches the returned hits
        for hit in data['response']['hits']:
            # compare the returned song title and artist name to the function arguments
            result_title = str(hit['result']['title']).lower() + str(hit['result']['primary_artist']['name']).lower()

            if result_title.find(song_artist.lower()) != -1 or result_title.find(
                    song_name.lower()) != -1:  # if we can find the artist or song name, then we have found our song
                found_song = hit
                title = hit['result']['title']
                artist = hit['result']['primary_artist']['name']
                print(format_text(f"Found: [bright yellow][italic]'{title}' by '{artist}'[reset]"))
                break

        if found_song:  # if we have found a hit
            song_id = found_song['result']['id']  # get the song's id

            # search genius for the song using it's id and get the 'path' to the document containing the song's lyrics
            song_data = requests.get(f"{base_url}songs/{song_id}", headers=headers).json()
            path = song_data['response']['song']['path']

            # use beautifulsoup to scrape the lyric page for just the song lyrics
            page = requests.get(f"http://genius.com{path}")
            html = BeautifulSoup(page.text, "html.parser")

            # remove script tags that they put in the middle of the lyrics
            [h.extract() for h in html(['style', 'script'])]

            try:
                # Genius nice and has a tag called 'lyrics'
                scraped_lyrics = html.find('div', class_='lyrics').get_text()

                # save to the dictionary object. These can then be retrieved later on for an offline search
                artist = remove_non_ascii(artist)
                title = remove_non_ascii(title)
                song_dict.save_to_dict(artist, title, scraped_lyrics)
                song_dict.save_dict()
            except:
                scraped_lyrics = None

            # return lyrics
            return scraped_lyrics
        else:
            return found_song

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
    elif check_internet() and offline_search is None:  # if there is an internet connection, run an online search
        count = 0
        print(format_text("Searching [italic][bright yellow]Genius.com[reset] for lyrics"))

        while count < 3:  # Try online search 3 times before doing an offline search
            value = online_search()
            if value is None:
                print(f"Try {count + 1} failed.\n")
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
                print("")
    return None
