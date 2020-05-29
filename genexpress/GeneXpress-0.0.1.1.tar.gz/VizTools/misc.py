from statsmodels.stats.power import TTestIndPower


def calc_stat_power(effect_size, cutoff=.05, power=.8):
    """

    Args:
        effect_size:
        cutoff:
        power:

    Returns:

    """
    power_analysis = TTestIndPower()
    samples = power_analysis.solve_power(effect_size=effect_size, power=power, alpha=cutoff)
    return samples