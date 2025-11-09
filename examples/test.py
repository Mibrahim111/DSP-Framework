import sys, os
from docx import Document 
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from framework.signals import (
    generate_signal,
    Signal
)
from framework.fileHandling import load_signal,save_signal
from framework.operations import (
    subtract_signals,
    normalize_signal,
    quantization,
    fourier_transform,
    remove_dc_component
)
from tests.signalcompare import (
    SignalComapreAmplitude,
    SignalComaprePhaseShift
)
from tests.CompareSignals import (
    SignalsAreEqual
)
