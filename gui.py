import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class AutocompleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CBT Autocomplete Engine")
        self.root.geometry("450x550")
        self.root.configure(bg="#2b2b2b")

        # Check if C++ backend exists
        if not os.path.exists("./autocomplete") and not os.path.exists("autocomplete.exe"):
            messagebox.showerror("Error", "Could not find the compiled 'autocomplete' executable. Please compile the C++ code first!")
            self.root.destroy()
            return

        # Start the C++ Subprocess
        exe_path = "./autocomplete.exe" if os.name == 'nt' else "./autocomplete"
        self.process = subprocess.Popen(
            [exe_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.read_until_prompt() # Consume initial boot text

        # --- GUI Setup ---
        title_label = tk.Label(root, text="🔍 Smart Search", font=("Helvetica", 18, "bold"), bg="#2b2b2b", fg="#ffffff")
        title_label.pack(pady=(20, 10))

        # Search Box
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_type)
        self.entry = tk.Entry(root, textvariable=self.search_var, font=("Helvetica", 14), bg="#3c3f41", fg="#ffffff", insertbackground="white")
        self.entry.pack(fill=tk.X, padx=30, pady=5)
        self.entry.focus()

        # Results Listbox
        self.listbox = tk.Listbox(root, font=("Helvetica", 12), bg="#3c3f41", fg="#ffffff", selectbackground="#4a90e2", highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#2b2b2b")
        btn_frame.pack(pady=(0, 20))

        btn_style = {"font": ("Helvetica", 10, "bold"), "bg": "#4a90e2", "fg": "white", "activebackground": "#357abd", "activeforeground": "white", "relief": "flat", "width": 10}
        
        tk.Button(btn_frame, text="Insert", command=self.insert_word, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Fuzzy", command=self.fuzzy_search, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Save", command=self.save_data, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_word, **btn_style).grid(row=1, column=1, padx=5, pady=5)

    def read_until_prompt(self):
        """Reads output from the C++ program until it hits the '> ' prompt."""
        output = []
        while True:
            char = self.process.stdout.read(1)
            if not char:
                break
            output.append(char)
            if "".join(output[-2:]) == "> ":
                break
        return "".join(output[:-2]).strip()

    def send_command(self, cmd):
        """Sends a command to C++ and returns the response."""
        self.process.stdin.write(cmd + "\n")
        self.process.stdin.flush()
        return self.read_until_prompt()

    def update_listbox(self, results_string):
        self.listbox.delete(0, tk.END)
        if results_string:
            words = results_string.split('\n')
            for word in words:
                if word.strip():
                    self.listbox.insert(tk.END, "  " + word.strip())

    def on_type(self, *args):
        """Triggered every time a key is pressed in the search box."""
        query = self.search_var.get().strip()
        if query:
            results = self.send_command(query)
            self.update_listbox(results)
        else:
            self.listbox.delete(0, tk.END)

    def insert_word(self):
        word = self.search_var.get().strip()
        if word:
            self.send_command(f"insert {word}")
            # CLEAR the box first (which triggers the wipe)
            self.entry.delete(0, tk.END) 
            # THEN post the message
            self.update_listbox(f"✅ '{word}' Inserted!") 

    def delete_word(self):
        word = self.search_var.get().strip()
        if word:
            self.send_command(f"delete {word}")
            # CLEAR the box first
            self.entry.delete(0, tk.END)
            # THEN post the message
            self.update_listbox(f"🗑️ '{word}' Deleted!")

    def fuzzy_search(self):
        word = self.search_var.get().strip()
        if word:
            results = self.send_command(f"fuzzy {word}")
            if results:
                self.update_listbox("--- Did you mean? ---\n" + results)
            else:
                self.update_listbox("❌ No fuzzy matches found.")


    def save_data(self):
        self.send_command("save")
        self.update_listbox("💾 Data saved successfully to 'saved.txt'!")

    def on_closing(self):
        """Closes the C++ backend properly when the Python window closes."""
        try:
            self.send_command("exit")
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutocompleteApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()