import os
import matplotlib.pyplot as plt
from framework.signals import Signal
from framework.signals import generate_signal
from tests.Task1Test import *
from tests.Task2Test import *

def list_gen_files(folder="."):
    """List all signal generation parameter files (.txt)."""
    return [f for f in os.listdir(folder) if f.endswith(".txt")]


def main():
    AddSignalSamplesAreEqual() # signal1 , signal2 , np.array = x , np.array = y 


if __name__ == "__main__":
    main()
