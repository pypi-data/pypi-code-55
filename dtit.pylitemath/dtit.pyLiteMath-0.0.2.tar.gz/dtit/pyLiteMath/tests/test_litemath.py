import dtit.pyLiteMath as lmath

print("----------------------")
print("pymin({:d}, {:d}) = {:d}".format(10, 3, lmath.pymin(10, 3)))
print("----------------------")

print("----------------------")
print("pymax({:d}, {:d}) = {:d}".format(1688, 2020, lmath.pymax(1688, 2020)))
print("----------------------")

print("----------------------")
test_values = [1433, -1986, 0]
for value in test_values:
    print("pyabs({:d}) = {:d}".format(value, lmath.pyabs(value)))
print("----------------------")

print("----------------------")
test_values = list(range(0,11)) + list(range(98,102)) + list(range(248,252)) + list(range(9998,10002))
for value in test_values:
    print("pysqrtn({:d}) = {:d}".format(value, lmath.pysqrt(value)))
print("----------------------")

print("----------------------")
test_values = range(0, 101)
for value in test_values:
    print("pysqrtn_m10({:d}) = {:d}".format(value, lmath.pysqrt_m10(value)))
print("----------------------")
