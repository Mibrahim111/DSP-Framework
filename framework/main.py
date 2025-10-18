import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from framework.signals import (
    generate_signal
)
from framework.fileHandling import load_signal
from framework.operations import (
    subtract_signals,
    normalize_signal,
    quantization
)
from tests.QuanTest1 import QuantizationTest1
from tests.QuanTest2 import QuantizationTest2

sig = load_signal("/home/mohammed/repos/dsp/Inputs/Quan1_input.txt")
q,enc,error,ind = quantization(sig,8)


QuantizationTest1("/home/mohammed/repos/dsp/outputs/Quan1_Out.txt",enc,q.y)



sig2 = load_signal("/home/mohammed/repos/dsp/Inputs/Quan2_input.txt")
q2,enc2,error2,ind2 = quantization(sig2,4)

QuantizationTest2("/home/mohammed/repos/dsp/outputs/Quan2_Out.txt",ind2,enc2,q2.y,error2)
