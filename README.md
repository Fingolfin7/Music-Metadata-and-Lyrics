# Music-Metadata-and-Lyrics
Python project that updates metadata (including album art) and searches for lyrics from the Genius API. 

## Update Metadata
`Metadata.py` takes in an mp3 file (or a folder path) and searches for the corresponding metadata from Genius.com using the Genius API and Eyed3 module.

## Search Song Lyrics
`Genius Lyrics.py` takes in a song name and artist name and searches Genius.com for the lyrics. The lyrics are saved to a json file called `song_lyrics.json`. Searches are performed on this saved data when offline.
