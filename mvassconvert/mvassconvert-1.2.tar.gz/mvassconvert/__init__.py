import os
returnSet = []
filename = 'error'


def conv(val, unit, out):
    file_path = os.path.dirname(os.path.abspath(__file__))
    global returnSet, filename
    conversionFactor = ''
    reverseFactor = ''
    i = 0
    if unit <= 8:  # TYPE Temperature
        unit -= 1
        out -= 1
        filename = '/temp'
    elif 9 <= unit <= 19:  # TYPE Time
        unit -= 9
        out -= 1
        filename = '/time'
    elif 20 <= unit <= 55:  # TYPE Volume
        unit -= 20
        out -= 20
        filename = '/volume'
    elif 56 <= unit <= 97:  # TYPE Speed
        unit -= 56
        out -= 56
        filename = '/speed'
    elif 98 <= unit <= 113:  # TYPE Acceleration
        unit -= 98
        out -= 98
        filename = '/acceleration'
    elif 114 <= unit <= 137:  # TYPE Angle
        unit -= 114
        out -= 114
        filename = '/angle'
    elif 138 <= unit <= 177:  # TYPE Area
        unit -= 138
        out -= 138
        filename = '/area'
    elif 178 <= unit <= 241:  # TYPE Area Density
        unit -= 178
        out -= 178
        filename = '/areaDensity'
    elif 242 <= unit <= 244:  # TYPE Chemical Amount
        unit -= 242
        out -= 242
        filename = '/chemicalAmount'
    elif 245 <= unit <= 298:  # TYPE Data Bandwidth
        unit -= 245
        out -= 245
        filename = '/dataBandwidth'
    elif 299 <= unit <= 351:  # TYPE Data Storage
        unit -= 299
        out -= 299
        filename = '/dataStorage'
    elif 352 <= unit <= 411:  # TYPE Density
        unit -= 352
        out -= 352
        filename = '/density'
    elif 412 <= unit <= 438:  # TYPE Electric Charge
        unit -= 412
        out -= 412
        filename = '/electricCharge'
    elif 439 <= unit <= 464:  # TYPE Electric Current
        unit -= 439
        out -= 439
        filename = '/electricCurrent'
    elif 465 <= unit <= 547:  # TYPE Energy, Work, And Heat
        unit -= 465
        out -= 465
        filename = '/ewh'
    elif 548 <= unit <= 637:  # TYPE Flow
        unit -= 548
        out -= 548
        filename = '/flow'
    elif 638 <= unit <= 674:  # TYPE Force
        unit -= 638
        out -= 638
        filename = '/force'
    elif 675 <= unit <= 716:  # TYPE Frequency
        unit -= 675
        out -= 675
        filename = '/frequency'
    elif 717 <= unit <= 724:  # TYPE Fuel Economy
        unit -= 717
        out -= 717
        filename = '/fuelEconomy'
    elif 725 <= unit <= 740:  # TYPE Illuminance
        unit -= 725
        out -= 725
        filename = '/illuminance'
    elif 741 <= unit <= 808:  # TYPE Length
        unit -= 741
        out -= 741
        filename = '/length'
    elif 809 <= unit <= 815:  # TYPE Luminance
        unit -= 809
        out -= 809
        filename = '/luminance'
    elif 816 <= unit <= 825:  # TYPE Luminous Intensity
        unit -= 816
        out -= 816
        filename = '/luminousIntensity'
    elif 826 <= unit <= 892:  # TYPE Mass
        unit -= 826
        out -= 826
        filename = '/mass'
    elif 893 <= unit <= 969:  # TYPE Mass Flow
        unit -= 893
        out -= 893
        filename = '/massFlow'
    elif 970 <= unit <= 999:  # TYPE Power
        unit -= 970
        out -= 970
        filename = '/power'
    elif 1000 <= unit <= 1031:  # TYPE Pressure
        unit -= 1000
        out -= 1000
        filename = '/pressure'
    elif 1032 <= unit <= 1036:  # TYPE Torque
        unit -= 1032
        out -= 1032
        filename = '/torque'
    elif 1037 <= unit <= 1192:  # TYPE Currency
        unit -= 1037
        out -= 1037
        i = 1
        from currency_api.converter import CurrencyRates
        r = CurrencyRates()
        factors = open(file_path+'/currencyLetters.txt', 'r')
        conversionFactors = factors.readlines()
        factors.close()
        factors = open(file_path+'/currencyLetters.txt', 'r')
        reverseFactors = factors.readlines()
        factors.close()
        inRate = conversionFactors.pop(unit)
        inRate = inRate.strip('\n')
        outRate = reverseFactors.pop(out)
        outRate = outRate.strip('\n')
        print(inRate, outRate)
        conversionFactor = ('a * ' + str(r.get_rate(inRate, 'USD')))
        reverseFactor = ('b * ' + str(r.get_rate('USD', outRate)))
        print(conversionFactor, reverseFactor)
    if i == 0:
        if filename == 'error':
            returnSet = ['sorry, and error occurred']
        else:
            factors = open(file_path + (filename + 'Factors.txt'), 'r')
            conversionFactors = factors.readlines()
            factors.close()
            conversionFactor = conversionFactors.pop(unit)
            conversionFactor = conversionFactor.strip('\n')
            factors = open(file_path + (filename + 'Reverse.txt'), 'r')
            reverseFactors = factors.readlines()
            factors.close()
            reverseFactor = reverseFactors.pop(out)
            reverseFactor = reverseFactor.strip('\n')
    a = val
    b = eval(conversionFactor)
    c = eval(reverseFactor)
    returnSet.append(c)
    return returnSet
