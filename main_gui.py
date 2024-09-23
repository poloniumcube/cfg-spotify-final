import pandas as pd
import random
import spotipy_client as spc
import customtkinter as ctk
from tkinter import *
import tkinter

# simplified code (compared to the main.py) :D, a bit buggy but does the job!

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()

app.geometry = ("800x400")
app.grid_columnconfigure((0, 1), weight=1)

while True:
    df = pd.read_csv('ClassicHit.csv')        

    # QUESTION 1 - MOOD
    question_1 = ctk.CTkInputDialog(text='''
    Hi, user! Welcome to the Song Selector - you'll get a tailored song recommendation after answering a few simple questions!
    Your answer options are indicated by [1] or [2] in the question - please make sure to type exactly what you see.
    Example: "Do you want a song to be [1]shorter or [2]longer?: "
    If you want a longer song, you would type 'longer' (without the captions) in the terminal.\n
    Have fun!\n\n           
    Now, what\'s your mood? Do you want the song to be [1]happy or rather [2]sad?''', 
    font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')

    answer_1 = question_1.get_input()

    if answer_1.lower() == 'happy':
        question_2 = ctk.CTkInputDialog(text='''\nSomeone\'s in a good mood :D Okay, next question:\n
Do you want a [1]longer or a [2]shorter one?''', font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')
        df = df[df['Mode'] == 1]  
    elif answer_1.lower() == 'sad':
        question_2 = ctk.CTkInputDialog(text='''\nA bad day? :( It\'s okay, let\'s go to the next question:\n
Do you want a [1]longer or a [2]shorter one?''', font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')
        df = df[df['Mode'] == 0]      

    # QUESTION 2 - DURATION    
    answer_2 = question_2.get_input()

    if answer_2.lower() == 'longer':
        df = df[df['Duration'] >= 175000]
    elif answer_2.lower() == 'shorter':
        df = df[df['Duration'] < 175000]  
    
    # QUESTION 3 - GENRE
    count_songs_per_genre = df.groupby('Genre').size().to_string()
    question_3 = ctk.CTkInputDialog(text=f'''
\nGotcha! I\'ll select a good one for you :D\n
Okay, now which genre do you prefer? Here's how many songs is left per genre:\n
{count_songs_per_genre}\n
What do you choose? ''', font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')

    answer_3 = question_3.get_input()
    
    df = df[df['Genre'].str.strip().str.lower() == answer_3.strip().lower()]
    
    # QUESTION 4 - CENTURY
    count_songs_19_century = df[df['Year'] == 1899].shape[0]
    count_songs_20_century = df[(df['Year'] > 1900) & (df['Year'] < 2000)].shape[0]
    count_songs_21_century = df[df['Year'] >= 2000].shape[0]

    question_4 = ctk.CTkInputDialog(text=f'''\nOooh {answer_3.lower()} is my favourite genre as well! Aaand onto the last question!\n
We have lots of songs here, old and new - which century would you want to choose? 
P.S. If you want a random song, type 0
P.P.S. Here's how many songs are left per century:
19th: {count_songs_19_century}
20th: {count_songs_20_century}
21st: {count_songs_21_century}\n
What do you choose? ''', font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')
    
    answer_4 = question_4.get_input()

    if answer_4 == '19':
        df = df[df['Year'] == 1899]
    elif answer_4 == '20':
        df = df[(df['Year'] > 1900) & (df['Year'] < 2000)]
    elif answer_4 == '21':
        df = df[df['Year'] >= 2000]
    elif answer_4 == '0':
        df = df[df['Year'] == random.randint(1889, 2024)]

    # API CALL
    filtered_result = df.sample() # random song selection
    track = filtered_result['Track'].values[0] 
    artist = filtered_result['Artist'].values[0]
    year = filtered_result['Year'].values[0]
                
    question_5 = ctk.CTkInputDialog(text=f'''\nThanks for the answers! Based on your choices, here\'s a random song to your liking: 
It's '{track}' by {artist}, recorded in {year}\n
Do you want to listen to the song you got? (yes/no)''', font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')
    answer_5 = question_5.get_input()
    if answer_5 == 'no':
        print('\nOkie, see ya!\n')
        break
    elif answer_5 == 'yes':
        spc.search_track(spc.token, track, artist)
        try_again =  ctk.CTkInputDialog(text="\nWanna try again? (yes/no) ", font=("Arial", 12),button_fg_color='#1a1a1a',button_text_color='#1a1a1a')
        try_again_answer = try_again.get_input()
        if try_again_answer == 'yes':
            continue
        else:            
            break


    app.mainloop()

  
    



