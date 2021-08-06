# Music-Metadata-and-Lyrics
Python project that updates metadata (including album art) and searches for lyrics from the Genius API. 

## Prerequisites
* Python 3
* BeautifulSoup module
* Eyed3 module

These modules can be installed using `pip install`

## Update Metadata
`Metadata.py` takes in an mp3 file (or a folder path) and searches for the corresponding metadata from Genius.com using the Genius API and Eyed3 module.

__Here is an example in a test folder I made:__

![image](https://user-images.githubusercontent.com/63872314/128447097-ededaaad-9bea-4273-a653-b72e134a9da5.png)

__Run Metadata Search (collected from Genius.com):__

![image](https://user-images.githubusercontent.com/63872314/128447244-50ff1129-283f-4468-b515-7a03ecc0d511.png)

__Updated mp3 file:__

![image](https://user-images.githubusercontent.com/63872314/128447351-ac50ae19-5c14-4fa3-bb67-fdf234412721.png)

Metadata.py contains the funtcion get_metadata,

```python
get_metadata(song_file, art_option=0)
```

Which is called with a file path to an mp3 file, and an optional `art_option` which is set to 0 by default.

Setting `art_option` to 0 will update the file with the songs *Album Art*,

Setting it to 1 will update the file to the songs *Song Art*, which sometimes differ.

## Search Song Lyrics
`GeniusLyrics.py` takes in a song name and artist name and searches Genius.com for the lyrics. The lyrics are saved to a json file called `song_lyrics.json`. Searches are performed on this saved data when offline. Here is an example, running `GUI.py` which is a simple gui for getting song lyrics

__Example Search__:

![image](https://user-images.githubusercontent.com/63872314/128579595-604eba7a-b5f2-4a3b-936d-5d20945767e9.png)

__Output__:

![image](https://user-images.githubusercontent.com/63872314/128579639-bb099cbe-0d5d-4a0f-99af-fe760f9c8308.png)

## Contribute to the project
Take a look, run the code, and contribute if you'd like!






