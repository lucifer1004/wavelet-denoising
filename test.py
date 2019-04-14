import numpy as np
import matplotlib.pyplot as plt
from utils.denoising import get_baseline, translation_invariant_denoise

if __name__ == "__main__":
    ecg = np.arange(0, 200, 0.1)
    ecg += np.random.normal(0, 5, 2000)
    denoised = translation_invariant_denoise(ecg, method='heursure', mode='soft', wavelets_name='sym5', level=5)
    print(denoised)
    baseline = get_baseline(data=ecg, wavelets_name="sym5", level=5)
    print(baseline)
