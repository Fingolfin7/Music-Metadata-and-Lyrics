import requests
import eyed3
import os
from datetime import datetime
from ColourText import format_text
from check_internet import check_internet


def clean_song_name(song_name=""):
    common_strings = ["(Official Video)", "(Lyrics)", "[Official Video]", "[Lyrics]", "Lyrics", "Official",
                      "Audio", "Video", "(Audio)", "(Video)"]
    song_name = song_name.lower()

    for common_string in common_strings:
        if song_name.find(common_string.lower()) != -1:
            song_name = song_name.replace(common_string.lower(), "")
    return song_name


def remove_non_ascii(in_string=""):
    if in_string.find("’") != -1:
        in_string = in_string.replace("’", "\'")
    if in_string.find("•") != -1:
        in_string = in_string.replace("•", "·")

    for char in in_string:
        if not char.isascii():
            in_string = in_string.replace(char, "")

    return in_string


def remove_special_characters(in_string=""):
    special_chars = "-,:;'_()!@#$%^&*=+|[]<>.~`?•/"

    for char in special_chars:
        if in_string.find(char) != -1:
            in_string = in_string.replace(char, "")

    return remove_non_ascii(in_string)


def get_metadata(song_file, art_option=0):
    if check_internet():
        print(format_text("Searching [italic][yellow]Genius.com[reset] for metadata"))

        song_file = os.path.normpath(song_file)
        song_base_name = os.path.basename(song_file)
        song_base_name = clean_song_name(song_base_name[0:-4])
        audio = eyed3.load(song_file)

        if audio.tag is None:
            audio.initTag()

        query = {"q": f"{song_base_name}",
                 "text_format": "plain"}
        headers = {"Authorization": "Bearer 1GMeKxBJy-XdctY7-7BcfRnWxeeTghUb6YCg71JXHfoLKEDDFdamibvhwrNMsFjS"}

        base_url = "https://api.genius.com/"

        data = requests.get(f"https://api.genius.com/search/", params=query, headers=headers).json()
        found_song = None

        for hit in data['response']['hits']:
            title = remove_non_ascii(hit['result']['title'])
            artist = remove_non_ascii(hit['result']['primary_artist']['name'])

            if song_base_name.lower().find(remove_special_characters(artist.lower())) != -1 or \
                    song_base_name.lower().find(remove_special_characters(title.lower())) != -1:
                found_song = hit
                print(format_text(f"Found: [yellow][italic]'{title}' by '{artist}'[reset]"))
                break
            else:
                return

        if found_song:
            song_id = found_song['result']['id']
            artist = remove_non_ascii(found_song['result']['primary_artist']['name'])

            song_data = requests.get(f"{base_url}songs/{song_id}?text_format=plain", headers=headers).json()
            song_data = song_data['response']['song']
            # print(song_data)

            if song_data['album'] is not None:
                album = remove_non_ascii(song_data['album']['name'])
                album_artist = remove_non_ascii(song_data['album']['artist']['name'])

                if art_option == 0:
                    art_url = song_data['album']['cover_art_url']
                else:
                    art_url = song_data['song_art_image_url']

            else:
                art_url = song_data['song_art_image_url']
                album = song_data['title']
                album_artist = album

            title = song_data['title']

            if song_data['release_date'] is None:
                date_str = song_data['release_date_for_display']
                year = datetime.strptime(date_str, '%Y-%m-%d').year
            else:
                date_str = song_data['release_date']
                year = datetime.strptime(date_str, '%Y-%m-%d').year

            # update tags
            audio.tag.artist = remove_non_ascii(artist)
            audio.tag.album = remove_non_ascii(album)
            audio.tag.album_artist = remove_non_ascii(album_artist)
            audio.tag.year = year
            audio.tag.release_date = year
            audio.tag.title = remove_non_ascii(title)

            print(format_text(f"\nTitle: [italic][yellow]{title}[reset]"
                              f"\nArtist: [italic][yellow]{artist}[reset]"
                              f"\nAlbum: [italic][yellow]{album}[reset]"
                              f"\nAlbum-artist: [italic][yellow]{album_artist}[reset]"
                              f"\nYear: [italic][yellow]{year}[reset]\n")
                  )
            # get file extension
            extension = os.path.splitext(art_url)[1]
            extension = extension[1:]

            if extension.find("?") != -1:
                extension = extension[0: extension.find("?")]

            if extension in ["webp", "WEBP"]:
                art_url = song_data['album']['cover_art_url']
                extension = os.path.splitext(art_url)[1]
                extension = extension[1:]

            r2 = requests.get(art_url)
            #open(f"Album Art/{song_base_name}.{extension}", "wb").write(r2.content)
            audio.tag.images.set(3, r2.content, f'image/{extension}')

            # save for the various tag versions
            audio.tag.save(version=(2, 3, 0))
            audio.tag.save(version=(1, None, None))
            audio.tag.save()

            print("Done!")
        else:
            return "Not found"
    else:
        print("Offline. Cannot run search")


def getSongsList():
    filepath = os.path.normpath(input("Please enter a folder path to play from: "))
    songlist = []
    filelist = os.listdir(filepath)

    for file in filelist:
        if file.endswith(".mp3"):
            songlist.append(str(filepath) + "\\" + file)

    return songlist


for song in getSongsList():
    try:
        get_metadata(song)
    except:
        os.system("pause")

os.system("pause")
