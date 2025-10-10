import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from fileHandling import load_signal, save_signal
from operations import (
    add_signals,
    subtract_signals,
    multiply_signal_byConst,
    square_signal,
    accumulate_signal,
    normalize_signal
)
from signals import (Signal,generate_signal,read_gen_file)

class DSPGui:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Signal Processor")
        self.root.geometry("460x520")
        self.signal1 = None
        self.signal2 = None
        self.plot_mode = tk.StringVar(value="discrete")
        self.normalize_mode = tk.StringVar(value="0to1")  # default normalize range

        tk.Button(root, text="Load Signal 1", command=self.load_signal1).pack(pady=5)
        tk.Button(root, text="Load Signal 2", command=self.load_signal2).pack(pady=5)
        tk.Button(root, text="Save Current Signal", command=self.save_signal).pack(pady=5)
        tk.Button(root, text="Generate Signal from File", command=self.generate_new_signal).pack(pady=5)

        tk.Label(root, text="Operations", font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Button(root, text="Add", command=self.add).pack(pady=3)
        tk.Button(root, text="Subtract", command=self.subtract).pack(pady=3)
        tk.Button(root, text="Multiply by Constant", command=self.multiply_const).pack(pady=3)
        tk.Button(root, text="Square", command=self.square).pack(pady=3)
        tk.Button(root, text="Accumulate", command=self.accumulate).pack(pady=3)

        tk.Label(root, text="Normalization Range", font=('Arial', 12, 'bold')).pack(pady=10)
        norm_frame = tk.Frame(root)
        norm_frame.pack()
        tk.Radiobutton(norm_frame, text="[-1, 1]", variable=self.normalize_mode, value="-1to1").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(norm_frame, text="[0, 1]", variable=self.normalize_mode, value="0to1").pack(side=tk.LEFT, padx=10)
        tk.Button(root, text="Normalize", command=self.normalize).pack(pady=5)

        tk.Label(root, text="Plot Mode", font=('Arial', 12, 'bold')).pack(pady=10)
        plot_frame = tk.Frame(root)
        plot_frame.pack()
        tk.Radiobutton(plot_frame, text="Discrete", variable=self.plot_mode, value="discrete").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(plot_frame, text="Continuous", variable=self.plot_mode, value="continuous").pack(side=tk.LEFT, padx=10)

        tk.Button(root, text="Plot Signals", command=self.plot_signals).pack(pady=10)

    # ===== File Handlers =====
    def load_signal1(self):
        path = filedialog.askopenfilename(title="Select Signal 1 File")
        if path:
            try:
                self.signal1 = load_signal(path)
                messagebox.showinfo("Loaded", f"Loaded Signal 1 from {path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_signal2(self):
        path = filedialog.askopenfilename(title="Select Signal 2 File")
        if path:
            try:
                self.signal2 = load_signal(path)
                messagebox.showinfo("Loaded", f"Loaded Signal 2 from {path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_signal(self):
        if self.signal1 is None:
            messagebox.showerror("Error", "No signal to save!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            try:
                save_signal(self.signal1, path)
                messagebox.showinfo("Saved", f"Signal saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ===== Operations =====
    def add(self):
        if self.signal1 and self.signal2:
            self.signal1 = add_signals(self.signal1, self.signal2)
            messagebox.showinfo("Result", "Signals added successfully.")
        else:
            messagebox.showerror("Error", "Load both signals first!")

    def subtract(self):
        if self.signal1 and self.signal2:
            self.signal1 = subtract_signals(self.signal1, self.signal2)
            messagebox.showinfo("Result", "Signals subtracted successfully.")
        else:
            messagebox.showerror("Error", "Load both signals first!")

    def multiply_const(self):
        if self.signal1 is None:
            messagebox.showerror("Error", "Load a signal first!")
            return
        c = simpledialog.askfloat("Multiply by Constant", "Enter constant:")
        if c is not None:
            self.signal1 = multiply_signal_byConst(self.signal1, c)
            messagebox.showinfo("Result", f"Signal multiplied by {c}")

    def square(self):
        if self.signal1:
            self.signal1 = square_signal(self.signal1)
            messagebox.showinfo("Result", "Signal squared successfully.")
        else:
            messagebox.showerror("Error", "Load a signal first!")

    def accumulate(self):
        if self.signal1:
            self.signal1 = accumulate_signal(self.signal1)
            messagebox.showinfo("Result", "Signal accumulated successfully.")
        else:
            messagebox.showerror("Error", "Load a signal first!")

    def normalize(self):
        if self.signal1:
            mode = self.normalize_mode.get()
            if mode == "-1to1" :
                mode = "-1_to_1"
            else :
                mode = "0_to_1"

            self.signal1 = normalize_signal(self.signal1, mode=mode)
            label = "[-1, 1]" if mode == "-1_to_1" else "[0, 1]"
            messagebox.showinfo("Result", f"Signal normalized to {label}.")
        else:
            messagebox.showerror("Error", "Load a signal first!")

    def generate_new_signal(self):
        """Generates a new signal from a text file containing parameters."""
        path = filedialog.askopenfilename(title="Select Signal Parameters File", filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                from signals import Signal  # ensure class is available
                self.signal1 = generate_signal(path)
                messagebox.showinfo("Generated", f"Signal generated successfully from {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate signal: {e}")

    def save_gen_signal(self):
        if self.signal1 is None:
            messagebox.showerror("Error", "No signal to save!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            try:
                save_signal(self.signal1, path)
                messagebox.showinfo("Saved", f"Signal saved to {path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    # ===== Plotting =====
    def plot_signals(self):
        if not self.signal1:
            messagebox.showerror("Error", "Load at least one signal!")
            return

        plt.figure(figsize=(8, 4))
        mode = self.plot_mode.get()

        if mode == "discrete":
            plt.stem(self.signal1.x, self.signal1.y, basefmt=" ", label="Signal 1")
            if self.signal2:
                plt.stem(self.signal2.x, self.signal2.y, linefmt='r--', markerfmt='ro', basefmt=" ", label="Signal 2")
        else:
            plt.plot(self.signal1.x, self.signal1.y, label="Signal 1")
            if self.signal2:
                plt.plot(self.signal2.x, self.signal2.y, label="Signal 2", linestyle='--')

        plt.xlabel("Samples" if mode == "discrete" else "Time")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.title(f"{mode.capitalize()} Signal Plot")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = DSPGui(root)
    root.mainloop()