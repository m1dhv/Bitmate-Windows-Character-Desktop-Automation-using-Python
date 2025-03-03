import speech_recognition as sr
import time
import openapp
import pet1 
import directorysaver
import openai

class VoiceAssistant:
    def __init__(self, trigger_word="siri"):
        self.trigger_word = trigger_word.lower()
        self.recognizer = sr.Recognizer()
        
    
    def refine_text(self, text):
        """
        Mock API for text refinement.
        Replace this with an actual API call if needed.
        """
        time.sleep(1)  # Simulate network delay
        return text.upper()  # Example refinement
   
    def listen_for_trigger(self):
        
        """
        Listens for the trigger word.
        Returns True if the trigger word is detected.
        """
        with sr.Microphone() as source:
            print("Listening for trigger word...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                # Recognize speech using Google Web Speech API
                trigger = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {trigger}")
                
                if "open app" in trigger:
                    words = trigger.split()
                    if len(words) > 1:
                        try:
                            appname = words[words.index("app") + 1]
                            openapp.open_software(appname)
                        except IndexError:
                            print("Try again")
                            
                            
                
                if "buddy" in trigger:
                    words = trigger.split()
                    if len(words) > 1:
                        name = words[words.index("buddy") + 1]
                        if name == "sleep":
                            pet1.DesktopPet.start_sleep(self);    
                if "save file" in trigger:
                    words = trigger.split()
                    try:
                        name1 = words[words.index("file") + 1]
                        directorysaver.dircopy(name1)
                    except IndexError:
                        print("Try again")
                        
                
                if "take file" in trigger:
                    words = trigger.split()
                    try:
                     name = words[words.index("file") + 1]
                     directorysaver.diropen(name)
                    except IndexError:
                        print("Try again")
                        pet1.DesktopPet.display_message("Try again")
                

                if "remove file" in trigger:
                    words = trigger.split()
                    try:
                        name = words[words.index("file") + 1]
                        directorysaver.delete_entry(name)
                    except IndexError:
                        print("Try again")
                        pet1.DesktopPet.display_message("Try again")

                if "ai" in trigger:
                    words = trigger.split()
                    new_text = " ".join(words[1:])
                    openai.askai(new_text)  
                    
                            
                        
                
                    
                if self.trigger_word in trigger:
                    print(f"Trigger word '{self.trigger_word}' detected. Listening for command...")
                    return True
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        return False

    def listen_for_command(self):
        """
        Listens for the command after the trigger word is detected.
        Returns the recognized command as text.
        """
        with sr.Microphone() as source:
            print("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                # Recognize speech using Google Web Speech API
                command = self.recognizer.recognize_google(audio)
                print(f"Command: {command}")
                return command
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        return None
    
    
    def process_command(self):
        """
        Listens for the trigger word, then listens for a command,
        refines the command, and returns the refined text.
        """
        if self.listen_for_trigger():
            command = self.listen_for_command()
            if command:
                refined_text = self.refine_text(command)
                print(f"Refined Text: {refined_text}")
                return refined_text
        return None



