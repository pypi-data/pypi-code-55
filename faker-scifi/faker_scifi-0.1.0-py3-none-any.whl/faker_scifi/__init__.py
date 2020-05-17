# -*- coding: utf-8 -*-

from faker.providers import BaseProvider

# Based loosely on https://tvtropes.org/pmwiki/pmwiki.php/Main/TechnoBabble
# and https://youtu.be/naXLxNX4UZc


class SciFi(BaseProvider):
    technobabble = {}

    technobabble['verbs'] = (
        'reverse',
        'increase',
        'absorb',
        'melt',
        'release',
        'short circuit',
        'calculate',
        'use',
        'bypass',
        'inject',
        'blow',
        'instantiate',
        'generate',
        'induce',
        'accelerate',
        'close',
        'modify',
        'disable',
        'heat',
        'enhance',
        'disengage',
        'run',
        'discharge',
        'power',
        'map',
        'distress',
        'invert',
        'probe',
        'adjust',
        'penetrate',
        'employ',
        'interpolate',
        'experience',
        'detect',
        'compensate',
        'analyze',
        'project',
        'sustain',
        'disrupt',
        'raise',
        'launch',
        'calibrate',
        'expend',
        'implement',
        'attach',
        'make operational',
        'shift',
        'store')

    technobabble['adjectives starting with consonant'] = (
        'polarity of the',
        'spacial',
        'warp',
        'miniaturization',
        'molecular',
        'time-space',
        'space-time',
        'dimorphic',
        'life-sustaining',
        'submolecular',
        'quark',
        'pulse',
        'flux',
        'reality',
        'dilithium',
        'crystalline',
        'distortion of the',
        'quantum',
        'heavy-ion',
        'narrow beam of',
        'nano',
        'tri-polymer',
        'chromodynamic',
        'multi-dimensional',
        'black hole',
        'light speed',
        'theoretical',
        'virtual',
        'missing',
        'minor',
        'highly localized',
        'neutrino',
        'discrete',
        'source of the',
        'result of the',
        'hyper',
        'sub-space',
        'diagnostic of the',
        'polarized',
        'concentration of',
        'radiated',
        'coherent',
        'large quantity of the',
        'functional',
        'magnetospheric',
        'bioregenerative',
        'memory',
        'phased',
        'Heisenberg',
        'gravitational',
        'double',
        'liquid',
        'turbo',
        'utlization of the')

    technobabble['adjectives starting with vowel'] = (
        'epithelial',
        'atomic',
        'external inertial',
        'infinite',
        'electro-magnetic',
        'upper',
        'aggregate',
        'inert',
        'adaptive',
        'anti-',
        'uncertainty')

    technobabble['singular nouns'] = (
        'flow',
        'linkage',
        'tissue',
        'core',
        'ray',
        'overloader',
        'coordinate',
        'system',
        'control',
        'grid',
        'parsec',
        'inertia',
        'reading',
        'vortex',
        'energy',
        'wave',
        'emitter',
        'field',
        'radiation',
        'fusion',
        'dampener',
        'mainframe',
        'particle',
        'plasma',
        'module',
        'drive',
        'physics',
        'collision',
        'prototype',
        'space',
        'imaging',
        'data',
        'fluctuation',
        'anamoly',
        'phenomenon',
        'continuum',
        'pattern',
        'source',
        'emission',
        'whirlwind',
        'signal',
        'atmosphere',
        'shield',
        'burst',
        'reaction',
        'sensor',
        'interior',
        'output',
        'interference',
        'inverter',
        'trajectory',
        'ionization',
        'subprogram',
        'log',
        'coil',
        'disruption',
        'anomaly',
        'principle',
        'vector')

    technobabble['plural nouns'] = (
        'flows',
        'linkages',
        'tissues',
        'cores',
        'rays',
        'overloaders',
        'coordinates',
        'systems',
        'controls',
        'grids',
        'parsecs',
        'readings',
        'vertices',
        'energies',
        'waves',
        'emitters',
        'fields',
        'dampeners',
        'mainframes',
        'particles',
        'plasmas',
        'modules',
        'drives',
        'collisions',
        'prototypes',
        'spaces',
        'images',
        'fluctuations',
        'anamolies',
        'phenomena',
        'continuums',
        'patterns',
        'sources',
        'emissions',
        'whirlwinds',
        'signals',
        'shields',
        'bursts',
        'reactions',
        'sensors',
        'interiors',
        'outputs',
        'interferences',
        'inverters',
        'trajectories',
        'ionizations',
        'subprograms',
        'logs',
        'coils',
        'disruptions',
        'anomalies',
        'principles',
        'vectors')

    article_choices = (
        'a',
        'an',
        'the')

    def _choose_babble_phrases(self) -> tuple:
        """Pick the specific phrases for babble to use
        This avoids grammar problems
        """
        noun_choices = ('singular nouns', 'plural nouns')
        noun_choice = self.random_element(noun_choices)

        adjective_choices = (
            'adjectives starting with consonant',
            'adjectives starting with vowel')

        if noun_choice == 'singular nouns':
            article_choice = self.random_element(self.article_choices)
        else:
            article_choice = 'the'

        if article_choice == 'an':
            adjective_choice = 'adjectives starting with vowel'
        elif article_choice == 'a':
            adjective_choice = 'adjectives starting with consonant'
        else:
            adjective_choice = self.random_element(adjective_choices)

        return (
            self.technobabble['verbs'],
            article_choice,
            self.technobabble[adjective_choice],
            self.technobabble[noun_choice])

    def babble(self) -> str:
        """
        :example 'reverse the polarity of the neutron flow'
        """
        result = []
        for phrase in self._choose_babble_phrases():
            if phrase in self.article_choices:
                result.append(phrase)
            else:
                result.append(self.random_element(phrase))

        return " ".join(result)
