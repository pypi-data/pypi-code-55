import dtit.pyLiteMath as lmath
import math
import numpy as np

print("----------------------")
test_values = list(range(1, 16))
for value in test_values:
    print("pydiv({:d}, 7) = {:d}, ground truth = {:.2f}".format(value, lmath.pydiv(value, 7), value/7))
print("----------------------")

print("----------------------")
test_values = list(range(0, 5))
for value in test_values:
    print("pypower(2, {:d}) = {:d}".format(value, lmath.pypower(2,value)))
    print("pypower(10, {:d}) = {:d}".format(value, lmath.pypower(10,value)))
print("----------------------")

print("----------------------")
test_values = [1, 2, 8, 10, 100, 250, 2048, 4096, 19861, 20232, 32767, 40500, 42600, 44660, 45678, 65001, 65301, 65535, 1234567, 1345644, 1459876]
for value in test_values:
    log2_v = lmath.pylog2(value)
    int_part = (int)(log2_v / 256)
    dec_part = (int)(log2_v % 256 * 10000 / 256)
    print("pylog2({:d}) = {:d}.{:d}, pylog2a({:d}, 2) = {:d} vs. math.log {:.4f}".format(value, int_part, dec_part, value, lmath.pylog2a(value, 2), math.log(value)/math.log(2)))
print("----------------------")


print("----------------------")
a = -1859
b = 12
print("pydividen({:d}, {:d}) = {:d} vs {:.1f}".format(a, b, lmath.pydividen(a, b), a/b))
a = 1859
print("pydividen({:d}, {:d}) = {:d} vs {:.1f}".format(a, b, lmath.pydividen(a, b), a/b))
print("----------------------")


print("----------------------")
test_values = np.array([-886, -843, 250, -526, -181, 747, -30, -540, -236, 62, -9, 333]).astype(np.int16)
value = lmath.pymean(test_values)
print("pymean() = {:d} vs {:.1f}".format(value, np.mean(test_values)))
print("----------------------")

print("----------------------")
test_values = np.array([-886, -843, 250, -526, -181, 747, -30, -540, -236, 62, -9, 333]).astype(np.int16)
print("pystatistics() = sum, max, min, mean, std")
value = lmath.pystatistics(test_values)
print("pystatistics() = {value}".format(value=value))
print("ground truth = {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.1f}".format(np.sum(test_values), np.max(test_values), np.min(test_values), np.mean(test_values), np.std(test_values)))
print("----------------------")