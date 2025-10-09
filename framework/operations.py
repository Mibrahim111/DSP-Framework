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
    y_new = sig1.y - sig2.y
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


# def normalize_signal(sig: Signal, mode: str = "-1_to_1") -> Signal:
#     """
#     Normalize signal amplitudes:
#     mode = "-1_to_1" → scale between -1 and 1
#     mode = "0_to_1"  → scale between 0 and 1
#     """
#     y = sig.y
#     y_min, y_max = np.min(y), np.max(y)
#     if y_max == y_min:
#         raise ValueError("Cannot normalize a constant signal.")

#     if mode == "-1_to_1":
#         y_new = 2 * (y - y_min) / (y_max - y_min) - 1
#     elif mode == "0_to_1":
#         y_new = (y - y_min) / (y_max - y_min)
#     else:
#         raise ValueError("Invalid mode. Use '-1_to_1' or '0_to_1'.")

#     return Signal(
#         name=sig.name + "Normalized",
#         signal_type=sig.signal_type,
#         is_periodic=sig.is_periodic,
#         x=sig.x,
#         y=y_new
#     )


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