"""
    Operations on signals :
    

    Add 2 or more signals
    
    Multiply by constant

    subtract two signals

    Accumlation of signals

    Squaring of signals

    Normalization of signals
    

"""
from signals import Signal
import numpy as np

# internal validation function 

def _validate_signals(sig1: Signal, sig2: Signal):
    """Ensure both signals are compatible for operations."""
    if sig1.size() != sig2.size():
        raise ValueError("Signals must have the same number of samples.")
    if not np.allclose(sig1.x, sig2.x):
        raise ValueError("Signals must have identical x (time/frequency) values.")
    if sig1.signal_type != sig2.signal_type:
        raise ValueError("Signals must be in the same domain (time/frequency).")


def add_signals(*signals: Signal, name: str = "Added Signal") -> Signal:
    """Add two or more signals sample-by-sample."""
    if len(signals) < 2:
        raise ValueError("At least two signals are required for addition.")

    ref = signals[0] # reference for Validating the rest of the tuple
    for s in signals[1:]:
        _validate_signals(ref, s)

    y_sum = np.sum([s.y for s in signals], axis=0)

    return Signal(
        name=name,
        signal_type=ref.signal_type,
        is_periodic=any(s.is_periodic for s in signals),
        x=ref.x,
        y=y_sum
    )

def subtract_signals(sig1: Signal, sig2: Signal, name: str = "Subtracted Signal") -> Signal:
    """Subtract sig2 from sig1."""
    _validate_signals(sig1, sig2)
    y_new = abs(sig1.y - sig2.y)
    return Signal(
        name=name,
        signal_type=sig1.signal_type,
        is_periodic=sig1.is_periodic or sig2.is_periodic,
        x=sig1.x,
        y=y_new
    )


def multiply_signal_byConst(sig : Signal, const : float = 1.0, name :str = "Multiplied Signal") -> Signal:
    """Multiply signal amplitude by a constant."""
    return Signal(
        name=name,
        signal_type=sig.signal_type,
        is_periodic=sig.is_periodic,
        x=sig.x,
        y=sig.y * const
        )


def normalize_signal(sig: Signal, mode: str = "-1_to_1") -> Signal:
    """
    Normalize signal amplitudes:
    mode = "-1_to_1" → scale between -1 and 1
    mode = "0_to_1"  → scale between 0 and 1
    """
    y = sig.y
    y_min, y_max = np.min(y), np.max(y)
    if y_max == y_min:
        raise ValueError("Cannot normalize a constant signal.")

    if mode == "-1_to_1":
        y_new = 2 * (y - y_min) / (y_max - y_min) - 1
    elif mode == "0_to_1":
        y_new = (y - y_min) / (y_max - y_min)
    else:
        raise ValueError("Invalid mode. Use '-1_to_1' or '0_to_1'.")

    return Signal(
        name=sig.name + "Normalized",
        signal_type=sig.signal_type,
        is_periodic=sig.is_periodic,
        x=sig.x,
        y=y_new
    )


def square_signal(sig: Signal, name: str = "Squared Signal") -> Signal:
    """Return a signal whose y values are squared."""
    return Signal(
        name=name,
        signal_type=sig.signal_type,
        is_periodic=sig.is_periodic,
        x=sig.x,
        y=np.square(sig.y)
    )


def accumulate_signal(sig: Signal, name: str = "Acc Signal") -> Signal:
    """Return cumulative sum of signal samples."""
    return Signal(
        name=name,
        signal_type=sig.signal_type,
        is_periodic=sig.is_periodic,
        x=sig.x,
        y=np.cumsum(sig.y)
    )


def quantization(sig: Signal, levels: int, name: str = "Quantized Signal"):
    """Quantize samples in sig.y into levels.
    Returns: (quantized_signal, encoded, error, indices)
    """
    if levels <= 1:
        raise ValueError("levels must be > 1")

    y = np.array(sig.y, dtype=float)
    x = np.array(sig.x) if hasattr(sig, "x") else np.arange(len(y))

    y_min, y_max = np.min(y), np.max(y)
    delta = (y_max - y_min) / levels

    if delta == 0:
        q_midpoints = np.full_like(y, y_min)
        indices = np.zeros_like(y, dtype=int)
    else:
        indices = np.floor((y - y_min) / delta).astype(int)
        indices = np.clip(indices, 0, levels - 1)
        q_midpoints = y_min + delta * (indices + 0.5)

    error = q_midpoints - y
    n_bits = int(np.ceil(np.log2(levels)))
    encoded = [format(int(i), f'0{n_bits}b') for i in indices]
    

    quantized_signal = Signal(
        name=name,
        signal_type=sig.signal_type,
        is_periodic=getattr(sig, "is_periodic", False),
        x=x.tolist(),
        y=q_midpoints.tolist()
    )
    indices +=1 #to be 1-based

    return quantized_signal, encoded, error,indices


def fourier_transform(sig: Signal, inverse: bool = False, name: str = "Fourier Transform") -> Signal:
    """
    Computes the DFT or IDFT of a discrete signal.

    Args:
        sig (Signal): Input signal (time domain for DFT, frequency domain for IDFT).
        inverse (bool): False for DFT, True for IDFT.
        name (str): Name of the resulting signal.

    Returns:
        Signal: Frequency-domain (for DFT) or time-domain (for IDFT) signal.
    """
    if sig is None or sig.y is None:
        raise ValueError("Invalid signal input for Fourier transform.")
    
    y = np.array(sig.y, dtype=complex)
    N = len(y)
    
    if inverse:
        if sig.phase is not None:
            complex_vals = sig.y * np.exp(1j * sig.phase)
        else:
            complex_vals = y
        
        n = np.arange(N)
        k = n.reshape((N, 1))
        
        exponent = 2j * np.pi * k * n / N
        transform = np.dot(np.exp(exponent), complex_vals) / N
        
        time_samples = np.arange(N)
        return Signal(
            name=name,
            signal_type=0,   # time domain
            is_periodic=sig.is_periodic,
            sample_rate=sig.sample_rate,
            x=time_samples,
            y=np.real(transform)  # remove j
        )
    else:
        n = np.arange(N)
        k = n.reshape((N, 1))
        
        exponent = -2j * np.pi * k * n / N
        transform = np.dot(np.exp(exponent), y)
        
        # Calculate amplitude and phase
        amplitude = np.abs(transform)
        phase = np.angle(transform)
        
        IDX = np.arange(N)
        
        return Signal(
            name=name,
            signal_type=1,   # frequency domain Important
            is_periodic=False,
            sample_rate=sig.sample_rate,
            x=IDX,
            y=amplitude, 
            phase=phase
        )