class rulesets:

    mr = None

    def __init__(self, mr):
        self.mr = mr

    # https://en.wikipedia.org/wiki/Nelson_rules
    def nelson(self):
        violations = { }
        bins = self.mr.individuals_bins()

        # Rule 1
        # One point is more than 3σ from the mean.
        # One sample is out of control.
        rule1 = execute_run_test(bins, 1, lambda t: t > 3 or t < -3)
        violations['Points more than 3σ from the mean'] = rule1  

        # Rule 2
        # Nine (or more) points in a row are on the same side of the mean.
        # Some prolonged bias exists.
        rule2 = execute_run_test(bins, 9, lambda t: t > 0)
        rule2 = rule2 + execute_run_test(bins, 9, lambda t: t < 0)
        violations['9 points same side of the mean'] = sorted(rule2)

        # Rule 3
        # Six (or more) points in a row are continually increasing (or decreasing).
        # A trend exists.
        direction = self.mr.individuals_direction()
        rule3 = execute_run_test(direction, 6, lambda t: t > 0)
        rule3 = rule3 + execute_run_test(direction, 6, lambda t: t < 0)
        violations['6 in/decreasing points'] = sorted(rule3)

        # Rule 4
        # Fourteen (or more) points in a row alternate in direction, increasing then decreasing.
        # This much oscillation is beyond noise. Note that the rule is concerned with directionality only. The position of the mean and the size of the standard deviation have no bearing.
        #
        # This is the only rule, not able to be implemented standard method
        rule4 = []
        rolling = [0] * 14
        for sample in range(len(direction) - 1):
            rolling.append(direction[sample] != direction[sample + 1])
            rolling = rolling[1:]
            if sum(rolling) == 14:
                for index in range(14):
                    rule4.append(sample - index)
        violations['14 oscillating points'] = sorted(list(set(rule4)))
        
        # Rule 5
        # Two (or three) out of three points in a row are more than 2σ from the mean in the same direction.
        # There is a medium tendency for samples to be mediumly out of control.The position of the third point is unspecified.
        rule5 = execute_run_test(bins, 3, lambda t: t > 2, 2/3)
        rule5 = rule5 + execute_run_test(bins, 3, lambda t: t < -2, 2/3)
        violations['2 of 3 points more than 2σ from the mean'] = sorted(rule5)

        # Rule 6
        # Four (or five) out of five points in a row are more than 1σ from the mean in the same direction.
        # There is a strong tendency for samples to be slightly out of control. The position of the fifth point is unspecified.
        rule6 = execute_run_test(bins, 5, lambda t: t > 1, 4/5)
        rule6 = rule6 + execute_run_test(bins, 5, lambda t: t < -1, 4/5)
        violations['4 of 5 points more than 1σ from the mean'] = sorted(rule6)

        # Rule 7
        # Fifteen points in a row are all within 1σ of the mean on either side of the mean.
        # With 1σ, greater variation would be expected.
        rule7 = execute_run_test(bins, 15, lambda t: abs(t) == 1)
        violations['15 points within 1σ of the mean'] = sorted(rule7)

        # Rule 8
        # Eight points in a row exist, but none within 1σ of the mean, and the points are in both directions from the mean.
        # Jumping from above to below whilst missing the 1σ band is rarely random.
        rule8 = execute_run_test(bins, 8, lambda t: abs(t) > 1)
        violations['8 points outwith 1σ of the mean'] = sorted(rule8)

        return violations
        
    # https://en.wikipedia.org/wiki/Western_Electric_rules
    def western_electic(self):
        violations = { }
        bins = self.mr.individuals_bins()

        # Rule 1
        # Any single data point falls outside the 3σ-limit from the mean
        rule1 = execute_run_test(bins, 1, lambda t: t > 3 or t < -3)
        violations['Points more than 3σ from the mean'] = rule1        

        # Rule 2
        # Two out of three consecutive points fall beyond the 2σ-limit, on the same side of the mean
        rule2 = execute_run_test(bins, 3, lambda t: t > 2, 2/3)
        rule2 = rule2 + execute_run_test(bins, 3, lambda t: t < -2, 2/3)
        violations['2 of 3 points more than 2σ from the mean'] = sorted(rule2)

        # Rule 3
        # Four out of five consecutive points fall beyond the 1σ-limit, on the same side of the mean
        rule3 = execute_run_test(bins, 5, lambda t: t > 1, 4/5)
        rule3 = rule3 + execute_run_test(bins, 5, lambda t: t < -1, 4/5)
        violations['4 of 5 points more than 1σ from the mean'] = sorted(rule3)

        # Rule 4
        # Eight consecutive points fall on the same side of the mean
        rule4 = execute_run_test(bins, 8, lambda t: t > 0)
        rule4 = rule4 + execute_run_test(bins, 8, lambda t: t < 0)
        violations['8 points same side of the mean'] = sorted(rule4)

        return violations

    def basic(self):
        violations = { }
        bins = self.mr.individuals_bins()

        # Rule 1
        # Any single data point falls outside the 3σ-limit from the mean
        rule1 = execute_run_test(bins, 1, lambda t: t > 3 or t < -3)
        violations['Points more than 3σ from the mean'] = rule1

        # Rule 2
        # Seven consecutive points fall on the same side of the mean
        rule2 = execute_run_test(bins, 7, lambda t: t > 0)
        rule2 = rule2 + execute_run_test(bins, 7, lambda t: t < 0)
        violations['7 points same side of the mean'] = sorted(rule2)

        return violations

# test should result in a boolean
# method tests runs of length sample size return true for the test some rules are 
# "four out of five", an optional ratio parameter allows for this
def execute_run_test(samples, sample_size, test, ratio = 1):
    results = []
    rolling = [0] * sample_size
    for sample in range(len(samples)):
        rolling.append(test(samples[sample]))
        rolling = rolling[1:]
        if sum(rolling) >= (sample_size * ratio):
            for index in range(sample_size):
                results.append(sample - index)
    return sorted(list(set(results)))