import pywt
import math
import numpy as np
from .sequence import right_shift, back_shift
from .threshold import heur_sure, visu_shrink, sure_shrink, min_max
from .utils import closest_two_power, get_var


# 获取近似基线
def baseline(data, wavelets_name='sym8', level=5):
    """
    :param data: signal
    :param wavelets_name: wavelets name in PyWavelets, 'sym8' as default
    :param level: deconstruct level, 5 as default
    :return: baseline signal
    """
    # 创建小波对象
    wave = pywt.Wavelet(wavelets_name)
    # 分解
    coeffs = pywt.wavedec(data, wave, level=level)
    # 除最高频外小波系数置零
    for i in range(1, len(coeffs)):
        coeffs[i] *= 0
    # 重构
    baseline = pywt.waverec(coeffs, wave)
    return baseline


# 阈值收缩去噪法
def dwt(data, method='sureshrink', mode='soft', wavelets_name='sym8', level=5):
    """
    :param data: signal
    :param method: {'visushrink', 'sureshrink', 'heursure', 'minmax'}, 'sureshrink' as default
    :param mode: {'soft', 'hard', 'garotte', 'greater', 'less'}, 'soft' as default
    :param wavelets_name: wavelets name in PyWavelets, 'sym8' as default
    :param level: deconstruct level, 5 as default
    :return: processed data
    """

    methods_dict = {
        'visushrink': visu_shrink,
        'sureshrink': sure_shrink,
        'heursure': heur_sure,
        'minmax': min_max
    }

    # 创建小波对象
    wave = pywt.Wavelet(wavelets_name)

    # 分解 阈值处理
    data_ = data[:]

    (cA, cD) = pywt.dwt(data=data_, wavelet=wave)
    var = get_var(cD)

    coeffs = pywt.wavedec(data=data, wavelet=wavelets_name, level=level)

    for idx, coeff in enumerate(coeffs):
        if idx == 0:
            continue
        # 求阈值thre
        thre = methods_dict[method](var, coeff)
        # 处理cD
        coeffs[idx] = pywt.threshold(coeffs[idx], thre, mode=mode)

    # 重构信号
    thresholded_data = pywt.waverec(coeffs, wavelet=wavelets_name)

    return thresholded_data


# 小波平移不变消噪
def ti(data, step=100, method='heursure', mode='soft', wavelets_name='sym5', level=5):
    """
    :param data: signal
    :param step: shift step, 100 as default
    :param method: {'visushrink', 'sureshrink', 'heursure', 'minmax'}, 'heursure' as default
    :param mode: {'soft', 'hard', 'garotte', 'greater', 'less'}, 'soft' as default
    :param wavelets_name: wavelets name in PyWavelets, 'sym5' as default
    :param level: deconstruct level, 5 as default
    :return: processed data
    """
    # 循环平移
    num = math.ceil(len(data) / step)
    final_data = [0] * len(data)
    for i in range(num):
        temp_data = right_shift(data, i * step)
        temp_data = dwt(
            temp_data, method=method, mode=mode, wavelets_name=wavelets_name, level=level)
        temp_data = temp_data.tolist()
        temp_data = back_shift(temp_data, i * step)
        final_data = list(map(lambda x, y: x + y, final_data, temp_data))

    final_data = list(map(lambda x: x / num, final_data))

    return final_data

# SWT阈值收缩去噪
def swt(data, method='sureshrink', mode='soft', wavelets_name='sym8', level=5):
    '''
    :param data: signal
    :param method: {'visushrink', 'sureshrink', 'heursure', 'minmax'}, 'sureshrink' as default
    :param mode: {'soft', 'hard', 'garotte', 'greater', 'less'}, 'soft' as default
    :param wavelets_name: wavelets name in PyWavelets, 'sym8' as default
    :param level: deconstruct level, 5 as default
    :return: processed data
    '''
    methods_dict = {'visushrink': visu_shrink,
                    'sureshrink': sure_shrink, 'heursure': heur_sure, 'minmax': min_max}
    # 创建小波对象
    wave = pywt.Wavelet(wavelets_name)

    # 分解 阈值处理
    l = len(data)
    data = np.pad(data, (0, closest_two_power(l) - l),
                  'constant', constant_values=0)

    coeffs = np.array(pywt.swt(data=data, wavelet=wave, level=level))

    for idx, coeff in enumerate(coeffs):
        var = get_var(coeffs[idx][1])

       # 求本层阈值thre
        thre = methods_dict[method](var, coeffs[idx][1])

        # 处理cD
        coeffs[idx][1] = pywt.threshold(coeffs[idx][1], thre, mode=mode)

    # 重构信号
    thresholded_data = pywt.iswt(coeffs, wavelet=wavelets_name)

    return thresholded_data[:l]

if __name__ == "__main__":
    pass
