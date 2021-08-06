import requests
from Auth_Code import GENIUS_TOKEN
from check_internet import check_internet
from ColourText import format_text
from SongsDict import *
from bs4 import BeautifulSoup

song_dict = SongDict()


def search_song_lyrics(song_name="", song_artist=""):
    def online_search():
        query = {"q": f"{song_name} {song_artist}",
                 "text_format": "plain"}
        title = ""
        artist = ""
        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

        base_url = "https://api.genius.com/"

        data = requests.get(f"https://api.genius.com/search/", params=query, headers=headers).json()
        found_song = None

        for hit in data['response']['hits']:
            result_title = str(hit['result']['title']).lower() + str(hit['result']['primary_artist']['name']).lower()

            if result_title.find(song_artist.lower()) != -1 or result_title.find(song_name.lower()) != -1:
                found_song = hit
                title = hit['result']['title']
                artist = hit['result']['primary_artist']['name']
                print(format_text(f"Found: [bright yellow][italic]'{title}' by '{artist}'[reset]"))
                break

        if found_song:
            song_id = found_song['result']['id']

            song_data = requests.get(f"{base_url}songs/{song_id}", headers=headers).json()
            path = song_data['response']['song']['path']

            # html scraping (beatifulsoup)
            page = requests.get(f"http://genius.com{path}")
            html = BeautifulSoup(page.text, "html.parser")

            # remove script tags that they put in the middle of the lyrics
            [h.extract() for h in html(['style', 'script'])]

            try:
                # at least Genius is nice and has a tag called 'lyrics'!
                scraped_lyrics = html.find('div', class_='lyrics').get_text()

                # save to dictionary
                song_dict.save_to_dict(artist, title, scraped_lyrics)
                song_dict.save_dict()
            except:
                scraped_lyrics = None

            # return lyrics
            return scraped_lyrics
        else:
            return found_song

    def offline_search():
        for artist_key in song_dict.dict:  # loop through artists
            if artist_key.lower().find(song_artist.lower()) != -1:  # if artist name is found in key
                for song in song_dict.dict[artist_key]:  # loop through song keys in  artist dict
                    if song.lower().find(song_name.lower()) != -1:  # if a song name is found in song key
                        print(format_text(f"Found: [bright yellow][italic]'{song}' by"
                                          f" '{artist_key}'[reset]"))
                        return song_dict.dict[artist_key][song]

        print(format_text(f"Lyrics for [bright yellow][italic]'{song_name}' by '{song_artist}'[reset] not found.\n"))

        for artist_key in song_dict.dict:
            if artist_key.lower().find(song_artist.lower()) != -1:
                print(format_text(f"Songs from [bright yellow][italic]{artist_key}[reset]"))
                index = 0
                for found_song in song_dict.dict[artist_key]:
                    print(format_text(f"[bright yellow][italic]{index + 1}. {found_song}[reset]"))
                    index += 1
                print("")

        return None

    if check_internet():
        count = 0
        print(format_text("Searching [italic][bright yellow]Genius.com[reset] for lyrics"))

        while count < 3:
            value = online_search()
            if value is None:
                print(f"Try {count + 1} failed.\n")
                count += 1
            else:
                return value

        print("Online searched failed. Running local search")
        return offline_search()

    else:
        print("Offline. Running local search.")
        # song_name = remove_special_characters(song_name)
        return offline_search()
