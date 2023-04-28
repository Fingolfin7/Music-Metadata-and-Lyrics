# Music-Metadata-and-Lyrics
Python project that updates metadata (including album art) and searches for lyrics from the Genius API. 

## Requirements
* A [Genius API Token](https://docs.genius.com/#/getting-started-h1)


## Getting the project

Download the project or clone it with git. You can create a virtual environment if you can.
Install the requisites by running

```
pip install -r requirements.txt
```

You will need to create an `auth_token.txt` file in the `Source` folder and paste a Genius token inside it. 
You can generate a genius token [here](https://docs.genius.com/#/getting-started-h1)

## Update Metadata
`Metadata.py` takes in an mp3 file (or a folder path) and searches for the corresponding metadata from Genius.com using the Genius API and Eyed3 module.

__Here is an example in a test folder I made:__

![image](https://user-images.githubusercontent.com/63872314/128647612-7f2d8515-69ad-4739-b986-fe6ce9ef14d1.png)

__Run Metadata Search (collected from Genius.com):__

![image](https://user-images.githubusercontent.com/63872314/128647830-2b3e475a-8fe5-41d5-9aa5-fe424e63d00e.png)

__Finished Search:__

![image](https://user-images.githubusercontent.com/63872314/128647739-e025fb6e-d320-4e5d-88e7-4eb40c8e175e.png)

__Updated mp3 file:__

![image](https://user-images.githubusercontent.com/63872314/128647768-c0492c67-567c-4e8a-b6b5-4eba72a060f9.png)

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






