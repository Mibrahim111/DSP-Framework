import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional ,Iterable
import os


class Signal : 
    """
    Represents a Discrete signal in either time or frequency domain.
    
    Attributes:
        name (str): Name or label of the signal.
        signal_type (int): 0 for time domain, 1 for frequency domain.
        is_periodic (bool): True if signal is periodic.
        sample_rate (Optional[float]): Sampling rate (Hz), if applicable.
        x (np.array): Time samples or frequency bins.
        y (np.array): Amplitude values.
        phase (Optional[np.array]): Phase values (only for frequency domain).
    """

    # using any Iterable and converting it to np.array to avoid future Bugs
    def __init__(self,name: str = "",signal_type:int = 0,is_periodic: bool = False,
                 sample_rate : Optional[float] = None,
                 x : Iterable = np.array([]),
                 y : Iterable = np.array([]),
                 phase : Optional[Iterable] = None):

        self.name = name
        self.signal_type = signal_type  # 0: time, 1: frequency , 2+ : phase or any future case
        self.is_periodic = is_periodic
        self.sample_rate = sample_rate

        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)

        self.phase = np.array(phase, dtype=float) if phase is not None else None        


    def size(self) -> int:
        return len(self.x)          

    # for Debugging Mainly
    def __str__(self):
        domain = "Time Domain" if self.signal_type == 0 else "Frequency Domain"
        periodicity = "Periodic" if self.is_periodic else "Aperiodic"
        size = len(self.x)

        preview_limit = 5
        x_preview = np.array2string(self.x[:preview_limit], precision=3, separator=', ')
        y_preview = np.array2string(self.y[:preview_limit], precision=3, separator=', ')
        phase_preview = (np.array2string(self.phase[:preview_limit], precision=3, separator=', ')
                        if self.phase is not None else "None")

        return (
            f"Signal '{self.name}' [{domain}, {periodicity}]\n"
            f"Sample Rate: {self.sample_rate if self.sample_rate is not None else 'N/A'} Hz\n"
            f"Samples: {size}\n"
            f"x: {x_preview} ...\n"
            f"y: {y_preview} ...\n"
            f"phase: {phase_preview}"
        )
    
    # for Debugging 
    def plot(self):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self.x, self.y)
        plt.title(f"{self.name} ({'Time' if self.signal_type == 0 else 'Frequency'} Domain)")
        plt.xlabel("Time (s)" if self.signal_type == 0 else "Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()


def load_signal(file_path: str) -> Signal:
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    signal_type = int(lines[0])
    is_periodic = bool(int(lines[1]))
    n_samples = int(lines[2])
    data_lines = lines[3:3 + n_samples]

    if signal_type == 0:
        x_vals, y_vals = [], []
        for line in data_lines:
            idx, amp = map(float, line.split())
            x_vals.append(idx)
            y_vals.append(amp)
        return Signal(
            name=os.path.basename(file_path),
            signal_type=0,
            is_periodic=is_periodic,
            x=np.array(x_vals),
            y=np.array(y_vals)
        )

    elif signal_type == 1:
        freq, amp, phase = [], [], []
        for line in data_lines:
            f_val, a_val, p_val = map(float, line.split())
            freq.append(f_val)
            amp.append(a_val)
            phase.append(p_val)
        return Signal(
            name=os.path.basename(file_path),
            signal_type=1,
            is_periodic=is_periodic,
            x=np.array(freq),
            y=np.array(amp),
            phase=np.array(phase)
        )

    else:
        raise ValueError(f"Unsupported signal type: {signal_type}")


def save_signal(signal: Signal, file_path: str):
    
    with open(file_path, 'w') as f:
        f.write(f"{signal.signal_type}\n")
        f.write(f"{int(signal.is_periodic)}\n")
        f.write(f"{len(signal.x)}\n")
        
        if signal.signal_type == 0:
            for xi, yi in zip(signal.x, signal.y):
                f.write(f"{xi}\t{yi}\n")
        
        elif signal.signal_type == 1:
            if getattr(signal, "phase", None) is None:
                raise ValueError("Frequency-domain signal must have a 'phase' attribute.")
            _phase: np.ndarray = np.asarray(signal.phase)
            for fi, ai, pi in zip(signal.x, signal.y,_phase):
                f.write(f"{fi}\t{ai}\t{pi}\n")
        else:
            raise ValueError(f"Unsupported signal type: {signal.signal_type}")
    
    print(f"Signal saved successfully to '{os.path.basename(file_path)}'")
