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

# Not Sure of the Validity of this function and if there's a better way
# Complexity -> O(N^2)
def validate_is_periodic(signal : Signal, eps=1e-6):
    N = signal.size()
    
    for p in range(1, N//2 + 1):
        flag = True
        for i in range(N - p):
            if abs(signal.y[i] - signal.y[i + p]) > eps:
                flag = False
                break
        if flag:
            return True
    
    return False

def generate_signal(file_path: str) -> Signal:
    params = read_gen_file(file_path)
    
    sig_type = params.get("type")
    A = params.get("A")
    F = params.get("AnalogFrequency",1.0)
    Fs = params.get("SamplingFrequency",2*F)
    theta = params.get("PhaseShift")

    if Fs < 2*F:
        raise ValueError(f"Sampling frequency {Fs} Hz is below Nyquist rate for F={F} Hz")

    t = np.arange(0, 1, 1/Fs)  
    if sig_type == "sin":
        y = A * np.sin(2 * np.pi * F * t + theta)
        name = f"Sine_{F}Hz"
    elif sig_type == "cos":
        y = A * np.cos(2 * np.pi * F * t + theta)
        name = f"Cosine_{F}Hz"
    else:
        raise ValueError(f"Unknown signal type '{sig_type}'")

    ret = Signal(name=name, signal_type=0, is_periodic=False, sample_rate=Fs, x=t, y=y)
    return ret


def read_gen_file(file_path: str) -> dict:
    """Reads parameters from a .txt file for sine/cosine generation."""
    params = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key in ['A', 'AnalogFrequency' , 'SamplingFrequency', 'PhaseShift']:
                params[key] = float(value)
            else:
                params[key] = value.lower() 
    return params
