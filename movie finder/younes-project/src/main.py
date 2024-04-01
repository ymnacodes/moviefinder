from tkinter import filedialog, messagebox
from dotenv import load_dotenv
from tkinter.font import Font
from tkinter import ttk
from helpers import *
import tkinter as tk
import lyricsgenius
import webbrowser
import pygame
import os
import re

# Load the environment variables
load_dotenv()

# Initialize the Tkinter app
root = tk.Tk()
root.configure(bg='#282634')
root.geometry("500x500")
root.title("LyricFinder")

# Function to select the folder
def select_folder():
    folder_path = filedialog.askdirectory()

    if folder_path:
        while not any(filename.endswith(".mp3") for filename in os.listdir(folder_path)):
            messagebox.showinfo("No Songs", "No songs found in the selected folder.")
            folder_path = filedialog.askdirectory()
            if not folder_path:
                return
     
        # Create a progress bar to show that the app is still loading
        progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        progress.pack(expand=True)
        progress.start()

        # Use the after() method to run the fetch_songs() function in the background
        fetch_songs(folder_path, progress)
        # root.after(100, lambda: fetch_songs(folder_path, progress))

def update_progress(progress: ttk.Progressbar, value: int):
    progress.step(value)
    root.update_idletasks()
    

# Function to fetch the lyrics of the songs in the selected folder
def fetch_songs(folder_path, progress: ttk.Progressbar):
    genius = lyricsgenius.Genius(os.getenv("GENIUS_ACCESS_TOKEN"))
    songs_with_lyrics = []
    songs_without_lyrics = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            song_title = os.path.splitext(filename)[0].split(" - ")[-1]
            song_artist = "Unknown Artist"
            match = re.match(r"(.+) - (.+)\.mp3", filename)
            if match:
                song_artist = match.group(1)
            update_progress(progress, 100 / len(os.listdir(folder_path)))
            song = genius.search_song(song_title, song_artist)
            if song:
                songs_with_lyrics.append((song_artist, song_title, song))
            else:
                songs_without_lyrics.append((song_artist, song_title))
            
    # Stop the progress bar
    progress.stop()
    progress.destroy()

    # Save the lyrics to text files
    if not os.path.exists("lyrics"):
        os.mkdir("lyrics")
    else:
        for filename in os.listdir("lyrics"):
            os.remove(f"lyrics/{filename}")

    for song in songs_with_lyrics:
        filename = f"lyrics/{song[0]} - {song[1]}.txt"
        with open(filename,encoding="utf-8", mode="w") as f:
            # Use re to remove the square brackets and their contents and skip line 1
            lyrics = re.sub(r"\[.*\]", "", song[2].lyrics).split("\n")[1:]
            f.write("\n".join(lyrics))

    # Show a message box with the songs that were not found
    if songs_without_lyrics:
        songs_without_lyrics_str = '\n* '.join(map(lambda song: f"{song[0]} - {song[1]}", songs_without_lyrics))
        messagebox.showinfo("Lyrics Not Found", f"Lyrics were not found for the following songs:\n* {songs_without_lyrics_str}")

    if not songs_with_lyrics and songs_without_lyrics:
        messagebox.showinfo("No Lyrics", "There were no lyrics found for any of the songs in the selected folder.")
        select_folder()
        return
    
    # Open documents directory
    documents_directory = "lyrics"
    documents = []
    for file_name in os.listdir(documents_directory):
        with open(os.path.join(documents_directory, file_name),encoding="utf-8", mode="r") as file:
            documents.append(file.read())

    # Clean documents
    for i in range(len(documents)):
        documents[i] = data_clean(documents[i])

    # Unify words in documents
    union_set = set()
    for document in documents:
        union_set.update(document)

    # Convert set to list
    terms = list(union_set)

    # Calculate Number of appearances of each term in each document
    documents_terms = []
    for i in range(len(documents)):
        dictionary = dict.fromkeys(terms, 0)
        for j in documents[i]:
            dictionary[j] += 1
        documents_terms.append(dictionary)

    # Calculate TF
    tf_list = []
    for i in range(len(documents)):
        tf_list.append(calcul_TF(documents_terms[i], documents[i]))

    # Calculate IDF
    idf = calcul_IDF(*documents_terms)

    # Calculate TFIDF
    tfidf_list = []
    for i in range(len(documents)):
        tfidf_list.append(calcul_TFIDF(tf_list[i], idf))
    
    # clear the content of the first page
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame for the search functionality with the background color set to #282634
    frame = tk.Frame(root, bg='#282634')
    frame.pack(expand=True)

    # Add the logo to the frame
    global logo_img
    logo_label = tk.Label(frame, image=logo_img, bg='#282634')
    logo_label.pack(side="top")

    # Add the text field for the search term
    search_var = tk.StringVar()
    search_entry = tk.Entry(frame, textvariable=search_var, background='#DCDCDC', foreground='#ff4057', font=Font(size=12, weight="bold"))
    search_entry.pack(side="top")

    # Add the search button
    def search():
        # Delete all previous widgets except the search bar
        for widget in frame.winfo_children():
            if widget != search_entry and widget != search_button:
                widget.destroy()

        query = search_var.get().lower()
        query = data_clean(query)

        # Represent query as vector
        query_vector = []
        for term in terms:
            if term in query:
                query_vector.append(1)
            else:
                query_vector.append(0)

        # Represent documents as vectors
        documents_vectors = []
        for i in range(len(documents)):
            documents_vectors.append(list(tfidf_list[i].values()))

        # Calculate correspondance between query and documents
        correspondance = []
        for i in range(len(documents)):
            correspondance.append(calcul_correspondance(documents_vectors[i], query_vector))
        results = sorted(range(len(correspondance)), key=lambda i: correspondance[i], reverse=True)[:10]
        results = list(filter(lambda i: correspondance[i] != 0, results))
        results = list(map(lambda i: (i, os.listdir(documents_directory)[i]), results))

        if results:
            # Destroy the logo from the frame
            logo_label.destroy()
            # Create a listbox to show the search results
            results_frame = tk.Frame(frame)
            results_frame.pack(side="top", fill="both", expand=True)
            scrollbar = tk.Scrollbar(results_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")
            listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set, background='#DCDCDC', foreground='#ff4057', font=Font(size=12, weight="bold"), selectbackground='#ff4057', selectforeground='#DCDCDC', width=50, height=10)
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=listbox.yview)

            # Add the filenames of the mp3 music files to the listbox
            for result in results:
                listbox.insert("end", result[1].replace(".txt", ".mp3"))
                
            # If the user double clicks on a song, show correspondance
            def on_double_click(event):
                selection = listbox.curselection()
                if selection:
                    messagebox.showinfo("Correspondance", format(correspondance[results[selection[0]][0]], '.4f'))
                    
            listbox.bind("<Double-Button-1>", on_double_click)

            # Add a button to play the selected song
            def play():
                global player
                selection = listbox.curselection()
                if selection:
                    filename = listbox.get(selection)
                    pygame.mixer.music.load(f"{folder_path}/{filename}")
                    pygame.mixer.music.play(loops=0)
            play_button = tk.Button(frame, text="Play", command=play, bg='#ff4057', fg='#DCDCDC', font=Font(size=12, weight="bold"), highlightthickness=0, activebackground='#DCDCDC', activeforeground='#ff4057')
            play_button.pack(side="top")

            # Add a button to open the selected song's lyrics in the browser
            def open_lyrics():
                selection = listbox.curselection()
                if selection:
                    filename = listbox.get(selection)
                    webbrowser.open(f"file://{os.getcwd()}/lyrics/{filename.replace('.mp3', '.txt')}")
            
            open_button = tk.Button(frame, text="Open Lyrics", command=open_lyrics, bg='#ff4057', fg='#DCDCDC', font=Font(size=12, weight="bold"), highlightthickness=0, activebackground='#DCDCDC', activeforeground='#ff4057')
            open_button.pack(side="top")
        else:
            messagebox.showinfo("No Results", "No results found.")
    search_button = tk.Button(frame, text="Search", command=search, bg='#ff4057', fg='#DCDCDC', font=Font(size=12, weight="bold"), highlightthickness=0, activebackground='#DCDCDC', activeforeground='#ff4057')
    search_button.pack(side="top")

pygame.mixer.init()

# Add the logo to the top middle of the frame
logo_img = tk.PhotoImage(file="assets/images/lyrifinder-logo.png")
logo_label = tk.Label(root, image=logo_img, bg='#282634')
logo_label.pack(side="top")

# Add the browse button and the field to select the folder on the first page
browse_button = tk.Button(root, text="Browse", command=select_folder, bg='#ff4057', fg='#DCDCDC', font=Font(size=12, weight="bold"), highlightthickness=0, activebackground='#DCDCDC', activeforeground='#ff4057')
browse_button.pack(side="top")
folder_label = tk.Label(root, text="Select a folder containing your music files", bg='#282634', fg='#ff4057', font=Font(size=12, weight="bold"))
folder_label.pack(side="top")

# Run the Tkinter app
root.mainloop()

