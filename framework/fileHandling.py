import os
from signals import Signal
import numpy as np

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
