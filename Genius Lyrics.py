import requests
import os
from check_internet import check_internet
from ColourText import format_text
from songs_dict import *
from bs4 import BeautifulSoup

song_dict = SongDict()


def search_song_lyrics(song_name="", song_artist=""):
    def online_search():
        query = {"q": f"{song_name} {song_artist}",
                 "text_format": "plain"}
        title = ""
        artist = ""
        headers = {"Authorization": "Bearer 1GMeKxBJy-XdctY7-7BcfRnWxeeTghUb6YCg71JXHfoLKEDDFdamibvhwrNMsFjS"}

        base_url = "https://api.genius.com/"

        data = requests.get(f"https://api.genius.com/search/", params=query, headers=headers).json()
        found_song = None

        for hit in data['response']['hits']:
            result_title = str(hit['result']['title']).lower() + str(hit['result']['primary_artist']['name']).lower()

            if result_title.find(song_artist.lower()) != -1 or result_title.find(song_name.lower()) != -1:
                found_song = hit
                title = hit['result']['title']
                artist = hit['result']['primary_artist']['name']
                print(format_text(f"Found: [yellow][italic]'{title}' by '{artist}'[reset]"))
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
        for artist_key in song_dict.dict.keys():  # loop through artists
            if artist_key.lower().find(song_artist.lower()) != -1:  # if artist name is found in key
                for pair in song_dict.dict[artist_key]:  # loop through song-lyric pairs in dict
                    for song_key in pair.keys():  # loop through song keys
                        if song_key.lower().find(song_name.lower()) != -1 and\
                                artist_key.lower().find(song_artist.lower()) != -1:  # if a song name is found in song key
                            print(format_text(f"Found: [yellow][italic]'{song_key}'[reset] by"
                                              f" '[yellow][italic]{artist_key}'[reset]"))
                            return pair[song_key]

        print(format_text(
            f"Lyrics for [yellow][italic]{song_name}[reset] by [yellow][italic]{song_artist}[reset] not found.\n"))

        for artist_key in song_dict.dict.keys():
            if artist_key.lower().find(song_artist.lower()) != -1:
                print(format_text(f"Songs from [yellow][italic]{artist_key}[reset]"))
                index = 0
                for found_pair in song_dict.dict[artist_key]:
                    found_keys = list(found_pair.keys())[0]
                    print(format_text(f"[yellow][italic]{index + 1}. {str(found_keys)}[reset]"))
                    index += 1
                print("")

        return None

    if check_internet():
        count = 0
        print(format_text("Searching [italic][yellow]Genius.com[reset] for lyrics"))

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


os.system("cls")
lyrics = search_song_lyrics("We Didn’t Start the Fire", "Billy Joel")
if lyrics is not None:
    print(format_text(f"[italic][yellow]{lyrics}[reset]"))
os.system("pause")
