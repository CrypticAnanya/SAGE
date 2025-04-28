using_terminator = False
import datetime
import time
import pytz
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import openai
import threading
import pyaudio
import smtplib
import subprocess
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import platform
import glob
from urllib.parse import quote
import pyautogui
searching = True
listening_for_interrupt = False
stop_speaking = False
expecting_code = False
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
preferred_voice_index = 1
if len(voices) > preferred_voice_index:
    engine.setProperty('voice', voices[preferred_voice_index].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def say(text):
    print("Sage\n", text)
    engine.say(text)
    engine.runAndWait()

def send_email(subject, body, to_email):
    from_email = "gppg317@gmail.com"
    password = "AGboy@@2001"

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        say("Email has been sent successfully.")
        print("Email sent!")
    except Exception as e:
        say("Sorry, I was not able to send the email.")
        print("Email sending error:", e)

def ai(prompt):
    try:
        openai.api_key = "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"
        openai.api_base = "https://api.groq.com/openai/v1"
        model_name = "llama3-8b-8192"

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response['choices'][0]['message']['content']
        print("AI Response:", reply)
        return reply

    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I encountered an error processing your request."


def chat(prompt):
    global searching
    if not searching:
        return "Searching is currently paused. Say 'start searching' to resume."
    try:
        openai.api_key = "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"
        openai.api_base = "https://api.groq.com/openai/v1"
        model_name = "llama3-8b-8192"

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response['choices'][0]['message']['content']
        print("Chat Response:", reply)
        say(reply)
        return reply

    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        say(error_msg)
        print(f"Chat Error: {e}")
        return error_msg

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            print("Listening for your command...")
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.RequestError:
            error_msg = "Error: Unable to connect to the speech recognition service."
            print(error_msg)
            say(error_msg)
            return error_msg
        except sr.UnknownValueError:
            error_msg = "Sorry, I couldn't understand what you said."
            print(error_msg)
            say(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            print(error_msg)
            say("An error occurred while listening. Please try again.")
            return error_msg
import subprocess

def open_app(command):
    app_mapping = {
        "excel": "excel",
        "powerpoint": "powerpnt",
        "word": "winword",
        "notepad": "notepad",
        "settings": "ms-settings:",
        "calculator": "calc",
        "paint": "mspaint",
        "chrome": "chrome",
        "command prompt": "cmd",
        "vscode": "code"
    }

    command = command.lower()

    for app, app_name in app_mapping.items():
        if app in command:
            try:
                print(f"Attempting to open {app_name}...")
                subprocess.run([app_name], check=True)
                print(f"{app_name} launched successfully.")
                say(f"Opening {app.capitalize()}.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error opening {app_name}: {e}")
                say(f"Could not open {app.capitalize()}.")
                return False

    say("Sorry, I don't recognize that app.")
    return False


def get_current_time():
    india = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(india)
    return now.strftime("%I:%M %p")

def get_current_date():
    india = pytz.timezone('Asia/Kolkata')
    today = datetime.datetime.now(india)
    return today.strftime("%A, %d %B %Y")

def open_music():
    music_folder = os.path.join(os.path.expanduser("~"), "Music")
    music_files = glob.glob(os.path.join(music_folder, "*.mp3"))
    if music_files:
        file_to_play = music_files[0]
        if platform.system() == "Windows":
            os.startfile(file_to_play)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_to_play])
        else:
            subprocess.call(["xdg-open", file_to_play])
        say("Playing music now.")
    else:
        say("Sorry, I couldn't find any music files.")

def use_terminator(command):
    try:
        result = subprocess.run(["terminator"] + command.split(), capture_output=True, text=True)
        print("Terminator Output:", result.stdout)
        say("Command executed using Terminator.")
    except Exception as e:
        print("Error running Terminator:", e)
        say("Failed to execute Terminator command.")


