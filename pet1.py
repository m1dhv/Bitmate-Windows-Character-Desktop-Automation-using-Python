import tkinter as tk
from tkinter import Toplevel, Menu
import os
from PIL import Image, ImageTk
import micopn

class DesktopPet:
    def __init__(self, character_name, gif_paths):
        """Initialize the desktop pet with GIF animations and a right-click menu."""
        self.bubble_active = False
        self.sleep_active = False
        self.character_name = character_name
        self.gif_paths = gif_paths
        self.cycle = 0
        self.dragging = False
        self.frames = []
        self.current_gif = 'idle'
        self.is_sleeping = False

        # Create the Tkinter window
        self.window = tk.Tk()
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)  # Remove window borders
        self.window.wm_attributes('-topmost', True)  # Keep on top
        self.window.wm_attributes('-transparentcolor', 'black')  # Make black transparent

        # Screen dimensions
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Pet's size
        self.pet_width = 100
        self.pet_height = 100

        # Taskbar height
        self.taskbar_height = 50

        # Start position (bottom-right corner)
        self.x = self.screen_width - self.pet_width
        self.y = self.screen_height - self.pet_height - self.taskbar_height

        # Position the pet
        self.window.geometry(f"{self.pet_width}x{self.pet_height}+{self.x}+{self.y}")

        # Create label for displaying the GIF
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.pack()

        # Load GIF frames
        self.load_gif(self.current_gif)

        # Create speech bubble for messages
        self.speech_bubble = tk.Label(self.window, text="", bg="white", fg="black", font=("Arial", 10), bd=1, relief="solid")
        self.speech_bubble.place(relx=0.5, rely=0, anchor="n")  # Position above the pet
        self.speech_bubble.place_forget()  # Hide initially

        # Bind mouse events for dragging and menu
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<Button-3>", self.show_menu)  # Right-click menu

        # Create a right-click menu
        self.menu = Menu(self.window, tearoff=0)
        self.menu.add_command(label="Inventory", command=self.open_inventory)
        self.menu.add_command(label="Sleep", command=self.start_sleep)
        self.menu.add_command(label="Wake", command=self.start_woke)
        self.menu.add_command(label="Quit", command=self.quit_app)

        # Start animation
        self.window.after(1, self.animate_gif)

    def load_gif(self, gif_key):
        """Load GIF frames into a list for animation."""
        try:
            if self.character_name in self.gif_paths:
                gif = self.gif_paths[self.character_name][gif_key]
                if os.path.exists(gif):
                    self.frames = []
                    image = Image.open(gif)
                    for frame in range(0, image.n_frames):
                        image.seek(frame)
                        frame_image = ImageTk.PhotoImage(image.copy())
                        self.frames.append(frame_image)
                    print(f"{self.character_name} GIF loaded successfully!")
                    self.label.configure(image=self.frames[0])  # Set first frame
                else:
                    print(f"Error: GIF not found at {gif}")
            else:
                print(f"Error: {self.character_name} not found in gif_paths")
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def start_drag(self, event):
        """Start dragging the pet."""
        self.dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        """Handle dragging."""
        if self.dragging:
            new_x = self.window.winfo_x() + (event.x - self.offset_x)
            new_y = self.window.winfo_y() + (event.y - self.offset_y)

            # Ensure the pet stays within screen bounds
            new_x = max(0, min(new_x, self.screen_width - self.pet_width))
            new_y = max(0, min(new_y, self.screen_height - self.pet_height - self.taskbar_height))

            self.window.geometry(f"{self.pet_width}x{self.pet_height}+{new_x}+{new_y}")

    def stop_drag(self, event):
        """Stop dragging."""
        self.dragging = False

    def show_menu(self, event):
        """Show the right-click menu at the cursor position."""
        self.menu.post(event.x_root, event.y_root)

    def open_inventory(self):
        """Open an inventory window to change the pet character."""
        inventory_window = Toplevel(self.window)
        inventory_window.title("Inventory")
        inventory_window.geometry("300x250")
        inventory_window.config(bg="white")

        label = tk.Label(inventory_window, text="Choose your pet:", bg="white", font=("Arial", 12))
        label.pack(pady=10)

        def change_pet(pet_name):
            """Change the pet's character."""
            self.character_name = pet_name
            self.current_gif = 'idle'  # Default to idle animation
            self.load_gif(self.current_gif)
            inventory_window.destroy()

        # Buttons for selecting different characters
        for pet_name in self.gif_paths.keys():
            tk.Button(inventory_window, text=pet_name, command=lambda p=pet_name: change_pet(p)).pack(pady=5)

    def quit_app(self):
        """Quit the application."""
        self.window.destroy()
    
    def animate_gif(self):
        """Loop through GIF frames to create an animation."""
        if self.frames:  # Ensure there are frames
            self.label.configure(image=self.frames[self.cycle])
            if self.current_gif == 'idle_to_sleep' and self.cycle == len(self.frames) - 1:
                # Transition to sleeping state after the transition GIF finishes
                self.is_sleeping = True
                self.current_gif = 'sleeping'
                self.load_gif(self.current_gif)
                self.cycle = 0
            elif self.current_gif == 'sleeping':
                # Loop the sleeping GIF
                self.cycle = (self.cycle + 1) % len(self.frames)
            else:
                # Loop other GIFs
                self.cycle = (self.cycle + 1) % len(self.frames)
        self.window.after(100, self.animate_gif)  # Adjust speed

    def display_message(self, message):
        if not self.sleep_active:
            """Display a specific message in a speech bubble."""
            self.speech_bubble.config(text=message)
            self.speech_bubble.place(relx=0.5, rely=0, anchor="n")
            # Position above the pet
            # Hide the speech bubble after 3 seconds
            self.window.after(3000, self.hide_message)

    def hide_message(self):
        """Hide the speech bubble."""
        self.speech_bubble.place_forget()

    def start_sleep(self):
        self.current_gif = 'idle_to_sleep'
        self.load_gif(self.current_gif)
        """Start the sleep sequence."""
        self.sleep_active = True
        if not self.is_sleeping:
            self.sleep_state()
            self.current_gif = 'sleep'
            self.load_gif(self.current_gif)
            self.cycle = 0
    def sleep_state(self):
        if self.sleep_active == True:
            return True
    
    def start_woke(self):
        self.bubble_active = True
        self.sleep_active = False
        self.current_gif = 'sleep_to_idle'
        self.load_gif(self.current_gif)
        """Start the wake sequence."""
        if not self.is_sleeping:
            self.current_gif = 'idle'
            self.load_gif(self.current_gif)
            self.cycle = 0

    def run(self):
        """Start the pet's main loop."""
        self.window.mainloop()

