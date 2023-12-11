import math
import numpy as np
import matplotlib.pyplot as plt

def two_peak_normal_distribution(x, x1, x2, amplitude1, amplitude2, sigma1=1, sigma2=1):
  peak1 = amplitude1 * np.exp(-((x - x1) ** 2) / (2 * sigma1 ** 2))
  peak2 = amplitude2 * np.exp(-((x - x2) ** 2) / (2 * sigma2 ** 2))
  return peak1 + peak2

def tram_probability (time):
  amplitude1 = 0.3
  amplitude2 = 0.3
  amplitude_mean = (amplitude1 + amplitude2) / 2
  time_start = 7 * 60
  time_end = 20 * 60 - 1
  rush_1 = 8 * 60
  rush_2 = 16 * 60
  baseline = two_peak_normal_distribution(time, rush_1, rush_2, 0.3, 0.3, 100, 100)
  result = np.power(baseline / amplitude_mean, 0.8) * amplitude_mean 
  
  return result

def display_probability():
  x = np.linspace(400, 1200, 2000)
  y = tram_probability(x)
  x_to_time = lambda x: f'{math.floor(x / 60)}:{x % 60}'
  plt.plot(x, y)
  plt.show()
