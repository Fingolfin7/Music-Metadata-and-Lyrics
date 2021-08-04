import json


class SongDict:
    def __init__(self):
        self.dict = {
            "artist":
                [{'song': 'lyrics'}]
        }

        self.load_dict()

    def __str__(self):
        return str(self.dict)

    def save_to_dict(self, artist="", song="", lyrics=""):
        if artist not in self.dict and artist.lower() not in [key.lower() for key in self.dict.keys()]:
            self.dict[artist] = [{song: lyrics}]
        else:
            if ({song: lyrics} not in self.dict[artist]) and (lyrics is not None and lyrics != ""):
                self.dict[artist].append({song: lyrics})

    def save_dict(self):
        json_songs = json.dumps(self.dict, indent=4)
        song_lyrics = open("song_lyrics.json", "w")
        song_lyrics.write(json_songs)
        song_lyrics.close()

    def load_dict(self):
        song_lyrics = open("song_lyrics.json", "r").read()
        self.dict = json.loads(song_lyrics)
