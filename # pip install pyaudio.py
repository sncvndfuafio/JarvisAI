import pyttsx3  # Text-to-speech engine
import speech_recognition as sr  # Speech recognition library
import datetime
import wikipedia  # For Wikipedia queries
import webbrowser
import os
import smtplib

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the first voice available


def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """Wish the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you?")


def take_command():
    """Take microphone input and recognize speech."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2  # Wait for a pause before ending input
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Recognize in English (India)
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Microphone input timed out.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None


def send_email(to, content):
    """Send an email using SMTP."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Replace with valid credentials
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email.")


if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()

        if query is None:
            continue

        # Logic for handling queries
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")
        
        elif 'open chat gpt' in query:
            webbrowser.open("https://chatgpt.com/c/674823ea-2168-8005-a4a1-53b0ebc2a614")
    

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'  # Update path
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No songs found in the directory.")
            else:
                speak("Music directory does not exist.")

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'open code' in query:
            code_path = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            if os.path.exists(code_path):
                os.startfile(code_path)
            else:
                speak("Visual Studio Code is not installed at the specified path.")

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = take_command()
                if content:
                    to = "harryyourEmail@gmail.com"  # Replace with recipient email
                    send_email(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I could not send the email.")
        
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, Sir. Have a great day!")
            break

        else:
            speak("I am not sure how to handle that query.")
