import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog as fd
import speech_recognition as sr
import moviepy.editor as mp
import cv2
import pytesseract

root = tk.Tk()
root.geometry("700x500")
root.resizable(0,0)
root.title("Convert Video Audio to Text")

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

global filename
filename = ""


def outins(instxt):
    output.config(state=tk.NORMAL)
    output.delete(1.0 , tk.END)
    output.insert(tk.INSERT,instxt)
    output.config(state=tk.DISABLED)

def upload_button():
    global filename
    filetypes=(
        ("mp4","*.mp4"),
        ("mpeg","*.mpeg"),
        ("ogv","*.ogv"),
        ("avi","*.avi"),
        ("mov","*.mov")
    )
    filename = fd.askopenfilename(title="Open",filetypes=filetypes)

def audio_to_text():
    global filename
    if filename != "":
        outins("Recognizing the audio. Please wait...")
        vidfile = mp.VideoFileClip(filename)
        vidfile.audio.write_audiofile("audio.wav",verbose=False,logger=None)
        r = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio = r.record(source) 
        try:
            out = r.recognize_google(audio)
            outins(out)
        except Exception as e:
            outins("Error:\n"+str(e))

def video_to_text():
    global filename
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = 0
    out = []
    fin = []
    outins("Recognizing the video. Please wait...")
    ret = True
    while ret:
        frames += 1
        ret,frame = cap.read()
        if frames%fps == 0:
            try:
                out.append(pytesseract.image_to_string(frame)+"\n")
                if len(out) == 10:
                    fin.append("".join(out))
                    out = []
            except:
                pass
    if len(out)>0:
        fin.append(out)
    line = "___________________________________________________________\n"
    finish = ""
    prev = 1
    for i in fin:
        time = str(prev//60)+":"+str(prev%60) + " - " + str((prev+9)//60)+":"+str((prev+9)%60)
        time = time.center(59," ")
        prev += 10
        if type(i)==list:
            i="\n".join(i)
        finish += line+ "\n" + time + "\n" + line+ "\n" + i
    outins(finish)
    

lframe = tk.Frame(root,height=500,width=200,background="#222e27")
lframe.pack(side=tk.LEFT)

rframe = tk.Frame(root,background="#195856")
rframe.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

txt="""
Convert
Video
Audio
to
Text
"""
Title = tk.Text(lframe,width=15,height=10,background="#222e27",highlightthickness=0,borderwidth=0,foreground="#d1d1d1")
Title.insert(tk.INSERT, txt)
Title.config(font=("Times New Roman",17,"bold"),state=tk.DISABLED)
Title.place(x=60,y=50)

output = st.ScrolledText(rframe,background="#195856",wrap=tk.WORD,state=tk.DISABLED,foreground="#d1d1d1")
output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

Upload = tk.Button(lframe,width=8,text="Upload",command=upload_button)
Upload.place(x=60,y=310)

audbutton = tk.Button(lframe,width=8,text="Audio",command=audio_to_text)
audbutton.place(x=60,y=360)

vidbutton = tk.Button(lframe,width=8,text="Video",command=video_to_text)
vidbutton.place(x=60,y=410)

root.mainloop()
