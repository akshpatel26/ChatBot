from tkinter import *
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import requests
import json
import os
from datetime import datetime
import threading
import time
import random

class EnhancedChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced AI Chatbot - Smart Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        self.root.maxsize(1600, 900)
        
        # Replace with your actual Gemini API key
        self.API_KEY = "AIzaSyBsWk1oh0RIPiuzeIeIFf0zaZJWEthhe7w"
        
        # Chat data
        self.chat_history = []
        self.typing_thread = None
        self.theme = StringVar(value="Light")
        
        # Random questions pool
        self.random_questions = [
            "What's your favorite hobby?",
            "Tell me about your goals for this year.",
            "What's the most interesting place you've visited?",
            "What technology do you find most fascinating?",
            "What's your favorite type of music?",
            "If you could learn any skill instantly, what would it be?",
            "What's the best advice you've ever received?",
            "What motivates you the most?",
            "What's your favorite season and why?",
            "If you could have dinner with anyone, who would it be?",
            "What's the most challenging thing you've overcome?",
            "What's your ideal way to spend a weekend?",
            "What book or movie has influenced you the most?",
            "What's something new you'd like to try?",
            "What's your biggest dream or aspiration?"
        ]
        
        # Static responses
        self.static_responses = {
            'hello': 'Hi there! How can I help you?',
            'hi': 'Hello! Nice to meet you!',
            'how are you': 'I\'m doing great! How about you?',
            'who created you': 'Aksh created me using Python with AI integration.',
            'thanks': 'You\'re welcome!',
            'thank you': 'Happy to help!',
            'what is your name': 'I\'m your Enhanced AI Chatbot Assistant!',
            'help': 'I\'m here to help! Ask me anything or try "Ask me something" for random questions.',
            'what is machine learning': 'Machine Learning (ML) is a subfield of Artificial Intelligence (AI) that focuses on building systems that learn from data and improve over time without being explicitly programmed.',
            'how does face recognition work': 'Face recognition uses computer vision and machine learning to identify and verify individuals by analyzing facial features and patterns.',
            'bye': 'Goodbye! Have a great day!',
            'goodbye': 'See you later!',
            'ask me something': 'RANDOM_QUESTION',
            'random question': 'RANDOM_QUESTION',
            'surprise me': 'RANDOM_QUESTION'
        }
        
        # Center the window and create layout
        self.center_window()
        self.create_layout()
        
        # Add welcome message
        self.add_bot_message("Hello! I'm your Enhanced AI Chatbot. I can answer questions using AI, respond to common queries, and even ask you random questions! Type 'ask me something' to get a random question.",)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")

    def create_layout(self):
        """Create the main layout"""
        # Header section
        self.create_header()
        
        # Main content frame
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Chat area
        chat_frame = Frame(main_frame, bg="white")
        chat_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))
        
        self.create_chat_area(chat_frame)
        self.create_input_area(chat_frame)
        
        # Right side - Controls and features
        right_frame = Frame(main_frame, bg="white")
        right_frame.pack(side=RIGHT, fill=Y)
        
        self.create_controls_section(right_frame)
        self.create_features_section(right_frame)
        self.create_stats_section(right_frame)

    def create_header(self):
        """Create header section"""
        # Try to load chatbot image
        try:
            if os.path.exists('Chatbot.png'):
                img_chat = Image.open('Chatbot.png')
                img_chat = img_chat.resize((60, 60), Image.Resampling.LANCZOS)
                self.photoimg = ImageTk.PhotoImage(img_chat)
            else:
                img_chat = Image.new('RGB', (60, 60), color='lightgreen')
                self.photoimg = ImageTk.PhotoImage(img_chat)
        except Exception:
            img_chat = Image.new('RGB', (60, 60), color='#3498db')
            self.photoimg = ImageTk.PhotoImage(img_chat)
        
        header_frame = Frame(self.root, bg="white")
        header_frame.pack(fill=X, padx=20, pady=(15, 10))
        
        # Title with image
        title_frame = Frame(header_frame, bg="white")
        title_frame.pack()
        
        img_label = Label(title_frame, image=self.photoimg, bg="white")
        img_label.pack(side=LEFT, padx=(0, 10))
        
        text_frame = Frame(title_frame, bg="white")
        text_frame.pack(side=LEFT)
        
        title_label = Label(text_frame, text="Enhanced AI Chatbot", 
                           font=("Segoe UI", 24, "bold"), 
                           bg="white", fg="#2c3e50")
        title_label.pack(anchor=W)
        
        subtitle_label = Label(text_frame, text="AI-Powered Intelligent Assistant with Random Questions", 
                              font=("Segoe UI", 12, "italic"), 
                              bg="white", fg="#7f8c8d")
        subtitle_label.pack(anchor=W)

    def create_chat_area(self, parent):
        """Create chat display area"""
        chat_container = LabelFrame(parent, text="💬 Chat Messages", 
                                   font=("Segoe UI", 10, "bold"), bg="white", 
                                   fg="#2c3e50", padx=5, pady=5)
        chat_container.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=WORD,
            height=20,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            fg="#2c3e50",
            relief=FLAT,
            padx=10,
            pady=8
        )
        self.chat_display.pack(fill=BOTH, expand=True)
        
        # Configure text tags
        self.chat_display.tag_configure("user_label", foreground="#3498db", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("bot_label", foreground="#e74c3c", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("ai_label", foreground="#27ae60", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("timestamp", foreground="#95a5a6", font=("Segoe UI", 8))
        self.chat_display.tag_configure("user_msg", foreground="#2c3e50", font=("Segoe UI", 10))
        self.chat_display.tag_configure("bot_msg", foreground="#34495e", font=("Segoe UI", 10))
        self.chat_display.tag_configure("ai_msg", foreground="#2d5a3f", font=("Segoe UI", 10))
        self.chat_display.tag_configure("typing", foreground="#95a5a6", font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_configure("error", foreground="#dc2626", font=("Segoe UI", 10))
        
        self.chat_display.config(state=DISABLED)

    def create_input_area(self, parent):
        """Create message input area"""
        input_container = LabelFrame(parent, text="✍️ Type Your Message", 
                                    font=("Segoe UI", 10, "bold"), bg="white", 
                                    fg="#2c3e50", padx=8, pady=8)
        input_container.pack(fill=X)
        
        input_frame = Frame(input_container, bg="white")
        input_frame.pack(fill=X)
        
        # Message entry
        self.message_entry = Text(
            input_frame,
            height=3,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2c3e50",
            relief=RIDGE,
            bd=1,
            padx=8,
            pady=5,
            wrap=WORD
        )
        self.message_entry.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # Button frame
        btn_frame = Frame(input_frame, bg="white")
        btn_frame.pack(side=RIGHT, fill=Y)
        
        # Send button
        self.send_button = Button(
            btn_frame,
            text="Send\n📤",
            font=("Segoe UI", 9, "bold"),
            bg="#3498db",
            fg="white",
            relief=FLAT,
            cursor="hand2",
            width=8,
            command=self.send_message
        )
        self.send_button.pack(pady=(0, 5))
        
        # Random question button
        self.random_btn = Button(
            btn_frame,
            text="Random\n❓",
            font=("Segoe UI", 9, "bold"),
            bg="#f39c12",
            fg="white",
            relief=FLAT,
            cursor="hand2",
            width=8,
            command=self.ask_random_question
        )
        self.random_btn.pack()
        
        # Bind Enter key
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        self.message_entry.bind("<Shift-Return>", lambda e: None)
        self.message_entry.focus()

    def create_controls_section(self, parent):
        """Create control buttons section"""
        controls_frame = LabelFrame(parent, text="🎛️ Chat Controls", 
                                   font=("Segoe UI", 9, "bold"), bg="white", 
                                   fg="#2c3e50", padx=10, pady=10)
        controls_frame.pack(pady=(0, 10))
        
        # Control buttons
        controls = [
            ("Clear Chat", self.clear_chat, "#e74c3c"),
            ("Save Chat", self.save_chat, "#27ae60"),
            ("Settings", self.show_settings, "#f39c12"),
            ("Toggle Theme", self.toggle_theme, "#8e44ad")
        ]
        
        self.control_buttons = []
        for text, command, color in controls:
            btn = Button(controls_frame, text=text,
                        font=("Segoe UI", 8, "bold"),
                        bg=color, fg="white",
                        relief=FLAT, cursor="hand2",
                        width=12, pady=3,
                        command=command)
            btn.pack(pady=2)
            self.control_buttons.append(btn)

    def create_features_section(self, parent):
        """Create features section"""
        features_frame = LabelFrame(parent, text="✨ Features", 
                                   font=("Segoe UI", 9, "bold"), bg="white", 
                                   fg="#2c3e50", padx=10, pady=8)
        features_frame.pack(pady=(0, 10))
        
        features = [
            "🤖 AI-Powered Responses",
            "❓ Random Questions",
            "💾 Chat History",
            "🎨 Theme Toggle",
            "📁 Export Chat",
            "⚡ Real-time Typing"
        ]
        
        for feature in features:
            Label(features_frame, text=feature, font=("Segoe UI", 8), 
                  bg="white", fg="#34495e", anchor="w").pack(fill=X, pady=1)

    def create_stats_section(self, parent):
        """Create stats section"""
        stats_frame = LabelFrame(parent, text="📊 Chat Statistics", 
                                font=("Segoe UI", 9, "bold"), bg="white", 
                                fg="#2c3e50", padx=10, pady=8)
        stats_frame.pack(fill=X)
        
        stats_data = [
            ("Messages:", "0"),
            ("AI Responses:", "0"),
            ("Questions Asked:", "0"),
            ("Session:", "Active")
        ]
        
        self.stats_labels = {}
        for category, value in stats_data:
            stat_frame = Frame(stats_frame, bg="white")
            stat_frame.pack(fill=X, pady=1)
            
            Label(stat_frame, text=category, font=("Segoe UI", 8, "bold"), 
                  bg="white", fg="#2980b9", width=12, anchor="w").pack(side=LEFT)
            
            value_label = Label(stat_frame, text=value, font=("Segoe UI", 8), 
                               bg="white", fg="#7f8c8d")
            value_label.pack(side=LEFT, padx=(5, 0))
            
            self.stats_labels[category.replace(":", "")] = value_label

    def send_message(self, event=None):
        """Send user message"""
        message = self.message_entry.get("1.0", "end-1c").strip()
        
        if not message:
            self.show_status_message("Please enter a message!", "error")
            return
        
        # Add user message
        self.add_user_message(message)
        
        # Clear input
        self.message_entry.delete("1.0", END)
        
        # Process response
        self.process_message(message)

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

    def add_bot_message(self, message, msg_type="bot"):
        """Add bot message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=NORMAL)
        
        if msg_type == "ai":
            self.chat_display.insert(END, "AI Bot ", "ai_label")
            tag = "ai_msg"
        else:
            self.chat_display.insert(END, "Bot ", "bot_label")
            tag = "bot_msg"
            
        self.chat_display.insert(END, f"({timestamp})\n", "timestamp")
        self.chat_display.insert(END, f"{message}\n\n", tag)
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)
        
        self.chat_history.append({"type": msg_type, "message": message, "time": timestamp})
        self.update_stats()

    def add_error_message(self, message):
        """Add error message to chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, "Error ", "bot_label")
        self.chat_display.insert(END, f"({timestamp})\n", "timestamp")
        self.chat_display.insert(END, f"{message}\n\n", "error")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def show_typing(self):
        """Show typing indicator"""
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, "🤖 AI is thinking", "typing")
        self.chat_display.insert(END, "...\n", "typing")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def remove_typing(self):
        """Remove typing indicator"""
        self.chat_display.config(state=NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.config(state=DISABLED)

    def process_message(self, message):
        """Process user message and generate response"""
        message_lower = message.lower().strip()
        
        # Check for static responses first
        response_found = False
        for key, response in self.static_responses.items():
            if key in message_lower:
                if response == 'RANDOM_QUESTION':
                    self.ask_random_question()
                else:
                    self.add_bot_message(response)
                response_found = True
                break
        
        if not response_found:
            # Use AI for more complex queries
            self.get_ai_response(message)

    def ask_random_question(self):
        """Ask a random question"""
        question = random.choice(self.random_questions)
        self.add_bot_message(f"Here's a random question for you: {question}")
        
        # Update questions asked counter
        current_count = int(self.stats_labels["Questions Asked"].cget("text"))
        self.stats_labels["Questions Asked"].config(text=str(current_count + 1))

    def get_ai_response(self, user_input):
        """Get response from Gemini AI"""
        if self.API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
            self.add_bot_message("Please configure your Gemini API key to use AI responses. For now, I can answer basic questions!")
            return
        
        # Show typing and disable send button
        self.show_typing()
        self.send_button.config(state='disabled', text='Sending...', bg='#95a5a6')
        
        # Make API call in separate thread
        threading.Thread(target=self._make_api_call, args=(user_input,), daemon=True).start()

    def _make_api_call(self, user_input):
        """Make API call in separate thread"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            
            data = {
                "contents": [{
                    "parts": [{"text": user_input}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            # Remove typing indicator
            self.root.after(0, self.remove_typing)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        answer = candidate['content']['parts'][0]['text']
                        self.root.after(0, lambda: self.add_bot_message(answer, "ai"))
                        
                        # Update AI responses counter
                        current_count = int(self.stats_labels["AI Responses"].cget("text"))
                        self.root.after(0, lambda: self.stats_labels["AI Responses"].config(text=str(current_count + 1)))
                    else:
                        self.root.after(0, lambda: self.add_error_message("Sorry, I couldn't generate a proper response."))
                else:
                    self.root.after(0, lambda: self.add_error_message("Sorry, no response was generated."))
                    
            elif response.status_code == 401:
                self.root.after(0, lambda: self.add_error_message("Invalid API key. Please check your credentials."))
            elif response.status_code == 429:
                self.root.after(0, lambda: self.add_error_message("Rate limit exceeded. Please wait and try again."))
            else:
                self.root.after(0, lambda: self.add_error_message(f"API Error {response.status_code}"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.add_error_message("Request timed out. Please try again."))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.add_error_message("Connection error. Check your internet connection."))
        except Exception as e:
            self.root.after(0, lambda: self.add_error_message(f"Error occurred: {str(e)}"))
        finally:
            # Re-enable send button
            self.root.after(0, lambda: self.send_button.config(state='normal', text='Send\n📤', bg='#3498db'))

    def show_status_message(self, message, msg_type="info"):
        """Show temporary status message"""
        color = {"info": "#3498db", "error": "#e74c3c", "success": "#27ae60"}.get(msg_type, "#3498db")
        
        # Create temporary status label
        status = Label(self.root, text=message, font=("Segoe UI", 9), 
                      bg=color, fg="white", relief=FLAT, pady=5)
        status.pack(side=BOTTOM, fill=X)
        
        # Remove after 3 seconds
        self.root.after(3000, status.destroy)

    def update_stats(self):
        """Update chat statistics"""
        user_msgs = len([msg for msg in self.chat_history if msg["type"] == "user"])
        
        self.stats_labels["Messages"].config(text=str(user_msgs))

    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear Chat", "Clear all chat messages?"):
            self.chat_display.config(state=NORMAL)
            self.chat_display.delete("1.0", END)
            self.chat_display.config(state=DISABLED)
            self.chat_history.clear()
            
            # Reset stats
            for key in self.stats_labels:
                if key != "Session":
                    self.stats_labels[key].config(text="0")
            
            self.add_bot_message("Chat cleared! How can I help you?")

    def save_chat(self):
        """Save chat to file"""
        if not self.chat_history:
            messagebox.showinfo("Save Chat", "No messages to save!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")],
                title="Save Chat History"
            )
            
            if filename:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Enhanced AI Chatbot Conversation\n")
                        f.write(f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 60 + "\n\n")
                        
                        for msg in self.chat_history:
                            sender = {"user": "You", "bot": "Bot", "ai": "AI Bot"}.get(msg["type"], "Unknown")
                            f.write(f"{sender} ({msg['time']}): {msg['message']}\n\n")
                
                messagebox.showinfo("Success", "Chat saved successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def show_settings(self):
        """Show settings dialog"""
        settings_text = """⚙️ Enhanced AI Chatbot Settings

🤖 AI Features:
• Gemini AI Integration: Enabled
• Random Questions: Available
• Smart Responses: Active

🎨 Interface:
• Theme: """ + self.theme.get() + """
• Font: Segoe UI
• Auto-scroll: Enabled

📊 Session Stats:
• Messages: """ + self.stats_labels["Messages"].cget("text") + """
• AI Responses: """ + self.stats_labels["AI Responses"].cget("text") + """
• Questions Asked: """ + self.stats_labels["Questions Asked"].cget("text") + """

💡 Tips:
• Type 'ask me something' for random questions
• Use AI for complex queries
• Save your conversations anytime
"""
        messagebox.showinfo("Settings", settings_text)

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.theme.get() == "Light":
            # Apply dark theme
            self.root.configure(bg="#343541")
            self.chat_display.configure(bg="#343541", fg="white", insertbackground="white")
            self.message_entry.configure(bg="#343541", fg="white", insertbackground="white")
            
            # Update button colors for dark theme
            for btn in self.control_buttons:
                current_bg = btn.cget("bg")
                btn.configure(activebackground="#5d6d7e")
            
            self.theme.set("Dark")
            self.show_status_message("Dark theme activated", "info")
        else:
            # Apply light theme
            self.root.configure(bg="white")
            self.chat_display.configure(bg="#f8f9fa", fg="#2c3e50", insertbackground="black")
            self.message_entry.configure(bg="white", fg="#2c3e50", insertbackground="black")
            
            # Reset button colors for light theme
            for btn in self.control_buttons:
                btn.configure(activebackground="#e0e0e0")
            
            self.theme.set("Light")
            self.show_status_message("Light theme activated", "success")
            

if __name__ == '__main__':
    root = Tk()
    app = EnhancedChatbot(root)
    root.mainloop()