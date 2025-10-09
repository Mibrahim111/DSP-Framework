#!/usr/bin/env python3
# DSPFramework.py
# Single-window Tkinter DSP framework
# Features:
# - Load signal files (the text format used in the Task1Test)
# - Display discrete (stem) and continuous (line) representations
# - Display two signals at the same time
# - Add any number of signals, multiply a signal by a constant
# - Save results in same format expected by the test script

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import os
# ---------------------
# File parsing / writing (matches the ReadSignalFile in the test)
# ---------------------
def read_signal_file(file_name):
    """Read signal file with the same structure as the test files.
    Skips first 4 lines (as in Task1Test.ReadSignalFile) and then reads lines with 'index value'.
    Returns (indices:list[int], samples:list[float])
    """
    indices = []
    samples = []
    with open(file_name, 'r') as f:
        # read up to 4 header lines (safe even if file shorter)
        for _ in range(4):
            line = f.readline()
            if not line:
                break
        while True:
            line = f.readline()
            if not line:
                break
            L = line.strip()
            if len(L.split()) == 2:
                a, b = L.split()
                try:
                    ia = int(a)
                except:
                    # if can't parse, skip
                    continue
                try:
                    vb = float(b)
                except:
                    vb = float(b.replace(',', '.'))
                indices.append(ia)
                samples.append(vb)
            else:
                break
    return indices, samples

def write_signal_file(file_name, indices, samples):
    """Write output in the same format as the provided files:
    First lines: 0\n0\n{N}\n  then lines 'index sample '
    This matches the test ReadSignalFile (skips 4 header lines then expects 'index value').
    """
    N = len(samples)
    with open(file_name, 'w') as f:
        # Use the same pattern observed in provided files
        f.write("0\n")
        f.write("0\n")
        f.write(f"{N}\n")
        for i, s in zip(indices, samples):
            # follow spacing like '0 0 ' (space separated)
            f.write(f"{i} {s} \n")

# ---------------------
# Signal object to keep things neat
# ---------------------
class Signal:
    def __init__(self, name, indices, samples, filepath=None):
        self.name = name
        self.indices = list(indices)
        self.samples = list(samples)
        self.filepath = filepath

    def copy(self):
        return Signal(self.name + "_copy", self.indices[:], self.samples[:], self.filepath)

