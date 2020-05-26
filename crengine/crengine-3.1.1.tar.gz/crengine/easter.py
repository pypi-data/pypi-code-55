######################################################################
### Date of Easter Sunday (Gregorian Calendar)
######################################################################
### The formulae for determining Easter Sunday came from an article
### by Simon Kershaw - http://easter.oremus.org/when/bradley.html
### Implemented in Python by Jonathan Wilson 12th April 2020
######################################################################

from datetime import datetime, timedelta

### easter - determine date of Easter Sunday

def easter(y=0):

    # If no year was supplied, use current year
    if y==0:
        y=datetime.now().year

    # Golden number
    g=y%19+1

    # Solar and lunar corrections
    s=(y-1600)//100-(y-1600)//400
    l=(((y-1400)//100)*8)//25

    # Paschal full moon (days after March 21st)
    p=(3-11*g+s-l)%30

    # Pascal full moon - correction
    if p==29 or (p==28 and g>11):
        p-=1

    # Dominical number
    d=(y+y//4-y//100+y//400)%7

    # Number of days from PFM to Easter Sunday
    x=(4-d-p)%7+1

    # Return date of Easter Sunday
    return datetime(y,3,21)+timedelta(p+x)


