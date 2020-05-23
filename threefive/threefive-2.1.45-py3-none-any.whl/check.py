
def syncbits(bite):
    '''
    Mpeg-ts requires each packet
    to start with the syncbyte 0x47
    '''
    return bite == 0x47


def tidbits(bite):
    '''
    SCTE 35 requires the packet
    to have a table id of 0xfc
    '''
    return bite == 0xfc

def sparebits(bite):
    '''
    SCTE 35 requires that the
    four bits after the table id
    be 0b0011
    '''
    return (bite >> 4) == 0b0011

def protobits(bite):
    '''
    SCTE 35 protocol_version
    must be 0
    '''
    return bite == 0
