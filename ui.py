import tkinter as tk
from tkinter import ttk
from cprog import set_custom_cursor, restore_cursor, default_cursors

class ControlPanel(tk.Frame):
  def __init__(self, master, output_callback):
    super().__init__(master, bg="#05301f", width=150)
    self.output_callback = output_callback
    self.pack_propagate(False)
    self.create_widgets()

  def create_widgets(self):
    actions = {
      "set_curs": lambda: set_custom_cursor(self.output_callback),
      "res_curs": lambda: restore_cursor(self.output_callback),
      "default_curs": lambda: default_cursors(self.output_callback)
    }

    for label, func in actions.items():
      btn = tk.Button(self, text=label, command=func, 
        bg="#1f1575", fg="white", font=("Arial", 10), relief="raised", bd=2)
      btn.pack(pady=10, padx=10, fill="x")

class OutputPanel(tk.Frame):
  def __init__(self, master):
    super().__init__(master, bg="gray")
    self.text_widget = tk.Text(self, wrap="word", font=("Courier", 10))
    self.text_widget.pack(padx=10, pady=10, fill="both", expand=True)
    self.text_widget.config(state="disabled")

  def write_text(self, text):
    self.text_widget.config(state="normal")
    self.text_widget.insert(tk.END, text + "\n")
    self.text_widget.see(tk.END)
    self.text_widget.config(state="disabled")

class MainLable(tk.Frame):
  def __init__(self, master):
    super().__init__(master, bg="white", width=500)
    self.lable = tk.Label(self, text="Sandbox Demo App", font=("Courier", 20, "bold"))
    self.lable.pack(pady=10, padx=40)

class SandboxApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Sandbox Demo App")
    self.geometry("800x600")
    self.configure(bg="white")

    self.top_middle_panel = MainLable(self)
    self.top_middle_panel.pack(side="top", fill="both")

    self.left_panel = ControlPanel(self, self.handle_output)
    self.left_panel.pack(side="left", fill="y")

    self.right_panel = OutputPanel(self)
    self.right_panel.pack(side="right", fill="both", expand=True)

  def say_hello(self):
    self.label.config(text="Hello, you there!")

  def handle_output(self, message):
    self.right_panel.write_text(message)

if __name__ == "__main__":
  app = SandboxApp()
  app.mainloop()
