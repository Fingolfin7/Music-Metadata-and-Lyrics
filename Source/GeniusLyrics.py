import re
import get_auth_token
import lyricsgenius
from functions import remove_non_ascii
from check_internet import check_internet
from ColourText import format_text
from SongsDict import SongDict

GENIUS_TOKEN = get_auth_token.get_token()

if GENIUS_TOKEN is None:
    print('Please create the auth_token.txt file inside the Source folder and put in a Genius Token.')
    exit()

# a class containing a dictionary with all the saved lyrics from previous searches
song_dict = SongDict()


def search_song_lyrics(song_name="", song_artist=""):
    def online_search():

        genius = lyricsgenius.Genius(GENIUS_TOKEN)
        song = genius.search_song(song_name, song_artist)
        if song:
            title = song.title
            artist = song.artist
            print(format_text(f"Found: [bright yellow][italic]'{title}' by '{artist}'[reset]"))

            lyrics = song.lyrics

            # regex to place newlines before and after square brackets
            lyrics = re.sub(r"(\[)", r"\n\1", lyrics)
            lyrics = re.sub(r"(\])", r"\1\n", lyrics)

            # more cleaning with regexes
            lyrics = re.sub(r'\d*\s?Contributors?', '', lyrics)
            lyrics = re.sub(r'\d*\s?Embed', '', lyrics)

            # clean up non-ascii characters
            artist = remove_non_ascii(artist)
            title = remove_non_ascii(title)

            # save the lyrics to the dictionary
            song_dict.save_to_dict(artist, title, lyrics)
            song_dict.save_dict()
            return lyrics
        else:
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
            if value is None:
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