def run_in_terminator_mode(command):
    global using_terminator
    say("Processing your request in Terminator mode.")
    print(f"[TERMINATOR] Executing: {command}")
    if open_app(command):
        return
    import re


    if "write" in command.lower() and "notepad" in command.lower():
        topic_match = re.search(r'write (about|a|an|the)?(.*)', command.lower())
        topic = topic_match.group(2).strip() if topic_match else "something interesting"
        prompt = f"Write a paragraph about {topic}."
        content = ai(prompt)
        file_path = os.path.join(os.getcwd(), "terminator_output.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        os.system(f'start notepad.exe "{file_path}"')
        say("I've written about that in Notepad for you.")


    elif "play" in command.lower() and "youtube" in command.lower():
        query = command.lower().replace("play", "").replace("on youtube", "").strip()
        search_query = quote(query)
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        say(f"Searching YouTube for {query} and playing it.")
        time.sleep(6)
        pyautogui.moveTo(330, 350)
        pyautogui.click()

    elif "open gmail" in command.lower():
        webbrowser.open("https://mail.google.com")
        say("Opening Gmail.")


    elif "open" in command.lower() and "website" in command.lower():
        match = re.search(r'open (.*?) website', command.lower())
        site = match.group(1).strip().replace(" ", "")
        url = f"https://{site}.com"
        webbrowser.open(url)
        say(f"Opening {site} website.")
    elif "search" in command.lower():
        search_term = command.lower().replace("search", "").strip()
        search_query = quote(search_term)
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        say(f"Searching Google for {search_term}.")
    elif "send email" in command.lower() or "write email" in command.lower():
        import re
        # Example: "send email to john@example.com with subject Hello and body How are you"
        to_match = re.search(r"email to (\S+)", command)
        subject_match = re.search(r"subject (.*?) and", command)
        body_match = re.search(r"body (.*)", command)

        to_email = to_match.group(1) if to_match else "someone@example.com"
        subject = subject_match.group(1) if subject_match else "No Subject"
        body = body_match.group(1) if body_match else "No message content"

        say("Sending email now.")
        send_email(subject, body, to_email)

    else:
        os.system(f'start cmd /k "{command}"')
        say("Command executed.")


def play_youtube_music(query, pyautogui=None):
    search_query = quote(query)
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)
    say(f"Searching YouTube for {query} and playing first music.")
    time.sleep(5)
    if pyautogui:
        pyautogui.press("tab", presses=6)
        pyautogui.press("enter")

def open_file_by_name(name):
    user_home = os.path.expanduser("~")
    search_paths = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "Documents"),
        os.path.join(user_home, "Downloads"),
        user_home
    ]
    found = False
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if name.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    say(f"Opening file: {file}")
                    os.startfile(file_path)
                    return True
            for folder in dirs:
                if name.lower() in folder.lower():
                    folder_path = os.path.join(root, folder)
                    say(f"Opening folder: {folder}")
                    os.startfile(folder_path)
                    return True
    say("Sorry, I couldn't find any matching files or folders.")
    return False
