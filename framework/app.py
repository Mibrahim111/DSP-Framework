import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from fileHandling import load_signal, save_signal
from operations import (
    add_signals,
    subtract_signals,
    multiply_signal_byConst,
    square_signal,
    accumulate_signal,
    normalize_signal,
    quantization,
    fourier_transform,
    fast_fourier_transform
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
        # tk.Button(root, text="Add", command=self.add).pack(pady=3)
        # tk.Button(root, text="Subtract", command=self.subtract).pack(pady=3)
        tk.Button(root, text="Multiply by Constant", command=self.multiply_const).pack(pady=3)
        tk.Button(root, text="Square", command=self.square).pack(pady=3)
        tk.Button(root, text="Accumulate", command=self.accumulate).pack(pady=3)
        tk.Button(root, text="Quantize Signal", command=self.Quantize).pack(pady=3)
        tk.Label(root, text="Frequency Domain", font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Button(root, text="Apply FFT/IFFT", command=self.apply_fft).pack(pady=5)
        # tk.Button(root, text="Apply DFT/IDFT", command=self.apply_fourier).pack(pady=5)
        tk.Button(root, text="Display Dominant Frequencies", command=self.display_dominant_frequencies).pack(pady=5)
        tk.Button(root, text="Remove DC Component (F(0))", command=self.remove_dc_component).pack(pady=5)
        tk.Button(root, text="Modify Amplitude & Phase", command=self.modify_amplitude_phase).pack(pady=5)

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


    def Quantize(self):             
        if self.signal1 is None:
            messagebox.showerror("Error", "Load a signal first!")
            return

        
        dialog = tk.Toplevel(self.root)
        dialog.title("Quantization Settings")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()  

        choice_var = tk.StringVar(value="levels")

        tk.Label(dialog, text="Select Input Type:", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Radiobutton(dialog, text="Number of Levels", variable=choice_var, value="levels").pack()
        tk.Radiobutton(dialog, text="Number of Bits", variable=choice_var, value="bits").pack()

        tk.Label(dialog, text="Enter Value:").pack(pady=10)
        value_entry = tk.Entry(dialog)
        value_entry.pack()

        def on_confirm():
            choice = choice_var.get()
            try:
                value = int(value_entry.get())
                if value <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a positive integer.")
                return

            levels = 2 ** value if choice == "bits" else value

            if (levels & (levels-1)) != 0:
                messagebox.showerror("Invalid Levels", "Number of levels must be a power of 2 (e.g., 2, 4, 8, 16...).")
                return

            dialog.destroy()

            try:
                # quantization() -> returns (quantized_signal,bits,error,indices)
                assert self.signal1 is not None
                self.signal1, bits, error, indices = quantization(self.signal1, levels)
            except Exception as e:
                messagebox.showerror("Quantization Error", str(e))
                return

            os.makedirs("outputs", exist_ok=True)
            filename = f"outputs/quantized_signal.txt"

            with open(filename, "w") as f:
                f.write(f"Levels: {levels}\n")
                f.write(f"Bits : {len(bits[0]) if bits else 0}\n\n")
                f.write(f"{'Index':>6} {'Encoded':>12} {'Quantized':>12} {'Error':>12}\n")
                for j, b, q, e in zip(indices, bits, self.signal1.y, error):
                    f.write(f"{j:6d} {b:>12} {float(q):12.6f} {float(e):12.6f}\n")

            messagebox.showinfo("Signal Quantized", f"Quantization complete.\nResults saved to: {filename}")
            print(f"Quantization complete. Results saved to: {filename}")

        tk.Button(dialog, text="OK", command=on_confirm).pack(pady=15)


    def apply_fourier(self):
        if self.signal1 is None:
            messagebox.showerror("Error", "Load a signal first!")
            return

        # First, ask for sampling frequency
        fs = simpledialog.askfloat("Sampling Frequency", 
                                "Enter sampling frequency in Hz:",
                                minvalue=0.1, initialvalue=1.0)
        if fs is None:  # User cancelled
            return
        
        if fs <= 0:
            messagebox.showerror("Error", "Sampling frequency must be positive!")
            return

        # Set sampling frequency for the signal
        self.signal1.sample_rate = fs

        # Ask for transform direction
        dialog = tk.Toplevel(self.root)
        dialog.title("Fourier Transform Settings")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        inverse_var = tk.BooleanVar(value=False)
        tk.Label(dialog, text="Select Transform Type:").pack(pady=10)
        tk.Radiobutton(dialog, text="DFT (Forward)", variable=inverse_var, value=False).pack()
        tk.Radiobutton(dialog, text="IDFT (Inverse)", variable=inverse_var, value=True).pack()

        def on_confirm():
            dialog.destroy()
            inverse = inverse_var.get()

            try:
                # Apply Fourier Transform
                assert self.signal1 is not None
                result = fourier_transform(self.signal1, inverse=inverse)
            except Exception as e:
                messagebox.showerror("Error", f"Fourier Transform failed:\n{e}")
                return

            self.signal1 = result

            # Create outputs directory
            os.makedirs("outputs", exist_ok=True)
            
            if not inverse:
                # ===== FORWARD DFT =====
                filename = "outputs/DFT_output.txt"
                
                # Calculate actual frequencies in Hz
                N = len(self.signal1.x)
                frequencies = self.signal1.x * (fs / N)
                
                # Get actual amplitudes and phases
                actual_amplitudes = self.signal1.y
                phases = self.signal1.phase if self.signal1.phase is not None else np.zeros_like(actual_amplitudes)
                
                # Normalize amplitudes to 0-1 range for display
                max_amp = np.max(actual_amplitudes) if np.max(actual_amplitudes) != 0 else 1
                normalized_amplitudes = actual_amplitudes / max_amp
                
                # Save both actual and normalized results
                with open(filename, "w") as f:
                    f.write("DFT Results (Sampling Frequency: {} Hz)\n".format(fs))
                    f.write("="*60 + "\n")
                    f.write("ACTUAL VALUES:\n")
                    f.write("{:>6} {:>20} {:>20}\n".format("Freq(Hz)", "Amplitude", "Phase(rad)"))
                    for i, (freq, amp, ph) in enumerate(zip(frequencies, actual_amplitudes, phases)):
                        f.write("{:8.2f} {:20.10f} {:20.10f}\n".format(freq, float(amp), float(ph)))
                    
                # ===== PLOTTING =====
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                
                # Plot 1: Frequency vs Normalized Amplitude (0-1)
                ax1.plot(frequencies, normalized_amplitudes)
                # ax1.stem(frequencies, normalized_amplitudes, basefmt=" ")
                ax1.set_title("Frequency vs Normalized Amplitude (0-1)")
                ax1.set_xlabel("Frequency (Hz)")
                ax1.set_ylabel("Normalized Amplitude")
                ax1.grid(True)
                
                # Plot 2: Frequency vs Phase
                ax2.plot(frequencies, phases)
                # ax2.stem(frequencies, phases, basefmt=" ")
                ax2.set_title("Frequency vs Phase")
                ax2.set_xlabel("Frequency (Hz)")
                ax2.set_ylabel("Phase (radians)")
                ax2.grid(True)
                
                plt.tight_layout()
                plt.show()
                
                messagebox.showinfo("DFT Complete", 
                                f"Fourier Transform applied successfully!\n"
                                f"Sampling Frequency: {fs} Hz\n"
                                f"Results saved to: {filename}")
                                
            else:
                # ===== INVERSE DFT =====
                filename = "outputs/IDFT_output.txt"
                
                with open(filename, "w") as f:
                    f.write("IDFT Results\n")
                    f.write("="*40 + "\n")
                    f.write("{:>6} {:>20}\n".format("Index", "Amplitude"))
                    for i, y_val in enumerate(self.signal1.y):
                        f.write("{:6d} {:20.10f}\n".format(i, float(y_val)))
                
                # Plot reconstructed signal
                plt.figure(figsize=(10, 4))
                if self.plot_mode.get() == "discrete":
                    plt.stem(self.signal1.x, self.signal1.y, basefmt=" ")
                else:
                    plt.plot(self.signal1.x, self.signal1.y, 'b-o', markersize=3)
                plt.title("Reconstructed Signal (IDFT)")
                plt.xlabel("Sample Index")
                plt.ylabel("Amplitude")
                plt.grid(True)
                plt.show()
                
                messagebox.showinfo("IDFT Complete", 
                                f"Signal reconstructed successfully!\n"
                                f"Results saved to: {filename}")

        tk.Button(dialog, text="OK", command=on_confirm).pack(pady=15)



    from operations import fast_fourier_transform  # make sure you import it at the top


    def apply_fft(self):
        if self.signal1 is None:
            messagebox.showerror("Error", "Load a signal first!")
            return

        fs = simpledialog.askfloat(
            "Sampling Frequency",
            "Enter sampling frequency in Hz:",
            minvalue=0.1,
            initialvalue=1.0
        )
        if fs is None:
            return
        if fs <= 0:
            messagebox.showerror("Error", "Sampling frequency must be positive!")
            return

        self.signal1.sample_rate = fs

        dialog = tk.Toplevel(self.root)
        dialog.title("FFT Settings")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        inverse_var = tk.BooleanVar(value=False)
        tk.Label(dialog, text="Select Transform Type:").pack(pady=10)
        tk.Radiobutton(dialog, text="FFT (Forward)", variable=inverse_var, value=False).pack()
        tk.Radiobutton(dialog, text="IFFT (Inverse)", variable=inverse_var, value=True).pack()

        def on_confirm():
            dialog.destroy()
            inverse = inverse_var.get()

            try:
                assert self.signal1 is not None
                result = fast_fourier_transform(self.signal1, inverse=inverse)
            except Exception as e:
                messagebox.showerror("Error", f"FFT failed:\n{e}")
                return

            self.signal1 = result
            os.makedirs("outputs", exist_ok=True)

            if not inverse:
                # ===== FORWARD FFT =====
                filename = "outputs/FFT_output.txt"
                N = len(self.signal1.x)
                frequencies = self.signal1.x * (fs / N)
                amplitudes = self.signal1.y
                phases = self.signal1.phase if self.signal1.phase is not None else np.zeros_like(amplitudes)

                max_amp = np.max(amplitudes) if np.max(amplitudes) != 0 else 1
                normalized_amplitudes = amplitudes / max_amp

                with open(filename, "w") as f:
                    f.write(f"FFT Results (Sampling Frequency: {fs} Hz)\n")
                    f.write("=" * 60 + "\n")
                    f.write("{:>6} {:>20} {:>20}\n".format("Freq(Hz)", "Amplitude", "Phase(rad)"))
                    for freq, amp, ph in zip(frequencies, amplitudes, phases):
                        f.write(f"{freq:8.2f} {amp:20.10f} {ph:20.10f}\n")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
                ax1.plot(frequencies, normalized_amplitudes)
                ax1.set_title("Frequency vs Normalized Amplitude (FFT)")
                ax1.set_xlabel("Frequency (Hz)")
                ax1.set_ylabel("Normalized Amplitude")
                ax1.grid(True)

                ax2.plot(frequencies, phases)
                ax2.set_title("Frequency vs Phase (FFT)")
                ax2.set_xlabel("Frequency (Hz)")
                ax2.set_ylabel("Phase (radians)")
                ax2.grid(True)

                plt.tight_layout()
                plt.show()

                messagebox.showinfo(
                    "FFT Complete",
                    f"FFT applied successfully!\nResults saved to: {filename}"
                )
            else:
                # ===== INVERSE FFT =====
                filename = "outputs/IFFT_output.txt"
                with open(filename, "w") as f:
                    f.write("IFFT Results\n")
                    f.write("=" * 40 + "\n")
                    f.write("{:>6} {:>20}\n".format("Index", "Amplitude"))
                    for i, y_val in enumerate(self.signal1.y):
                        f.write(f"{i:6d} {y_val:20.10f}\n")

                plt.figure(figsize=(10, 4))
                if self.plot_mode.get() == "discrete":
                    plt.stem(self.signal1.x, self.signal1.y, basefmt=" ")
                else:
                    plt.plot(self.signal1.x, self.signal1.y, 'b-o', markersize=3)
                plt.title("Reconstructed Signal (IFFT)")
                plt.xlabel("Sample Index")
                plt.ylabel("Amplitude")
                plt.grid(True)
                plt.show()

                messagebox.showinfo(
                    "IFFT Complete",
                    f"Signal reconstructed successfully!\nResults saved to: {filename}"
                )

        tk.Button(dialog, text="OK", command=on_confirm).pack(pady=15)


    def generate_new_signal(self):
        """Generates a new signal from a text file containing parameters."""
        path = filedialog.askopenfilename(title="Select Signal Parameters File", filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                from signals import Signal 
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

    def display_dominant_frequencies(self):
        """Display frequencies with amplitude > 0.5 after applying Fourier Transform."""
        if self.signal1 is None:
            messagebox.showerror("Error", "Load and apply Fourier Transform first!")
            return

        if not hasattr(self.signal1, "phase") or self.signal1.phase is None:
            messagebox.showerror("Error", "No Fourier Transform data found. Apply DFT first!")
            return

        try:
            # Sampling frequency should have been stored
            fs = getattr(self.signal1, "sample_rate", 1.0)
            N = len(self.signal1.x)
            frequencies = np.array(self.signal1.x) * (fs / N)
            amplitudes = np.array(self.signal1.y, dtype=float)

            # Normalize amplitudes between 0 and 1
            max_amp = np.max(amplitudes) if np.max(amplitudes) != 0 else 1
            normalized_amplitudes = amplitudes / max_amp

            # Get dominant frequencies
            threshold = 0.5
            dominant_indices = np.where(normalized_amplitudes > threshold)[0]
            dominant_freqs = frequencies[dominant_indices]
            dominant_amps = normalized_amplitudes[dominant_indices]

            if len(dominant_freqs) == 0:
                messagebox.showinfo("Dominant Frequencies", "No frequencies found above 0.5 amplitude.")
                return

            # Plot with highlighted points
            plt.figure(figsize=(10, 5))
            plt.stem(frequencies, normalized_amplitudes, basefmt=" ", label="All Frequencies")
            plt.scatter(dominant_freqs, dominant_amps, color='r', s=80, label="Dominant (>0.5)")
            plt.title("Dominant Frequencies (Amplitude > 0.5)")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Normalized Amplitude")
            plt.grid(True)
            plt.legend()
            plt.show()



        except Exception as e:
            messagebox.showerror("Error", f"Failed to display dominant frequencies:\n{e}")

    def remove_dc_component(self):

        if self.signal1 is None:
            messagebox.showerror("Error", "No signal loaded!")
            return

        if not hasattr(self.signal1, "y") or len(self.signal1.y) == 0:
            messagebox.showerror("Error", "Invalid signal data!")
            return

        try:

            if not hasattr(self.signal1, "phase") or self.signal1.phase is None:
                messagebox.showerror("Error", "Apply Fourier Transform first!")
                return

            # Remove DC component (first frequency component)
            original_dc = self.signal1.y[0]
            self.signal1.y[0] = 0.0
            if hasattr(self.signal1, "phase"):
                self.signal1.phase[0] = 0.0

            messagebox.showinfo("DC Component Removed", f"DC component (F(0)) = {original_dc:.4f} has been removed.")

            # Optional: plot new amplitude spectrum
            fs = getattr(self.signal1, "sample_rate", 1.0)
            N = len(self.signal1.x)
            frequencies = np.array(self.signal1.x) * (fs / N)
            amplitudes = np.array(self.signal1.y, dtype=float)

            max_amp = np.max(amplitudes) if np.max(amplitudes) != 0 else 1
            normalized_amplitudes = amplitudes / max_amp

            plt.figure(figsize=(10, 5))
            plt.stem(frequencies, normalized_amplitudes, basefmt=" ")
            plt.title("Amplitude Spectrum after Removing DC Component")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Normalized Amplitude")
            plt.grid(True)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove DC component:\n{e}")

    def modify_amplitude_phase(self):
        """Open a GUI to view and modify the amplitude and phase of each frequency component."""
        if self.signal1 is None:
            messagebox.showerror("Error", "No signal loaded!")
            return

        if not hasattr(self.signal1, "phase") or self.signal1.phase is None:
            messagebox.showerror("Error", "Apply DFT first before modifying components!")
            return

        try:
            fs = getattr(self.signal1, "sample_rate", 1.0)
            N = len(self.signal1.x)
            frequencies = np.array(self.signal1.x) * (fs / N)
            amplitudes = np.array(self.signal1.y, dtype=float)
            phases = np.array(self.signal1.phase, dtype=float)

            # Create a new window for editing
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Modify Amplitude and Phase")
            edit_window.geometry("600x400")
            edit_window.grab_set()

            # Scrollable frame (in case of many frequencies)
            canvas = tk.Canvas(edit_window)
            scrollbar = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Header
            tk.Label(scroll_frame, text="Freq(Hz)", font=("Arial", 10, "bold"), width=10).grid(row=0, column=0, padx=5,
                                                                                               pady=5)
            tk.Label(scroll_frame, text="Amplitude", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=5,
                                                                                                pady=5)
            tk.Label(scroll_frame, text="Phase (rad)", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2,
                                                                                                  padx=5, pady=5)

            # Entry fields for each frequency
            amp_entries = []
            phase_entries = []

            for i, (freq, amp, ph) in enumerate(zip(frequencies, amplitudes, phases), start=1):
                tk.Label(scroll_frame, text=f"{freq:.2f}", width=10).grid(row=i, column=0, padx=5, pady=2)
                amp_var = tk.StringVar(value=f"{amp:.6f}")
                ph_var = tk.StringVar(value=f"{ph:.6f}")

                amp_entry = tk.Entry(scroll_frame, textvariable=amp_var, width=15)
                ph_entry = tk.Entry(scroll_frame, textvariable=ph_var, width=15)
                amp_entry.grid(row=i, column=1, padx=5, pady=2)
                ph_entry.grid(row=i, column=2, padx=5, pady=2)

                amp_entries.append(amp_var)
                phase_entries.append(ph_var)

            # Apply button
            def apply_changes():
                try:
                    new_amplitudes = [float(a.get()) for a in amp_entries]
                    new_phases = [float(p.get()) for p in phase_entries]

                    # Update the signal data
                    
                    self.signal1.y = new_amplitudes
                    self.signal1.phase = new_phases

                    messagebox.showinfo("Updated", "Amplitude and phase values updated successfully!")

                    # Optional: plot the modified spectrum
                    plt.figure(figsize=(10, 5))
                    plt.stem(frequencies, new_amplitudes, basefmt=" ", label="Modified Amplitude")
                    plt.title("Modified Amplitude Spectrum")
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Amplitude")
                    plt.grid(True)
                    plt.legend()
                    plt.show()

                    edit_window.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric values for all fields.")

            tk.Button(scroll_frame, text="Apply Changes", command=apply_changes, bg="#4CAF50", fg="white").grid(
                row=len(frequencies) + 1, column=0, columnspan=3, pady=10
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to modify components:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DSPGui(root)
    root.mainloop()