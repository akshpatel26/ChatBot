from tkinter import *
from tkinter import messagebox, scrolledtext, filedialog
from datetime import datetime
import threading
import time
import random

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI ChatBot - Smart Assistant")
        # EXACT same window settings as developer.py
        self.root.geometry("600x400")
        self.root.configure(bg="white")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)     # Minimum reasonable window
        self.root.maxsize(1600, 900)    # Up to ~75% of screen resolution
 
        
        # Center the window (same method as developer.py)
        self.center_window()
        
        # Chat data
        self.chat_history = []
        self.typing_thread = None
        
        # Create main layout
        self.create_layout()
        
        # Add welcome message
        self.add_bot_message("Hello! I'm your AI assistant. How can I help you today?")
        
        self.static_responses = {
        'hello': 'Hi there! How can I help you?',
        'hi': 'Hello! Nice to meet you!',
        'how are you': 'I\'m doing great! How about you?',
        'who created you': 'Aksh did using Python.',
        'thanks': 'You\'re welcome!',
        'thank you': 'Happy to help!',
        'what is your name': 'I\'m your AI chatbot assistant!',
        'help': 'I\'m here to help! Ask me anything.',
        'what is machine learning': 'Machine Learning (ML) is a subfield of Artificial Intelligence (AI)...',
        'how does face recognition work ?': 'The Advance Face Recognition Student Attendance System is...',
        'how does face recognition work step by step': 'Step 1: Student Registration...\nStep 2: Model Training...\n...',
        'bye': 'Goodbye! Have a great day!',
        'how do i add a new photo folder?': 'To add a new photo folder, register a student...'
}


    def center_window(self):
        """Center the window on screen - EXACT same as developer.py"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"600x400+{x}+{y}")

    def create_layout(self):
        """Create compact layout similar to developer.py structure"""
        # Header section - same style as developer.py
        header_frame = Frame(self.root, bg="white")
        header_frame.pack(fill=X, padx=20, pady=(15, 10))

        title_label = Label(header_frame, text="AI ChatBot Assistant", 
                           font=("Segoe UI", 20, "bold"), 
                           bg="white", fg="#2c3e50")
        title_label.pack()

        subtitle_label = Label(header_frame, text="Intelligent Conversational AI & Smart Assistant", 
                              font=("Segoe UI", 10, "italic"), 
                              bg="white", fg="#7f8c8d")
        subtitle_label.pack(pady=(2, 8))

        desc_text = ("Advanced AI chatbot powered by natural language processing. "
                    "Ask questions, get help, or have a friendly conversation!")
        
        desc_label = Label(header_frame, text=desc_text, font=("Segoe UI", 9), 
                          bg="white", fg="#34495e", wraplength=550, justify=CENTER)
        desc_label.pack()

        # Main content frame - same structure as developer.py
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left side - Chat area (main content)
        chat_frame = Frame(main_frame, bg="white")
        chat_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))

        # Chat title
        chat_title = Label(chat_frame, text="💬 Live Chat Session", 
                          font=("Segoe UI", 12, "bold"), 
                          bg="white", fg="#2980b9")
        chat_title.pack(anchor=W, pady=(0, 10))

        # Chat display area
        self.create_chat_area(chat_frame)
        
        # Input area
        self.create_input_area(chat_frame)

        # Right side - Controls and Info (like developer.py sidebar)
        right_frame = Frame(main_frame, bg="white")
        right_frame.pack(side=RIGHT, fill=Y)

        self.create_controls_section(right_frame)
        self.create_stats_section(right_frame)

    def create_chat_area(self, parent):
        """Create chat display area"""
        chat_container = LabelFrame(parent, text="Chat Messages", 
                                   font=("Segoe UI", 9, "bold"), bg="white", 
                                   fg="#2c3e50", padx=5, pady=5)
        chat_container.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=WORD,
            height=12,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief=FLAT,
            padx=8,
            pady=5
        )
        self.chat_display.pack(fill=BOTH, expand=True)

        # Configure text tags for different message types
        self.chat_display.tag_configure("user_label", foreground="#3498db", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_configure("bot_label", foreground="#e74c3c", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_configure("timestamp", foreground="#95a5a6", font=("Segoe UI", 8))
        self.chat_display.tag_configure("user_msg", foreground="#2c3e50", font=("Segoe UI", 9))
        self.chat_display.tag_configure("bot_msg", foreground="#34495e", font=("Segoe UI", 9))
        self.chat_display.tag_configure("typing", foreground="#95a5a6", font=("Segoe UI", 9, "italic"))

        # Make read-only
        self.chat_display.config(state=DISABLED)

    def create_input_area(self, parent):
        """Create message input area"""
        input_container = LabelFrame(parent, text="Type Your Message", 
                                    font=("Segoe UI", 9, "bold"), bg="white", 
                                    fg="#2c3e50", padx=8, pady=8)
        input_container.pack(fill=X)

        # Input frame
        input_frame = Frame(input_container, bg="white")
        input_frame.pack(fill=X)

        # Message entry
        self.message_entry = Text(
            input_frame,
            height=2,
            font=("Segoe UI", 9),
            bg="white",
            fg="#2c3e50",
            relief=RIDGE,
            bd=1,
            padx=5,
            pady=3,
            wrap=WORD
        )
        self.message_entry.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        # Send button
        self.send_button = Button(
            input_frame,
            text="Send\n📤",
            font=("Segoe UI", 8, "bold"),
            bg="#3498db",
            fg="white",
            relief=FLAT,
            cursor="hand2",
            width=6,
            command=self.send_message
        )
        self.send_button.pack(side=RIGHT, fill=Y)

        # Bind Enter key
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        self.message_entry.bind("<Shift-Return>", lambda e: None)

    def create_controls_section(self, parent):
        """Create control buttons section - similar to developer.py image section"""
        controls_frame = LabelFrame(parent, text="Chat Controls", 
                                   font=("Segoe UI", 9, "bold"), bg="white", 
                                   fg="#2c3e50", padx=10, pady=10)
        controls_frame.pack(pady=(0, 10))

        # Control buttons
        controls = [
            ("Clear Chat", self.clear_chat, "#e74c3c"),
            ("Save Chat", self.save_chat, "#27ae60"),
            ("Settings", self.show_settings, "#f39c12"),
            ("Theme", self.toggle_theme, "#8e44ad")
        ]

        for text, command, color in controls:
            btn = Button(controls_frame, text=text,
                        font=("Segoe UI", 8, "bold"),
                        bg=color, fg="white",
                        relief=FLAT, cursor="hand2",
                        width=12, pady=2,
                        command=command)
            btn.pack(pady=2)

    def create_stats_section(self, parent):
        """Create stats section - similar to developer.py skills section"""
        stats_frame = LabelFrame(parent, text="Chat Statistics", 
                                font=("Segoe UI", 9, "bold"), bg="white", 
                                fg="#2c3e50", padx=10, pady=8)
        stats_frame.pack(fill=X)

        stats_data = [
            ("Messages:", "0"),
            ("Responses:", "0"),
            ("Session:", "Active"),
            ("Status:", "Online")
        ]

        self.stats_labels = {}
        for category, value in stats_data:
            stat_frame = Frame(stats_frame, bg="white")
            stat_frame.pack(fill=X, pady=1)
            
            Label(stat_frame, text=category, font=("Segoe UI", 8, "bold"), 
                  bg="white", fg="#2980b9", width=8, anchor="w").pack(side=LEFT)
            
            value_label = Label(stat_frame, text=value, font=("Segoe UI", 8), 
                               bg="white", fg="#7f8c8d")
            value_label.pack(side=LEFT, padx=(5, 0))
            
            self.stats_labels[category.replace(":", "")] = value_label

    def send_message(self):
        """Send user message"""
        message = self.message_entry.get("1.0", "end-1c").strip()
        
        if not message:
            return
        
        # Add user message
        self.add_user_message(message)
        
        # Clear input
        self.message_entry.delete("1.0", END)
        
        # Show typing and get bot response
        self.show_typing()
        threading.Thread(target=self.get_bot_response, args=(message,), daemon=True).start()

    def add_user_message(self, message):
        """Add user message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, "You ", "user_label")
        self.chat_display.insert(END, f"({timestamp})\n", "timestamp")
        self.chat_display.insert(END, f"{message}\n\n", "user_msg")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)
        
        self.chat_history.append({"type": "user", "message": message, "time": timestamp})
        self.update_stats()

    def add_bot_message(self, message):
        """Add bot message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, "Bot ", "bot_label")
        self.chat_display.insert(END, f"({timestamp})\n", "timestamp")
        self.chat_display.insert(END, f"{message}\n\n", "bot_msg")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)
        
        self.chat_history.append({"type": "bot", "message": message, "time": timestamp})
        self.update_stats()

    def show_typing(self):
        """Show typing indicator"""
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, "Bot is typing", "typing")
        self.chat_display.insert(END, "...\n", "typing")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def remove_typing(self):
        """Remove typing indicator"""
        self.chat_display.config(state=NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.config(state=DISABLED)

    def get_bot_response(self, user_message):
        """Generate bot response"""
        # Simulate thinking time
        time.sleep(random.uniform(1, 2.5))
        
        self.remove_typing()
        
        # Generate response
        response = self.generate_response(user_message.lower())
        self.add_bot_message(response)

    def generate_response(self, message):
        """Generate intelligent responses"""
        # Smart responses based on keywords
        if any(word in message for word in ["hello", "hi", "hey"]):
            return random.choice([
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Hey! Nice to meet you. How are you doing?"
            ])
        
        elif any(word in message for word in ["how are you", "how do you do"]):
            return "I'm doing great, thank you for asking! I'm here and ready to help. How are you?"
        
        elif any(word in message for word in ["name", "who are you"]):
            return "I'm your AI ChatBot Assistant! You can call me Bot. I'm here to help with questions and conversations."
        
        elif any(word in message for word in ["help", "assist", "support"]):
            return "I'm here to help! I can answer questions, have conversations, provide information, or just chat. What would you like to talk about?"
        
        elif any(word in message for word in ["time", "clock"]):
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."
        
        elif any(word in message for word in ["date", "today"]):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
        
        elif any(word in message for word in ["weather", "temperature"]):
            return "I don't have access to real-time weather data, but I recommend checking your local weather app or website for current conditions!"
        
        elif any(word in message for word in ["joke", "funny"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a fake noodle? An impasta!"
            ]
            return random.choice(jokes)
        
        elif any(word in message for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! It was great chatting with you. Feel free to come back anytime!"
        
        elif any(word in message for word in ["thank", "thanks"]):
            return "You're very welcome! I'm happy to help. Is there anything else you'd like to know?"
        
        else:
            # General responses
            responses = [
                "That's interesting! Tell me more about that.",
                "I understand. What else would you like to discuss?",
                "Thanks for sharing! How can I help you further?",
                "That's a good point. What other questions do you have?",
                "I see what you mean. What else is on your mind?",
                "Interesting perspective! What would you like to explore next?"
            ]
            return random.choice(responses)
        
    def generate_response(self, message):
   
         # Normalize input
        msg_clean = message.strip().lower()
     
         # Check static responses first
        for key in self.static_responses:
             if key in msg_clean:
                 return self.static_responses[key]
     
         # Smart keywords fallback (your previous logic)
        if any(word in msg_clean for word in ["joke", "funny"]):
             jokes = [
                 "Why don't scientists trust atoms? Because they make up everything!",
                 "Why did the scarecrow win an award? He was outstanding in his field!",
                 "What do you call a fake noodle? An impasta!"
             ]
             return random.choice(jokes)
     
         # Default fallback
        fallback_responses = [
             "That's interesting! Tell me more about that.",
             "I understand. What else would you like to discuss?",
             "Thanks for sharing! How can I help you further?",
             "That's a good point. What other questions do you have?",
             "I see what you mean. What else is on your mind?",
             "Interesting perspective! What would you like to explore next?"
         ]
        return random.choice(fallback_responses)
    

    def update_stats(self):
        """Update chat statistics"""
        user_msgs = len([msg for msg in self.chat_history if msg["type"] == "user"])
        bot_msgs = len([msg for msg in self.chat_history if msg["type"] == "bot"])
        
        self.stats_labels["Messages"].config(text=str(user_msgs))
        self.stats_labels["Responses"].config(text=str(bot_msgs))

    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear Chat", "Clear all chat messages?"):
            self.chat_display.config(state=NORMAL)
            self.chat_display.delete("1.0", END)
            self.chat_display.config(state=DISABLED)
            self.chat_history.clear()
            self.update_stats()
            self.add_bot_message("Chat cleared! How can I help you?")

    def save_chat(self):
        """Save chat to file"""
        if not self.chat_history:
            messagebox.showinfo("Save Chat", "No messages to save!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Chat History"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"ChatBot Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for msg in self.chat_history:
                        sender = "You" if msg["type"] == "user" else "Bot"
                        f.write(f"{sender} ({msg['time']}): {msg['message']}\n\n")
                
                messagebox.showinfo("Success", "Chat saved successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", 
                           "⚙️ ChatBot Settings\n\n" +
                           "• Theme: Light Mode\n" +
                           "• Font Size: Normal\n" +
                           "• Auto-save: Disabled\n" +
                           "• Sound: Enabled\n\n" +
                           "More options coming soon!")

    def toggle_theme(self):
        current_theme = self.theme.get()

        if current_theme == "Light":
            self.root.configure(bg="#2c3e50")
            self.main_label.configure(bg="#2c3e50", fg="white")
    
            # Apply dark background to text area
            self.chat_display.configure(bg="#34495e", fg="white", insertbackground="white")
    
            # Apply dark background to entry
            self.message_entry.configure(bg="#34495e", fg="white", insertbackground="white")
    
            # Apply dark background to control buttons
            for btn in self.control_buttons:
                btn.configure(bg="#3c5f7f", fg="white", activebackground="#5d6d7e")
    
            # Apply dark background to status bar
            self.status_label.configure(bg="#2c3e50", fg="white")
    
            self.theme.set("Dark")
    
        else:
            self.root.configure(bg="white")
            self.main_label.configure(bg="white", fg="black")
    
            # Apply light background to text area
            self.chat_display.configure(bg="white", fg="black", insertbackground="black")
    
            # Apply light background to entry
            self.message_entry.configure(bg="white", fg="black", insertbackground="black")
    
            # Apply light background to control buttons
            for btn in self.control_buttons:
                btn.configure(bg="#d9d9d9", fg="black", activebackground="#e0e0e0")
    
            # Apply light background to status bar
            self.status_label.configure(bg="white", fg="black")
    
            self.theme.set("Light")

        

if __name__ == "__main__":
    root = Tk()
    app = ChatBotGUI(root)
    root.mainloop()