def open_camera():
    say("Opening your camera now.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Sorry, I couldn't access the camera.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            say("Failed to grab frame.")
            break
        cv2.imshow("Sage Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            say("Closing camera.")
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    say("Hello My name is Sage")
    print('Sage')
    while True:
        print("Listening.....")
        query = takecommand()

        if "use terminator" in query.lower() or (query.lower().strip() == "terminator"):
            using_terminator = True
            say("What should I do in the terminal?")
            continue
        if using_terminator:
            if query is None:
                continue

            query = query.lower().strip()

            if "stop terminator" in query or "exit terminator" in query or "leave terminal" in query:
                say("Exiting Terminator mode.")
                using_terminator = False
                continue

            run_in_terminator_mode(query)
            continue

        if "i want to type" in query.lower():
            say("Okay, switching to text mode. Please type your command.")
            query = input("Enter your command: ")

        if "play" in query and "youtube" in query:
            video_query = query.lower().replace("play", "").replace("on youtube", "").strip()
            play_youtube_music(video_query, pyautogui)
            continue

        if "use terminator" in query.lower():
            if using_terminator:
                using_terminator = True

        if expecting_code:
            if "type" in query.lower():
                say("Paste your code. Type 'done' when you're finished.")
                code_lines = []
                while True:
                    line = input()
                    if line.strip().lower() == "done":
                        break
                    code_lines.append(line)
                full_code = "\n".join(code_lines)
            else:
                say("Please speak your code. Say 'done' when you're finished.")
                code_lines = []
                while True:
                    line = takecommand()
                    if "done" in line.lower():
                        break
                    line = line.replace("colon", ":").replace("indent", "    ").replace("open parenthesis", "(").replace("close parenthesis", ")")
                    code_lines.append(line)
                full_code = "\n".join(code_lines)
            corrected_code = ai(f"Please correct the following Python code:\n\n{full_code}")
            say("Here's the corrected version.")
            print("Corrected Code:\n", corrected_code)
            expecting_code = False
            continue

        if "correct my code" in query.lower():
            say("Okay, would you like to type or speak your code?")
            expecting_code = True
            continue

        print("Processing query:", query)

        if "stop searching" in query.lower():
            searching = False
            say("I've paused searching. Say 'start searching' to resume.")
            continue
        elif "start searching" in query.lower():
            searching = True
            say("I've resumed searching. How can I help you?")
            continue

        if "exit youtube" in query.lower() or "close youtube" in query.lower():
            say("Closing the YouTube tab.")
            pyautogui.hotkey('ctrl', 'w')
            continue

        skip_processing = False
        def search_google(query):
            search_query = quote(query)
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            say(f"Searching Google for {query}.")

        apps = [["game", r'start "" "C:\\Users\\Public\\Desktop\\Grand Theft Auto V.lnk"'], ["music", open_music], ["notepad", r'start "" "C:\\Windows\\notepad.exe"'], ["gallery", r'start "" "C:\\Users\\irsha\\OneDrive\\Pictures"']]
        for app in apps:
            if f"open {app[0]}" in query.lower():
                say(f"Starting {app[0]}, sir...")
                if callable(app[1]):
                    app[1]()
                else:
                    os.system(app[1])
                skip_processing = True

        if "the time" in query.lower():
            current_time = get_current_time()
            say(f"Sir, the time is {current_time}")
            print(f"Current time: {current_time}")
            skip_processing = True

        if "the date" in query.lower():
            current_date = get_current_date()
            say(f"Sir, today is {current_date}")
            print(f"Current date: {current_date}")
            skip_processing = True
        if "play" in query and "youtube" in query:
            video_query = query.lower().replace("play", "").replace("on youtube", "").strip()
            play_youtube_music(video_query, pyautogui)
            continue

        if "write an email" in query.lower() or "send email" in query.lower():
            say("Who should I send the email to?")
            to_email = input("Receiver Email Address: ")
            say("What is the subject of the email?")
            subject = takecommand()

            say("What should I write in the email?")
            body = takecommand()

            say("Should I make it more professional using AI?")
            confirmation = takecommand()

            if "yes" in confirmation.lower():
                prompt = f"Write a professional email with subject: '{subject}' and message: '{body}'"
                body = ai(prompt)
                print("AI-enhanced Email:\n", body)

            send_email(subject, body, to_email)
            continue

        if any(x in query.lower() for x in ["exit", "quit", "good bye", "bye"]):
            say("Goodbye sir!")
            print("sage shutting down...")
            break

        if "open file" in query.lower() or "open image" in query.lower() or "open pdf" in query.lower() or "open music" in query.lower():
            say("Which file should I open?")
            file_name = takecommand()
            open_file_by_name(file_name)
            continue
        elif "open camera" in query:
            open_camera()

        if skip_processing:
            continue

        print("Processing query:", query)

        if "using ai" in query.lower():
            response = ai(query)
            print("AI output:", response)
            say(response)
        elif searching:
            response = chat(query)
            print("Chat output:", response)
