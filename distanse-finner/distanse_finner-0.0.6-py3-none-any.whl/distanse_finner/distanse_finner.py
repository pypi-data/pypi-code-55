from pandas import read_csv, to_datetime
from pylab import arange, arcsin, array, cos, pi, sin, sqrt
from scipy.interpolate import interp1d


def haversinus(vinkel):
    """Haversinus funksjonen
    
    Brukes for å regne ut vinkelen mellom to punkt på et kuleskall
    
    Du kan lese om denne funksjonen her
    https://en.wikipedia.org/wiki/Versine
    """
    return sin(vinkel/2)**2


def arc_haversinus(forhold):
    """Den inverse haversinus funksjonen
    
    Brukes for å regne ut vinkelen mellom to punkt på et kuleskall
    
    Du kan lese om denne funksjonen her
    https://en.wikipedia.org/wiki/Versine
    """
    return 2*arcsin(sqrt(forhold))


def sentralvinkel(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2,
):
    """Finner sentralvinkelen mellom to punkt på et kuleskall
    
    For å finne sentralvinkelen brukes haversinus formelen,
    som du kan lese om her:
    https://en.wikipedia.org/wiki/Haversine_formula
    """
    lengdegrad_diff = lengdegrad2 - lengdegrad1
    breddegrad_diff = breddegrad1 - breddegrad2
    
    ledd1 = haversinus(lengdegrad_diff)
    ledd2 = cos(lengdegrad1)*cos(lengdegrad2)*haversinus(breddegrad_diff)
    
    return arc_haversinus(ledd1 + ledd2)


def avstand(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2, radius
):
    """Finner avstanden mellom to punkt på et kuleskall.
    
    Du kan lese mer om haversinus formelen vi bruker her
    https://en.wikipedia.org/wiki/Haversine_formula
    
    Vinkelene er lister 
     * Første element er lengdegrad 
     * Andre element er breddegrad
    """
    return radius*sentralvinkel(lengdegrad1, breddegrad1, lengdegrad2, breddegrad2)


def jordavstand(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2
):
    """Finn luftavstand mellom to punkt på jordoverflata i km.
    
    Her bruker vi en kuleapproksimasjon av jorda, men siden jorda
    er elliptisk vil tallene være noe feil med veldig store
    avstander (f.eks avstand mellom to fjerne land).
    """
    jord_radius_km = 6371
    
    return avstand(
        lengdegrad1, breddegrad1, lengdegrad2, breddegrad2, jord_radius_km
    )


def grad_til_radian(grad):
    """Gjør om grader til radianer
    """
    return grad*pi/180


def hent_lengdegrad(rad):
    """Hent ut lengdegraden fra en rad fra en GPSLogger CSV fil.
    """
    return grad_til_radian(rad['lon'])


def hent_breddegrad(rad):
    """Hent ut breddegraden fra en rad fra en GPSLogger CSV fil.
    """
    return grad_til_radian(rad['lat'])


def finn_tidsendring_i_sekunder(tidspunkt1, tidspunkt2):
    """Finner tidsendring i sekund mellom to tidspunktsvariabler.
    """
    tidsendring = tidspunkt1 - tidspunkt2
    return tidsendring.seconds + tidsendring.microseconds/1_000_000


def hent_forflyttningsdata(data):
    """Lager en array som inneholder hvor langt man har bevegd seg i kilometer ved den gitte målingen.
    """
    forflytning_siden_start = [0]
    
    # Vi starter med å ikke ha noen posisjon
    nåværende_lengdegrad = None
    nåværende_breddegrad = None
    for tidspunkt, rad in data.iterrows():
        if rad['provider'] != 'gps':
            continue
            
        forrige_lengdegrad = nåværende_lengdegrad
        forrige_breddegrad = nåværende_breddegrad
        nåværende_lengdegrad = hent_lengdegrad(rad)
        nåværende_breddegrad = hent_breddegrad(rad)
        
        # Hvis vi ikke har noen forrige posisjon
        # så fortsetter vi til neste iterasjon
        if forrige_lengdegrad is None:
            continue
        
        # Regn ut avstanden vi har bevegd oss
        posisjonsendring = jordavstand(
            forrige_lengdegrad,
            forrige_breddegrad,
            nåværende_lengdegrad,
            nåværende_breddegrad
        )
        
        # Legg til den avstanden i forflytningen vår
        nåværende_forflytning = forflytning_siden_start[-1] + posisjonsendring
        
        # Plasser den nåværende forflytningen på slutten av forflytningslista
        forflytning_siden_start.append(nåværende_forflytning)
    
    return array(forflytning_siden_start)


def hent_tidsdata(data):
    """Lager en array som inneholder hvor lenge man har bevegd seg i sekunder ved den gitte målingen.
    """
    sekunder_siden_start = [0]
    
    nåværende_tidspunkt = None
    for indeks, rad in data.iterrows():
        if rad['provider'] != 'gps':
            continue
            
        forrige_tidspunkt = nåværende_tidspunkt
        nåværende_tidspunkt = indeks
        if forrige_tidspunkt is None:
            continue
        
        tidsendring = finn_tidsendring_i_sekunder(
            nåværende_tidspunkt, forrige_tidspunkt
        )
        tid_siden_start = sekunder_siden_start[-1] + tidsendring
        sekunder_siden_start.append(tid_siden_start)
    
    return array(sekunder_siden_start)


def hent_uniform_data(data, tid_mellom_målinger_s=5):
    """Gjør om datasettet slik at alle målingene er like langt unna hverandre
    
    Trekker en rett linje mellom hvert datapunkt 
    (slik som når vi plotter) og henter ut forflyttningsdata
    med like langt tid mellom hver måling.
    
    Returnerer avstander og tidspunkt.
    """
    tidspunkt_s = hent_tidsdata(data)
    avstander_km = hent_forflyttningsdata(data)
    
    interpolant = interp1d(tidspunkt_s, avstander_km)
    tidspunkt_uniform = arange(0, tidspunkt_s[-1], tid_mellom_målinger_s)
    
    return tidspunkt_uniform, interpolant(tidspunkt_uniform)


def last_rådata(datafil):
    data = read_csv(datafil).set_index('time')
    data.index = to_datetime(data.index)
    
    tidspunkt_s = hent_tidsdata(data)
    avstander_km = hent_forflyttningsdata(data)
    
    return tidspunkt_s, avstander_km


def last_uniform_data(datafil, tid_mellom_målinger_s):
    data = read_csv(datafil).set_index('time')
    data.index = to_datetime(data.index)
    
    return hent_uniform_data(data, tid_mellom_målinger_s)