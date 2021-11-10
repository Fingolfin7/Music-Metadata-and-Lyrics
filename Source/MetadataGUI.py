import os
import threading
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from Metadata import get_metadata, getSongsList
from tkinter.filedialog import askopenfilename


class MetadataGUI:
    def __init__(self, tk_root: Tk):
        tk_root.resizable(width=False, height=False)
        self.frame = Frame(tk_root)
        self.top = LabelFrame(self.frame)
        self.bottom = LabelFrame(self.frame)
        self.artFrame = LabelFrame(self.frame)

        # vars
        self.fileStr = StringVar()
        self.img = None
        self.imgLabel = Label(self.artFrame, image='')
        self.title = StringVar()
        self.artist = StringVar()
        self.album = StringVar()
        self.album_artist = StringVar()
        self.year = StringVar()
        self.boolVar = BooleanVar()

        # topSide
        Label(self.top, text="Enter file/folder path").grid(row=0, column=0, sticky=W, padx=4)

        self.file_path = Entry(self.top, textvariable=self.fileStr, width=45)
        self.file_path.grid(row=0, column=1, sticky=W, padx=4)

        self.browseButton = Button(self.top, text="Browse")
        self.browseButton.bind("<Button-1>", self.get_path)
        self.browseButton.grid(row=0, column=2, sticky=W, padx=4)

        # self.innerTop

        self.radioBtn1 = Radiobutton(self.top, text="Album Art", variable=self.boolVar, value=False)
        self.radioBtn1.grid(row=1, column=2, sticky=W, pady=2)

        self.radioBtn2 = Radiobutton(self.top, text="Song Art", variable=self.boolVar, value=True)
        self.radioBtn2.grid(row=1, column=3, sticky=W, pady=2)

        self.startButton = Button(self.top, text="Get Metadata")
        self.startButton.bind("<Button-1>", self.metadata)
        tk_root.bind("<Return>", self.metadata)
        self.startButton.grid(row=0, column=3, sticky=W, padx=4)

        # bottom left and right side
        attrWidth = 18
        valWidth = 62

        Label(self.bottom, text="Title", width=attrWidth, borderwidth=2, relief="groove").grid(row=0, column=0, pady=2)
        Label(self.bottom, textvariable=self.title, width=valWidth, background="grey", fg="white").grid(row=0, column=1, pady=2)

        Label(self.bottom, text="Artist", width=attrWidth, borderwidth=2, relief="groove").grid(row=1, column=0, pady=2)
        Label(self.bottom, textvariable=self.artist, width=valWidth, background="grey", fg="white").grid(row=1, column=1, pady=2)

        Label(self.bottom, text="Album", width=attrWidth, borderwidth=2, relief="groove").grid(row=2, column=0, pady=2)
        Label(self.bottom, textvariable=self.album, width=valWidth, background="grey", fg="white").grid(row=2, column=1, pady=2)

        Label(self.bottom, text="Album Artist", width=attrWidth, borderwidth=2, relief="groove").grid(row=3, column=0, pady=2)
        Label(self.bottom, textvariable=self.album_artist, width=valWidth, background="grey", fg="white").grid(row=3, column=1, pady=2)

        Label(self.bottom, text="Year", width=attrWidth, borderwidth=2, relief="groove").grid(row=4, column=0, pady=2)
        Label(self.bottom, textvariable=self.year, width=valWidth, background="grey", fg="white").grid(row=4, column=1, pady=2)

        self.top.pack(side=TOP, fill=BOTH)
        self.bottom.pack(side=BOTTOM, fill=BOTH)
        self.artFrame.pack(side=BOTTOM, fill=BOTH)
        self.frame.pack()

    def get_path(self, event=None):
        path = askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        self.fileStr.set(path)

    def metadata(self, event=None):
        def thread_func():
            os.system("cls")
            for song in getSongsList(self.file_path.get()):
                if self.boolVar.get():
                    print(f"Song Art: {self.boolVar.get()}")
                    mDict = get_metadata(song, 1)
                else:
                    print(f"Album art: {not self.boolVar.get()}")
                    mDict = get_metadata(song)

                if mDict is not None:
                    self.title.set(mDict['title'])
                    self.artist.set(mDict['artist'])
                    self.album.set(mDict['album'])
                    self.album_artist.set(mDict['album_artist'])
                    self.year.set(mDict['year'])

                    # album art
                    ext = mDict['img_extension']
                    temp_name = self.album.get() + " by " + self.artist.get()

                    if not os.path.isdir("Album Art"):
                        os.mkdir("Album Art")

                    open(f"Album Art/{temp_name + ext}", "wb").write(mDict['image_req'].content)

                    # clear old image
                    self.imgLabel.config(image='')

                    self.img = ImageTk.PhotoImage(Image.open(f"Album Art/{temp_name + ext}").resize((450, 450)))
                    self.imgLabel.config(image=self.img)
                    self.imgLabel.image = self.img
                    self.imgLabel.pack()

                    # os.remove(f"{temp_name + ext}")
                else:
                    messagebox.showinfo(
                        "Failed",
                        f"Couldn't find metadata for\n'{self.fileStr.get()}'"
                    )

        metadata_thread = threading.Thread(target=thread_func)
        metadata_thread.start()


def main():
    root = Tk()
    root.title('Music Metadata & Lyrics')
    root.resizable(width=False, height=False)

    MetadataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
