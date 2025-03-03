import pet1  # Custom module for the desktop pet
import spt   # Custom module for the voice assistant
import threading
import queue


# Function to listen for voice commands in a separate thread

def __init__(self):
    self.buddy_is_sleep = False
    self.spt_active = False

def listen_for_commands(assistant, command_queue):
    while True:
            if not pet1.DesktopPet.sleep_state == True:
                refined_text = assistant.process_command()
                if refined_text:
                # Put the refined text in the queue for the main thread to process
                    command_queue.put(refined_text)
                 
                else:
                    command_queue.put("No command detected. Listening again...")

# Main function
def main():
    # Define GIF paths for multiple pets
    pet_gifs = {
        'Buddy': {
            'idle': 'Character-test/idle.gif',
            'sleep': 'Character-test/sleep.gif',
            'idle_to_sleep': 'Character-test/idle_to_sleep.gif',
            'sleep' : 'Character-test/sleep.gif',
            'sleep_to_idle':'Character-test/sleep_to_idle.gif',
            
        },
        'Whiskers': {
            'idle': 'Character-test/idle.gif',
            'sleep': 'Character-test/sleep.gif'
        },
        'Fluffy': {
            'idle': 'Character-test/idle_to_sleep.gif',
            'sleep': 'Character-test/sleep.gif'
        }
    }
    

    # Create the pet
    buddy = pet1.DesktopPet("Buddy", pet_gifs)

    # Display a specific message initially
    buddy.display_message("Hello! I'm Buddy. How can I help you?")

    # Create the voice assistant
    assistant = spt.VoiceAssistant(trigger_word="rachel")  # You can change the trigger word

    # Create a queue to safely communicate with the main thread
    command_queue = queue.Queue()


    # Create the assistant thread to run the voice assistant
    assistant_thread = threading.Thread(target=listen_for_commands, args=(assistant, command_queue))
    assistant_thread.daemon = True  # Allow the assistant thread to exit when the main thread exits
    assistant_thread.start()

    # Function to safely update Buddy's message from the main thread
    def update_buddy_message():
        if not command_queue.empty():
            # Get the latest message from the queue
            command_message = command_queue.get()
            buddy.display_message(command_message)  # Display the refined text

        # Call this function again after 100ms to check for new messages
        buddy.window.after(100, update_buddy_message)

    # Start the message updating process
    update_buddy_message()

    # Run the GUI in the main thread
    buddy.run()

# Entry point
if __name__ == "__main__":
    main()