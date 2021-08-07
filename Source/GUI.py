import os
import threading
from tkinter import *
from tkinter import messagebox
from GeniusLyrics import search_song_lyrics, song_dict


def search(event=None):
    def thread_func():
        os.system("cls")
        print(f"Song: {songName.get()}\nArtist: {artistName.get()}")
        lyrics = search_song_lyrics(songName.get(), artistName.get())
        if lyrics:

            if lyrics[0] == "\n" and lyrics[1] == "\n":
                lyrics = lyrics[2:]

            print(lyrics)

            # pack and attach to textbox
            scrollbar.pack(side=RIGHT, fill=Y)
            output.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=output.yview)

            # pack output
            output.pack(side=BOTTOM, fill=BOTH)
            output.delete(1.0, "end")
            output.insert(1.0, lyrics)
        else:
            messagebox.showinfo(
                "Failed",
                f"Couldn't find fyrics for\n'{songName.get()}' by '{artistName.get()}'"
            )

    search_thread = threading.Thread(target=thread_func)
    search_thread.start()


root = Tk()
root.title('Music Metadata and Lyrics')
root.resizable(width=False, height=False)
frame = Frame(root)

songName = StringVar()
artistName = StringVar()

top_section = LabelFrame(frame, font="Calibri", pady=2)

Label(top_section, text="Song").pack(side=LEFT, padx=4)
songEntry = Entry(top_section, textvariable=songName)
songEntry.pack(side=LEFT, padx=4)

Label(top_section, text="Artist").pack(side=LEFT, padx=4)
artistName = Entry(top_section, textvariable=artistName)
artistName.pack(side=LEFT, padx=4)

searchButton = Button(top_section, text="Search")
searchButton.bind("<Button-1>", search)
root.bind("<Return>", search, add="+")
searchButton.pack(side=LEFT)

output = Text(frame, font="Calibri 11", width=root.winfo_width(), height=25)

# create scrollbar
scrollbar = Scrollbar(frame)

top_section.pack(side=TOP)
frame.pack()
root.mainloop()
