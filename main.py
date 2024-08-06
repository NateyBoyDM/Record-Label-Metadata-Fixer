import streamlit as st
import music_tag
import sys
import os
import PIL

types = [".mp3", ".aac", ".ogg", ".flac", ".m4a", ".wav", ".aiff", ".aif"]
data = [None] * 4
prevData = [None] * 3

def display(path, type):
    i = 0
    while i < 1:
        for subdir, dirs, files in os.walk(path):
            for track in files:
                if track.endswith(type.rstrip()):
                    if not track.startswith("._"):
                        file = (subdir + "/" + track)
                        f = music_tag.load_file(file)
                        art = f['artwork']
                        data[0] = (art.first.thumbnail([2048, 2048]))
                        data[1] = (str(f['album artist']))
                        data[2] = (str(f['album']))
                        data[3] = (str(f['title']))
                        if label in track:
                            track = track.split(" - ", 1)[1] 
                        print(track)
                        prevData[0] = track.split(" - ", 1)[0]
                        previewAlbum = track.split(prevData[0] + " - ", 1)[1]
                        prevData[1] = previewAlbum.split(" - ", 1)[0]
                        prevData[2] = (str(f['title']))
                        i += 1


def run(path, label, type, rename):
    for subdir, dirs, files in os.walk(path):
        if not os.path.exists(path + "/finished/"):
            os.makedirs(path + "/finished/")
        for track in files:
            if track.endswith(type.rstrip()):
                if not track.startswith("._"):
                    file = (subdir + "/" + track)
                    f = music_tag.load_file(file)
                    tag = f['album artist']
                    if label in track:
                        origTrack = track
                        track = track.split(" - ", 1)[1] 
                    if label in str(tag):
                        artist = track.split(" - ", 1)[0]
                        album = track.split(artist + " - ", 1)[1]
                        album = album.split(" - ", 1)[0]
                        f['album artist'] = artist
                        f['artist'] = artist
                        f['album'] = album
                        f.save()
                        print('tag changed from ' + str(tag) + ' to ' + str(artist))
                    if rename:
                        print(subdir + "/" + track)
                        os.rename(subdir + "/" + label  + " - " + track, path + "/finished/" + track)
                    else:
                        os.rename(subdir + "/" + origTrack, path + "finished/" + origTrack)
                else:
                    pass

def prevUpdate():
    st.image(data[0])
    st.subheader("Previous")
    st.text("Artist: " + data[1])
    st.text("Album: " + data[2])
    st.text("Track: " + data[3])

def newUpdate():
    st.subheader("New")
    st.text("Artist: " + prevData[0])
    st.text("Album: " + prevData[1])
    st.text("Track: " + prevData[2])

st.title("Record Label Metadata Fixer")
col1, col2 = st.columns(2)

# label 
with col1:
    st.header("Input")
    st.subheader("Label")
    label = st.text_input("Please enter the name of the record label displayed in the metadata and press enter: ")
    type = st.selectbox("File Type", types)
    st.subheader("Files")
    path = st.text_input("Please enter the path of the folder in which your audio files are contained and press enter: ")
    if path:
        display(path, type)
    rename = st.toggle("Would you like to also rename the file to exclude the record label?")
    if st.button("Run"):
        run(path, label, type, rename)
with col2:
    st.header("Output")
    st.subheader("Preview")
    if st.button("Update"):
        prevUpdate()
        newUpdate()
