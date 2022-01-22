import speech_recognition as sr
import pyttsx3
import pywhatkit
import pandas as pd
import wikipedia

'''
Here google survey form is used to get the required data as a csv file
Another method for inserting yourown data will be available later
Or you can alter the data using pandas
'''
df = pd.read_csv(r'LOCATION OF THE CSV FILE')   #the csv file is available in the repo

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    print('now speaking...')
    engine.say(text)
    print(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5) #adjusting the microphone as necessary
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command.lower()
            print(command)        
    except sr.UnknownValueError:
        print('Unknown error occured')
    except:
        print("Try again!")
    
    return command

def get_data():
    request = input('Enter the name : ')
    filt = df['Name'].str.contains(request, na=False)
    data = df.loc[filt]
    return data


def run_bot():
    command = take_command()
    bot_data = get_data()

    if any(command == i for i in ask_name):
        talk('Hi, my name is ' + bot_data['Name'].item())
        
    elif any(i in command for i in wellness):
        talk(bot_data["How you doin' ?"].item())
       
    elif any(i in command for i in ask_song):
        talk('My favourite song is ' + bot_data['Favourite Song'].item() + ', would you like me to play it?')
        command = take_command()
        if (('yes' or 'play') in command or any(command == i for i in ask_song)):
            talk('Playing ' + bot_data['Favourite Song'].item() + ' on YouTube')
            pywhatkit.playonyt(bot_data['Favourite Song'])
        else:
            talk('As you wish!')
    
    elif any(i in command for i in ask_username):
        talk('My username is ' + bot_data['Alias/username'].item())

    elif any(i in command for i in ask_gender):
        if bot_data['Gender'].item() == 'M':
            talk('I am a ' + bot_data['Gender'].item())
        else:
            talk('Bots do not have a gender.')

    elif any(i in command for i in ask_age):
        talk('I am ' + str(bot_data['Age'].item()))
    
    elif any(i in command for i in ask_city):
        talk('I currently live in ' + bot_data['Current Residence(City)'].item())
    
    elif any(i in command for i in ask_hobby):
        talk('I like ' + bot_data['Hobbies (use commas for separation)'].item())

    elif any(i in command for i in about_self):
        talk(bot_data['Tell something about yourself.'].item())

    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    
    elif 'time' in command:
        time = datetime.datetime.now.strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif ('who is' or 'what is') in command:
        person = command.replace('who is','')
        info = wikipedia.summary(person, 1)
        talk(info)
    
    else:
        print('Err...')


ask_name = ('what is your name', "what's your name", 'who are you', 'can you tell me your name', 'what do people call you')
wellness = ('how you doing', 'how are you', "how you doin'", 'how are you doing')
ask_song = ('what is your favourite song', "what's your favourite song", 'play your favourite song', 'play me your favourite song', 'which song do you like the most')
ask_username = ('what is your username', "what's your username", 'your username')
ask_gender = ('what is your gender', "what's your gender", 'are you a male or a female')
ask_age = ('what is your age', 'how old are you', "what's your age")
ask_city = ('where do you live', 'where are you from' , 'where are you currently')
ask_hobby = ('what are your hobbies', 'what do you like', 'what is your hobby')
about_self = ('tell something about yourself', 'tell me something about yourself', 'about yourself')

while True:
    run_bot()




