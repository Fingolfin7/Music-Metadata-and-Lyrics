import json


class SongDict:
    def __init__(self):
        self.dict = {}
        self.load_dict()
        self.lower_keys = [key.lower() for key in self.dict]

    def __str__(self):
        return str(self.dict)

    def save_to_dict(self, artist="", song="", lyrics=""):
        if artist.lower() not in self.lower_keys:
            self.dict[artist] = {song: lyrics}
            self.lower_keys.append(artist.lower())
        else:
            for key in self.dict:
                if key.lower().find(artist.lower()) != -1:
                    self.dict[key][song] = lyrics

    def save_dict(self):
        json_songs = json.dumps(self.dict, indent=4)
        song_lyrics = open("song_lyrics.json", "w")
        song_lyrics.write(json_songs)
        song_lyrics.close()

    def load_dict(self):
        try:
            song_lyrics = open("song_lyrics.json", "r").read()
            self.dict = json.loads(song_lyrics)
        except FileNotFoundError:
            open("song_lyrics.json", "w")
        except json.decoder.JSONDecodeError:
            pass
