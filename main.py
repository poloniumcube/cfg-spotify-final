import pandas as pd
import random
import spotipy_client as spc
# import customtkinter

# app = customtkinter.CTk()
# app.mainloop()

def songselection ():
    
    print('''
        Hi, user! Welcome to the Song Selector - you'll get a tailored song recommendation after answering a few simple questions!
        You'll see the example of an input in the curly braces () after every question - please make sure to type exactly what you see.
        Example: "Do you want a song to be shorter (s) or longer (l)? (s/l): "
        In this case, you would be expected to type 's' (without the captions) in the terminal.\n
        Have fun!
        ''')

    while True: # loop to restart the process if the user wants to try again
        df = pd.read_csv('ClassicHit.csv')        
        user_check = input('Do you want to proceed? (y/n) ').lower()
        
        if user_check == 'n':
            print('\nOkay, bye :(\n')
            break
        elif user_check == 'y':
            print('\nOkay, let\'s go!\n')
            
            # filter the dataset based on the user's input (mood, duration, genre, century)
            user_mode = input('Now, what\'s your mood? Do you want the song to be happy (h) or rather sad (s)? (h/s) ').lower()
            if user_mode == 'h':
                print('\nSomeone\'s in a good mood :D Okay, next question:\n')
                df = df[df['Mode'] == 1]  
            elif user_mode == 's':
                print('\nA bad day? :( It\'s okay, let\'s go to the next question:\n')
                df = df[df['Mode'] == 0]      
            
            user_duration = input('Do you want a longer (l) or a shorter (s) one? (l/s) ').lower()
            print('\nGotcha! I\'ll select a good one for you :D\n')
            if user_duration == 'l':
                df = df[df['Duration'] >= 175000]
            elif user_duration == 's':
                df = df[df['Duration'] < 175000]
            
            count_songs_per_genre = df.groupby('Genre').size().to_string()
            user_genre = input(f'''Okay, now which genre do you prefer? Here's how many songs is left per genre:\n
{count_songs_per_genre}\n
What do you choose? ''')
            print(f'\nOooh {user_genre.lower()} is my favourite genre as well! Aaand onto the last question!\n')
            
            df = df[df['Genre'].str.strip().str.lower() == user_genre.strip().lower()]
            count_songs_19_century = df[df['Year'] == 1899].shape[0]
            count_songs_20_century = df[(df['Year'] > 1900) & (df['Year'] < 2000)].shape[0]
            count_songs_21_century = df[df['Year'] >= 2000].shape[0]

            # Prompt user with counts
            user_century = input(f'''We have lots of songs here, old and new - which century would you want to choose? 
P.S. If you want a random song, type 0
P.P.S. Here's how many songs are left per century:
19th: {count_songs_19_century}
20th: {count_songs_20_century}
21st: {count_songs_21_century}\n
What do you choose? ''')
            
            # df filter based on the user input
            if user_century == '19':
                df = df[df['Year'] == 1899]
            elif user_century == '20':
                df = df[(df['Year'] > 1900) & (df['Year'] < 2000)]
            elif user_century == '21':
                df = df[df['Year'] >= 2000]
            elif user_century == '0':
                df = df[df['Year'] == random.randint(1889, 2024)]
    
            if df.empty: # if a random selection landed you on a century with no songs for the previous filters
                print('\nOops! No songs matched your criteria. Let\'s try again with different answers.\n')
                continue  
            else:
                while True: 
                    try:
                        filtered_result = df.sample() # random song selection
                        track = filtered_result['Track'].values[0] 
                        artist = filtered_result['Artist'].values[0]
                        year = filtered_result['Year'].values[0]
                        print(f'''\nThanks for the answers! Based on your choices, here\'s a random song to your liking: 
It's '{track}' by {artist}, recorded in {year}\n''')
                        break
                    except IndexError:
                        print("Couldn't find a match :( Retrying...")
            spotify_check = input('Do you want to listen to the song you got? (y/n) ').lower()
            if spotify_check == 'n':
                print('\nOkie, see ya!\n')
                break
            elif spotify_check == 'y':
                spc.search_track(spc.token, track, artist)
                try_again = input('\nWanna try again? (y/n) ').lower()
                if try_again == 'y':
                    continue
                else:            
                    break


songselection()

# next steps -->
    # 1. [m] import customtkinter to create a GUI for the user input --> issues with the installation, debug later
        # 1.1 [a] add a button to the GUI to play the song on Spotify
    # https://github.com/TomSchimansky/CustomTkinter
    # https://customtkinter.tomschimansky.com/

    # 2. [a] store the user's answers in a dictionary and use it to filter the dataset (more efficient [?])
