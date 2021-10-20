from tkinter import *
from PIL import ImageTk, Image
from MetadataGUI import MetadataGUI
from GeniusLyricsGUI import GeniusLyricsGUI


# Globals
root = Tk()
root.title('Music Metadata & Lyrics')
# icon = ImageTk.PhotoImage(Image.open("images/img1.ico"))
# root.iconphoto(True, icon)
root.resizable(width=False, height=False)
welcomeFrame = Frame(root)


def lyrics_btn(event=None):
    welcomeFrame.destroy()
    GeniusLyricsGUI(root)


def metadata_btn(event=None):
    welcomeFrame.destroy()
    MetadataGUI(root)


def main():
    Label(welcomeFrame, text="Music Metadata & Lyrics", font="Calibri 16").pack(side=TOP, fill=BOTH)
    Label(welcomeFrame, text="Powered by Genius.com", font="Calibri 10 italic").pack(side=TOP, fill=BOTH, pady=5)

    img = ImageTk.PhotoImage(Image.open("images/img1.ico"))
    imgLabel = Label(welcomeFrame, image=img)
    imgLabel.image = img
    imgLabel.pack(side=TOP, pady=10)

    lyrics_button = Button(welcomeFrame, text="Search Lyrics", font="Calibri 12", bd=2, padx=7, pady=7, relief="groove")
    lyrics_button.bind("<Button-1>", lyrics_btn)
    lyrics_button.pack(side=TOP, padx=1, pady=1, fill=BOTH)

    metadata_button = Button(welcomeFrame, text="Search Metadata", font="Calibri 12", bd=2, padx=7, pady=7,
                             relief="groove")
    metadata_button.bind("<Button-1>", metadata_btn)
    metadata_button.pack(side=TOP, padx=1, pady=1, fill=BOTH)

    welcomeFrame.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
