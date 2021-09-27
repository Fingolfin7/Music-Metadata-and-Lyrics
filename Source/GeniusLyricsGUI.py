import os
import threading
from tkinter import *
from tkinter import messagebox
from GeniusLyrics import search_song_lyrics, song_dict


class GeniusLyricsGUI:
    def __init__(self, tk_root: Tk):
        tk_root.resizable(width=False, height=False)
        self.lyrics_frame = Frame(tk_root)

        self.songName = StringVar()
        self.artistName = StringVar()

        self.top_section = LabelFrame(self.lyrics_frame, font="Calibri", pady=2)

        Label(self.top_section, text="Song").pack(side=LEFT, padx=4)
        self.songEntry = Entry(self.top_section, textvariable=self.songName)
        self.songEntry.pack(side=LEFT, padx=4)

        Label(self.top_section, text="Artist").pack(side=LEFT, padx=4)
        self.artistName = Entry(self.top_section, textvariable=self.artistName)
        self.artistName.pack(side=LEFT, padx=4)

        self.searchButton = Button(self.top_section, text="Search")
        self.searchButton.bind("<Button-1>", self.search)
        tk_root.bind("<Return>", self.search)
        self.searchButton.pack(side=LEFT)

        # create scrollbar
        self.scrollbar = Scrollbar(self.lyrics_frame)

        self.top_section.pack(side=TOP)
        self.output = Text(self.lyrics_frame, font="Calibri 11", width=self.top_section.winfo_width(), height=25)
        self.lyrics_frame.pack()

    def search(self, event=None):
        def thread_func():
            os.system("cls")
            print(f"Song: {self.songName.get()}\nArtist: {self.artistName.get()}\n")
            lyrics = search_song_lyrics(self.songName.get(), self.artistName.get())
            if lyrics:

                if lyrics[0] == "\n" and lyrics[1] == "\n":
                    lyrics = lyrics[2:]

                print(lyrics)

                # pack and attach to textbox
                self.scrollbar.pack(side=RIGHT, fill=Y)
                self.output.config(yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.output.yview)

                # pack output
                self.output.pack(side=BOTTOM, fill=BOTH)
                self.output.delete(1.0, "end")
                self.output.insert(1.0, lyrics)
            else:
                messagebox.showinfo(
                    "Failed",
                    f"Couldn't find lyrics for\n'{self.songName.get()}' by '{self.artistName.get()}'"
                )

        search_thread = threading.Thread(target=thread_func)
        search_thread.start()


def main():
    root = Tk()
    root.title('Music Metadata & Lyrics')
    root.resizable(width=False, height=False)

    GeniusLyricsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
