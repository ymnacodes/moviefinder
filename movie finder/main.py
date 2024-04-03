import tkinter as tk
from PIL import ImageTk, Image
from tokenizer import *
#from api import Trailer
import webbrowser

# Function to switch between frames
def switch_frame(frame_to_hide, frame_to_show):
    frame_to_hide.grid_forget()
    frame_to_show.grid()

# Function to fetch movies using the movie quote
def fetch_movies():
    # Get the movie quote from the input field
    quote = qentry.get()
    best_matches = querytomovies(quote)

     # Clear previous listings (excluding the button)
    for widget in listings_frame.winfo_children():
        if widget != BackButton and isinstance(widget, tk.Label):  # Only clear Label widgets (optional)
            widget.destroy()

    # Display movie listings
    for i, movie_title in enumerate(best_matches[:5], start=1):
        MovieTitle = tk.Label(listings_frame, text=f"{i}. {movie_title}")
        MovieTitle.grid(row=5 + i, column=1)

    # Switch to listings frame when clicked
    switch_frame(search_frame, listings_frame)


# Function to fetch movie details from youtube data API
def fetch_trailer(movie_title):
    # Placeholder function
    #url=r"https://www.youtube.com/watch?v=9SDfIMZc6ag"
    #return url
    pass

# Function to display movie trailer
def display_movie_details(movie_info):
    # Placeholder function
    pass

# Main window
root = tk.Tk()
root.title("FilmHunt")
root.geometry("1000x1000")

# Search Frame
search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, sticky="nsew")

# Title
title1 = tk.Label(search_frame, text="WELCOME TO", font=("Poppins", 28))
imgpre= Image.open('moviefinder\movie finder\images\logo.png').resize((30,50))
img = ImageTk.PhotoImage(imgpre)
img_label= tk.Label(search_frame, image=img)
title2 = tk.Label(search_frame, text="Film Hunt", font=("Times", 28))
title1.grid(row=0, column=0, columnspan=2)
img_label.grid(row=1, column=0, columnspan=2)
title2.grid(row=2, column=0, columnspan=2)

# Search Part
qentry = tk.Entry(search_frame, width=80, font=('Poppins', 20))
qentry.insert(0, "Enter What You Remember")
qentry.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Button to fetch movies
SearchButton = tk.Button(search_frame, text="Find Film", fg="#FFFFFF", bg="#343434", padx=50, command=lambda: fetch_movies())
SearchButton.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Movie Listings Frame
listings_frame = tk.Frame(root)

# Button to go back to search frame
BackButton = tk.Button(listings_frame, text="Back to Search", command=lambda: switch_frame(listings_frame, search_frame))
BackButton.grid(row=20, column=2)

# Run the Tkinter app
root.mainloop()