# ---------------------
# GUI
# ---------------------
class DSPApp:
    def __init__(self, root):
        self.root = root
        root.title("DSP Framework")
        self.signals = []  # list of Signal

        # --- Top frame: buttons and listbox ---
        top = tk.Frame(root, padx=6, pady=6)
        top.pack(side=tk.TOP, fill=tk.X)

        btn_load = tk.Button(top, text="Load Signal(s)", command=self.load_signals)
        btn_load.grid(row=0, column=0, padx=4, pady=4)

        btn_plot = tk.Button(top, text="Plot Selected", command=self.plot_selected)
        btn_plot.grid(row=0, column=1, padx=4, pady=4)

        btn_plot_two = tk.Button(top, text="Plot Two Signals", command=self.plot_two_signals)
        btn_plot_two.grid(row=0, column=2, padx=4, pady=4)

        btn_add = tk.Button(top, text="Add Selected Signals", command=self.add_selected_signals)
        btn_add.grid(row=0, column=3, padx=4, pady=4)

        btn_mult = tk.Button(top, text="Multiply Selected by Const", command=self.multiply_selected_signal)
        btn_mult.grid(row=0, column=4, padx=4, pady=4)

        btn_save = tk.Button(top, text="Save Selected As...", command=self.save_selected)
        btn_save.grid(row=0, column=5, padx=4, pady=4)

        # Left: listbox of loaded signals
        left = tk.Frame(root, padx=6, pady=6)
        left.pack(side=tk.LEFT, fill=tk.Y)

        l = tk.Label(left, text="Loaded Signals (Ctrl+click to multi-select):")
        l.pack(anchor="w")

        self.listbox = tk.Listbox(left, selectmode=tk.EXTENDED, width=36)
        self.listbox.pack(fill=tk.Y, expand=False)

        # Right: plot area
        right = tk.Frame(root, padx=6, pady=6)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Radio button for plot type
        self.plot_type = tk.StringVar(value="discrete")
        rb1 = tk.Radiobutton(right, text="Discrete (stem)", variable=self.plot_type, value="discrete")
        rb2 = tk.Radiobutton(right, text="Continuous (line)", variable=self.plot_type, value="continuous")
        rb1.pack(anchor="nw")
        rb2.pack(anchor="nw")

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7,5))
        self.ax.set_title("Signal Plot")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status = tk.StringVar(value="No signals loaded.")
        status_bar = tk.Label(root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------------------
    # GUI actions
    # ---------------------
    def load_signals(self):
        files = filedialog.askopenfilenames(title="Select signal file(s)", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not files:
            return
        for filepath in files:
            try:
                indices, samples = read_signal_file(filepath)
                base = os.path.basename(filepath)
                if len(indices) == 0:
                    messagebox.showwarning("Warning", f"No samples found in {base}. Skipping.")
                    continue
                sig = Signal(base, indices, samples, filepath)
                self.signals.append(sig)
                self.listbox.insert(tk.END, sig.name)
                self.status.set(f"Loaded {len(self.signals)} signal(s).")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read {filepath}:\n{e}")

    def get_selected_signals(self):
        sel = self.listbox.curselection()
        if not sel:
            return []
        return [self.signals[i] for i in sel]

    def plot_selected(self):
        sels = self.get_selected_signals()
        if len(sels) == 0:
            messagebox.showinfo("Plot", "Select one signal to plot.")
            return
        # plot first selected only
        sig = sels[0]
        self._plot_signals([sig])

    def plot_two_signals(self):
        sels = self.get_selected_signals()
        if len(sels) < 2:
            messagebox.showinfo("Plot Two", "Select at least two signals (Ctrl+click) to plot together.")
            return
        self._plot_signals(sels[:2])

    def add_selected_signals(self):
        sels = self.get_selected_signals()
        if len(sels) < 2:
            messagebox.showinfo("Add Signals", "Select two or more signals to add (Ctrl+click).")
            return
        try:
            result = self.add_signals(sels)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add signals:\n{e}")
            return
        # show result in plot
        self._plot_signals([result])
        # ask to save
        save = messagebox.askyesno("Save", "Save the addition result to file now?")
        if save:
            self._ask_and_save_signal(result)

    def multiply_selected_signal(self):
        sels = self.get_selected_signals()
        if len(sels) != 1:
            messagebox.showinfo("Multiply", "Select exactly one signal to multiply.")
            return
        sig = sels[0]
        # ask constant
        val = simpledialog.askfloat("Multiply", f"Enter multiplication constant for '{sig.name}':", initialvalue=1.0)
        if val is None:
            return
        result = self.multiply_signal(sig, val)
        self._plot_signals([result])
        save = messagebox.askyesno("Save", "Save the multiplication result to file now?")
        if save:
            self._ask_and_save_signal(result)

    def save_selected(self):
        sels = self.get_selected_signals()
        if len(sels) != 1:
            messagebox.showinfo("Save", "Select exactly one signal to save.")
            return
        sig = sels[0]
        self._ask_and_save_signal(sig)

    # ---------------------
    # Signal operations
    # ---------------------
    def add_signals(self, signal_list):
        """Add any number of signals. Returns a new Signal.
        Strategy:
        - We'll align by indices. If signals share identical index arrays, simple elementwise add.
        - If indices differ, produce result indices = union(min..max) (integer indices) and fill missing with 0.
        """
        # determine global index range as integer min..max
        mins = [min(s.indices) for s in signal_list]
        maxs = [max(s.indices) for s in signal_list]
        global_min = min(mins)
        global_max = max(maxs)
        # assume integer indices increasing by 1 typically; construct full integer grid
        indices = list(range(global_min, global_max + 1))
        # compute value for each signal at each index (0 if missing)
        accum = [0.0] * len(indices)
        idx_to_pos = {i: pos for pos, i in enumerate(indices)}
        for s in signal_list:
            for i, val in zip(s.indices, s.samples):
                if i in idx_to_pos:
                    accum[idx_to_pos[i]] += val
        name = " + ".join([s.name for s in signal_list])
        return Signal("add(" + name + ")", indices, accum)

    def multiply_signal(self, sig, const):
        indices = sig.indices[:]
        samples = [float(x) * float(const) for x in sig.samples]
        name = f"mul({sig.name},{const})"
        return Signal(name, indices, samples)

    # ---------------------
    # Plotting helper
    # ---------------------
    def _plot_signals(self, sigs):
        self.ax.cla()
        self.ax.set_title("Signal Plot")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Amplitude")
        plot_type = self.plot_type.get()
        colors = ['C0', 'C1', 'C2', 'C3']
        for k, sig in enumerate(sigs):
            x = np.array(sig.indices)
            y = np.array(sig.samples, dtype=float)
            col = colors[k % len(colors)]
            if plot_type == "discrete":
                # use stem
                
                try:
                  # For older matplotlib versions (<3.6)
                    markerline, stemlines, baseline = self.ax.stem(x, y, label=sig.name, use_line_collection=True)
                except TypeError:
                # For newer versions (>=3.6)
                    markerline, stemlines, baseline = self.ax.stem(x, y, label=sig.name)

                plt.setp(markerline, marker='o', markersize=4)
                plt.setp(stemlines, linewidth=1)
            else:
                # continuous: plot line connecting samples; if indices are not contiguous, still connect
                self.ax.plot(x, y, label=sig.name, linewidth=1.5)
                # optionally scatter
                self.ax.scatter(x, y, s=6)
        self.ax.legend(loc='upper left', fontsize='small')
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.canvas.draw()
        self.status.set(f"Plotted {len(sigs)} signal(s).")

    # ---------------------
    # Save helper
    # ---------------------
    def _ask_and_save_signal(self, sig):
        fname = filedialog.asksaveasfilename(title="Save signal as...", defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not fname:
            return
        try:
            write_signal_file(fname, sig.indices, sig.samples)
            messagebox.showinfo("Saved", f"Saved signal to:\n{fname}")
            self.status.set(f"Saved {os.path.basename(fname)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

# ---------------------
# Run the app
# ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DSPApp(root)
    root.geometry("1000x650")
    root.mainloop()
