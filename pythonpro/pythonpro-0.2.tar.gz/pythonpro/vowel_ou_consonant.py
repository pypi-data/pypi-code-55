"""
This program receive a letter and verify if it is consonant or vowel.
"""


def vocal_ou_consoante(letra):
    if letra in list('aeiou'):
        return 'You digited a vowel'
    elif letra in set('BÇDFGHJKLMNÑPQRSTVWXYZbcçdfhjklmnñpqrsvwxyz'):
        return 'You digited a consonant'
    else:
        return 'Incorrect input'


letra = input('Digite uma Letra -> ')
print(vocal_ou_consoante(letra))
