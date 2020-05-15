from dataclasses import dataclass, field
import numpy as np
from scipy.stats import lognorm

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


def p_ds(x, medians, stddevs, dist_type='lognormal'):
    if dist_type == 'lognormal':
        return lognorm(s=stddevs, scale=medians).cdf(x)
    else:
        return None


@dataclass
class FragilityCurves:
    medians: list = field(default_factory=list)
    stddevs: list = field(default_factory=list)
    thresholds: list = field(default_factory=list)
    μs: list = field(default_factory=list)
    means: list = field(default_factory=list)
    typology: str = ''
    description: str = ''
    dist_type: str = 'lognormal'
    imt: str = 'PGA'

    @property
    def centrals(self):
        _centrals = []
        _thresholds = self.thresholds.copy()
        _thresholds.append(1.0)
        for i in range(0, len(_thresholds) - 1):
            _centrals.append(0.5 * (_thresholds[i] + _thresholds[i + 1]))
        # return [0.5 * _thresholds[0]] + _centrals
        return [0.0] + _centrals  # Για το DS0 θεωρώ ότι ο κεντρικός δείκτης βλάβης είναι 0

    def get_μs_from_medians(self):
        if self.dist_type == 'lognormal':
            self.μs = np.log(np.array(self.medians)).tolist()
            
    def get_means_from_μs(self):
        if self.dist_type == 'lognormal':
            self.means = np.exp(np.array(self.μs) + 0.5*np.array(self.stddevs)**2).tolist()



    def calc(self, x):
        p = p_ds(x, self.medians, self.stddevs, self.dist_type)

        _δP = []
        for i in range(0, len(p) - 1):
            _δP.append(p[i] - p[i + 1])
        # Για το τελευταίο DS η πιθανότητα είναι απευθείας από την καμπύλη τρωτότητας
        _δP.append(p[-1])
        # Για το DS0 η πιθανότητα είναι η 1.0 μείον την πιθανότητα του DS1
        δP = [1.0 - p[0]] + _δP

        if len(self.thresholds) > 0:
            mdf = sum(np.array(δP) * np.array(self.centrals))
        else:
            mdf = None

        _results = {'P': p,
                    'δP': δP,
                    'MDF': mdf}

        return _results

    def plot_fragility_model(self, minIML, maxIML, dist_type='lognormal', colors=None):
        xs = np.linspace(minIML, maxIML, 500)

        f, ax = plt.subplots(figsize=(12, 8))

        for iDS in range(len(self.medians)):
            _median = self.medians[iDS]
            _stdev = self.stddevs[iDS]

            if colors is None:
                color = 'grey'
            else:
                if colors=='default5':
                    colors = ['#abdb57', '#086c34', '#e28b05', '#fb4c4c', '#b91f1f']
                color = colors[iDS]

            ax.plot(xs, p_ds(xs, _median, _stdev, dist_type), linewidth=2, color=color, label=f'DS{iDS}')

        ax.set_xlim(minIML, maxIML)
        ax.set_xlabel('PGA [g]', fontsize=12)

        ax.set_ylim(0., 1.01)
        ax.set_ylabel('Probabilty of Exceedance', fontsize=12)
        ax.legend()

        return f, ax







