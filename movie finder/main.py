import tkinter as tk
from PIL import ImageTk, Image
from tokenizer import *
from api import Trailer
import webbrowser

# Function to switch between frames
def switch_frame(frame_to_hide, frame_to_show):
    frame_to_hide.grid_forget()
    frame_to_show.grid()

# Function to fetch movies using the movie quote
def fetch_movies():
    # Get the movie quote from the input field
    quote = qentry.get()
    best_matches = querytomovies(cleaned_corpus,quote)

     # Clear previous listings (excluding the button)
    for widget in listings_frame.winfo_children():
        if widget != BackButton and isinstance(widget, tk.Label):  # Only clear Label widgets (optional)
            widget.destroy()

    top5=tk.Label(listings_frame,text="Top 5 Results:",font="Poppins",bg="#D4C5C5")
    top5.grid(row=0,column=2)
    # Display movie listings
    for i, movie_title in enumerate(best_matches[:5], start=1):
        MovieTitle = tk.Label(listings_frame, text=f"{i}. {movie_title}",cursor="hand2",bg= "#D4C5C5",pady=20,font="Poppins")
        MovieTitle.grid(row=6 + i, column=2)
        Trailer_Url= fetch_trailer(movie_title)
        MovieTitle.bind("<Button-1>", lambda event, id="": open_Trailer(f"{Trailer_Url}"))

    # Switch to listings frame when clicked
    switch_frame(search_frame, listings_frame)


# Function to fetch movie details from youtube data API
def fetch_trailer(movie_title):
    trailer = Trailer(movie_title)
    id= trailer.getVidId()
    url=f"https://www.youtube.com/watch?v={id}"
    return url


def open_Trailer(video_url):
    webbrowser.open(video_url)


# Main window
root = tk.Tk()
root.title("FilmHunt")
root.geometry("405x500")
root.configure(bg="#D4C5C5")

# Search Frame
search_frame = tk.Frame(root,bg="#D4C5C5")
search_frame.grid(row=0, column=0, sticky="nsew")

something=tk.Label(search_frame,text="           ", bg="#D4C5C5")
something.grid(row=0,column=0)
# Title
title1 = tk.Label(search_frame, text="WELCOME TO", font=("Poppins", 20),bg="#D4C5C5")
imgpre= Image.open('movie finder\images\logo.png').resize((30,50))
img = ImageTk.PhotoImage(imgpre)
img_label= tk.Label(search_frame, image=img,bg="#D4C5C5")
title2 = tk.Label(search_frame, text="Film Hunt", font=("Poppins", 50), bg="#D4C5C5")
title1.grid(row=1, column=1)
img_label.grid(row=3, column=1)
title2.grid(row=2, column=1)
# Search Part
qentry = tk.Entry(search_frame, width=30, font=('Poppins', 10))
qentry.insert(0, "Enter What You Remember")
qentry.grid(row=4, column=1, padx=10, pady=10)

# Button to fetch movies
SearchButton = tk.Button(search_frame, text="Find Film",font="Poppins",  fg="#FFFFFF", bg="#343434", padx=50, command=lambda: fetch_movies())
SearchButton.grid(row=5, column=1,padx=10, pady=10)

# Movie Listings Frame
listings_frame = tk.Frame(root, bg="#D4C5C5")

# Button to go back to search frame

BackButton = tk.Button(listings_frame, text="Back to Search",font="Poppins", fg="#FFFFFF", bg="#343434", padx=50, command=lambda: switch_frame(listings_frame, search_frame))
BackButton.grid(row=20, column=2)

# Run the Tkinter app
root.mainloop()

