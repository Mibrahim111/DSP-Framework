import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from framework.signals import (
    generate_signal,
)
from framework.operations import (
    subtract_signals,
    normalize_signal
)
from tests.Task2Test import (
    SinCosSignalSamplesAreEqual,
    SubSignalSamplesAreEqual,
    NormalizeSignal,
    SignalSamplesAreEqual,
    ReadSignalFile
)

sig1 = generate_signal("/home/mohammed/repos/dsp/sin_cos/inputs.txt")
SinCosSignalSamplesAreEqual("sine","/home/mohammed/repos/dsp/sin_cos/SinOutput.txt",sig1.x,sig1.y)

sig2 = generate_signal("/home/mohammed/repos/dsp/sin_cos/cos.txt")
SinCosSignalSamplesAreEqual("cos","/home/mohammed/repos/dsp/sin_cos/CosOutput.txt",sig2.x,sig2.y)
