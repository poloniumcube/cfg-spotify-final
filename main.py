import pandas as pd
import random
import spotipy_client as spc

## working code w/o the customtkinter gui

def songselection ():
    
    print('''
        Hi, user! Welcome to the Song Selector - you'll get a tailored song recommendation after answering a few simple questions!
        Your answer options are indicated by [1] or [2] in the question - please make sure to type exactly what you see.
        Example: "Do you want a song to be [1]shorter or [2]longer?: "
        If you want a longer song, you would type 'longer' (without the captions) in the terminal.\n
        Have fun!
        ''')

    while True: # loop to restart the process if the user wants to try again
        
        df = pd.read_csv('ClassicHit.csv')        
        
        # some cleaning for the sake of adhering to best practices (the dataset is expected to be clean but you never know)
        df.drop_duplicates(inplace=True)
        df = df[df['Mode'].isin([0,1])] 
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df.dropna(subset=['Track', 'Artist', 'Year'],inplace=True) 

        user_check = input('Do you want to proceed? (yes/no) ').strip().lower()        
        if user_check == 'no':
            print('\nOkay, bye :(\n')
            break
        elif user_check == 'yes':
            print('\nOkay, let\'s go!\n')
            
            # filter the dataset based on the user's input (mood, duration, genre, century) 
            user_mode = input('Now, what\'s your mood? Do you want the song to be [1]happy or rather [2]sad? ').strip().lower()
            if user_mode == 'happy':
                print('\nSomeone\'s in a good mood :D Okay, next question:\n')
                df = df[df['Mode'] == 1]  
            elif user_mode == 'sad':
                print('\nA bad day? :( It\'s okay, let\'s go to the next question:\n')
                df = df[df['Mode'] == 0]      
            
            user_duration = input('Do you want a [1]longer or a [2]shorter one? ').strip()
            print('\nGotcha! I\'ll select a good one for you :D\n')
            if user_duration == 'longer':
                df = df[df['Duration'] >= 175000]
            elif user_duration == 'shorter':
                df = df[df['Duration'] < 175000]
            
            count_songs_per_genre = df.groupby('Genre').size().to_string()
            user_genre = input(f'''Okay, now which genre do you prefer? Here's how many songs is left per genre:\n
{count_songs_per_genre}\n
What do you choose? ''').strip().lower()
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
What do you choose? ''').strip()
            
            if user_century == '19':
                df = df[df['Year'] == 1899]
            elif user_century == '20':
                df = df[(df['Year'] > 1900) & (df['Year'] < 2000)]
            elif user_century == '21':
                df = df[df['Year'] >= 2000]
            elif user_century == '0':
                df = df[df['Year'] == random.randint(1889, 2024)]
    
            if df.empty: # if a random century selection landed you on a century with no songs for the previous filters
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
                    except IndexError: # the only try-except because this error was particularly annoying
                        print("Couldn't find a match :( Retrying...")
                        
            spotify_check = input('Do you want to listen to the song you got? (yes/no) ').strip().lower()
            if spotify_check == 'no':
                print('\nOkie, see ya!\n')
                break
            elif spotify_check == 'yes':
                spc.search_track(spc.token, track, artist)
                continue

songselection()