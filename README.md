# ⚡ VectorDSP: High-Performance Signal Processing in Python

**VectorDSP** is a lightweight, high-performance Digital Signal Processing (DSP) framework built entirely on **NumPy**. 

While most academic implementations rely on slow, iterative Python loops and vanilla lists, VectorDSP leverages **vectorized operations** to provide a cleaner API and significantly faster execution for complex signal transformations.

## 🚀 Key Features

- **Vectorized Core:** Every operation—from basic arithmetic to complex transforms—is optimized using NumPy's C-accelerated backends.
- **Pure Math, Zero Fluff:** No heavy dependencies. Just NumPy and pure signal theory.
- **Comprehensive Toolkit:** Includes everything from basic signal manipulation to frequency-domain analysis.

---

## 🛠️ Functional Overview

### 1. Basic Signal Operations
Perform element-wise arithmetic on signals with broadcasting support:
* `add`, `sub`, `multiply`, `inverse`
* `normalize` (Amplitude scaling)
* `const_mult` (Scalar transformations)

### 2. Frequency Domain Analysis
High-fidelity implementations of fundamental transforms:
* **DFT / IDFT:** The theoretical foundation of digital signals.
* **FFT / IFFT:** Optimized Radix-2 implementation for $O(N \log N)$ performance.
* **DC Component Removal:** Zero-centering signals for precise analysis.

### 3. Filters & Systems
* **Convolution & Correlation:** Built-in support for linear systems analysis and pattern matching.
* **Basic Filters:** Intuitive tools for signal smoothing and noise reduction.
