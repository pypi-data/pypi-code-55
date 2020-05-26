# -*- coding: utf-8 -*-
import logging
import struct
import math
import sys

from .crc16 import crc16

logger = logging.getLogger(__name__)

def debugprint(msg):
    pass
    #logger.debug("{}".format(msg))

class NeedMoreData(BaseException):
    pass

class AFDecoder:
    def __init__(self):
        self.timestamp = (None, None)
        self.istd = None # contains data payload, 24ms of encoded audio
        self.version = None
        self.uptime = None
        self.audio_left = None
        self.audio_right = None
        self.dflc = None
        self._success = False

    def decode_af(self, in_data):
        if len(in_data) < 10:
            raise NeedMoreData()
        headerdata = in_data[:10]
        ix = 10

        sync, plen, seq, ar, pt = struct.unpack("!2sLHBc", headerdata)

        crc_flag = (ar & 0x80) != 0x00
        revision = ar & 0x7F

        if len(in_data) < ix + plen + 2:
            raise NeedMoreData()
        payload = in_data[ix:ix+plen]
        ix += plen

        (crc,) = struct.unpack("!H", in_data[ix:ix+2])
        ix += 2

        crc_calc = crc16(headerdata)
        crc_calc = crc16(payload, crc_calc)
        crc_calc ^= 0xFFFF

        crc_ok = crc_calc == crc

        success = False
        if crc_flag and crc_ok:
            debugprint("AF CRC ok")
            debugprint("plen {}".format(plen))
            debugprint("seq {}".format(seq))
            debugprint("revision {}".format(revision))
            debugprint("protocol type {}".format(pt))

            if pt == b"T":
                success = self._decode_tag(payload)
        elif crc_flag:
            logger.warn("AF CRC: is 0x{0:04x}, calculated 0x{1:04x}".format(crc, crc_calc))
        else:
            # CRC absent
            logger.info("AF CRC absent")

        self._success = success

        return (success, ix)

    def is_valid(self):
        return self._success

    def __str__(self):
        return "AF Packet {} ".format(self.dflc) + "valid" if self.is_valid() else "invalid"

    def _tagitems(self, tagpacket):
        i = 0
        while i+8 < len(tagpacket):
            name, length = struct.unpack("!4sL", tagpacket[i:i+8])

            # length is in bits, because it's more annoying this way
            if length % 8 != 0:
                sys.stderr.write("ASSERTION ERROR: length of tagpacket is not multiple of 8: {}".format(length))
            length /= 8
            length = int(length)

            debugprint("  tag item {} length {}: {}-{}".format(name, length, i+8, i+8+length))
            tag_value = tagpacket[i+8:i+8+length]
            yield {'name': name, 'length': length, 'value': tag_value}

            i += 8 + length
        debugprint("Completed decoding all TAG items after {} bytes".format(i))

    def _decode_tag(self, tagpacket):
        debugprint("Tag packet len={}".format(len(tagpacket)))
        for item in self._tagitems(tagpacket):
            # TODO handle tag decode failure
            if item['name'].startswith(b"*ptr"):
                self._decode_starptr(item)
            elif item['name'] == b"dsti":
                self._decode_dsti(item)
            elif item['name'].startswith(b"ss"):
                self._decode_ssn(item)
            elif item['name'] == b"*dmy":
                self._decode_stardmy(item)
            elif item['name'] == b"ODRa":
                self._decode_odr_audio(item)
            elif item['name'] == b"ODRv":
                self._decode_odr_version(item)
            else:
                logger.warn("Unknown tag item '{}': {}".format(item['name'], item['value']))
        return True

    def _decode_starptr(self, item):
        debugprint("TAG item {} ({})".format(item['name'], item['length']))
        tag_value = item['value']

        unpacked = struct.unpack("!4sHH", tag_value)
        protocol, major, minor = unpacked

        debugprint("Protocol {}, Ver {} {}".format(protocol, major, minor) )
        return True

    def _decode_stardmy(self, item):
        debugprint("TAG item {} ({})".format(item['name'], item['length']))
        return True

    def _decode_dsti(self, item):
        item_dsti_header_struct = "!H"
        tag_value = item['value']
        offset = 0
        (dsti_header, ) = struct.unpack(item_dsti_header_struct, tag_value[:2])
        offset += 2

        stihf = (dsti_header >> 15) & 0x1
        atstf = (dsti_header >> 14) & 0x1
        rfadf = (dsti_header >> 13) & 0x1
        dfcth = (dsti_header >> 8) & 0x1F
        dfctl = dsti_header & 0xFF

        self.dflc = dfcth * 250 + dfctl # modulo 5000 counter

        expected_length = 2 + (3 if stihf else 0) + (1 + 4 + 3 if atstf else 0) + (9 if rfadf else 0)

        if expected_length != item['length']:
            logger.error("DSTI has incorrect length {}, expected {}".format(item['length'], expected_length))
            return False

        if stihf:
            stat, spid = struct.unpack("!BH", tag_value[offset:offset+3])
            offset += 3
            #m_data_collector.update_stat(stat, spid)

        if atstf:
            utco, seconds = struct.unpack("!BI", tag_value[offset:offset+5])
            offset += 5

            self.timestamp = (utco, seconds)

            tsta1, tsta2, tsta3 = struct.unpack("!BBB", tag_value[offset:offset+3])
            offset += 3
            tsta = (tsta1 << 16) | (tsta2 << 8) | tsta3
        else:
            # Null timestamp, ETSI ETS 300 799, C.2.2
            tsta = 0xFFFFFF

        if rfadf:
            rfad = tag_value[offset:offset+9]
            offset += 9

            #m_data_collector.update_rfad(rfad)

        return True

    def _decode_ssn(self, item):
        _, ssN = struct.unpack("!2sH", item['name'])
        debugprint("TAG SS{:02}".format(ssN))

        tag_value = item['value']

        offset = 0
        rfa = tag_value[offset] >> 3
        tid = tag_value[offset] & 0x07

        istc1, istc2, istc3 = struct.unpack("!BBB", tag_value[offset:offset+3])
        offset += 3
        istc = (istc1 << 16) | (istc2 << 8) | istc3

        tidext = istc >> 13
        crcstf = (istc >> 12) & 0x1
        stid = istc & 0xFFF

        if rfa != 0:
            debugprint("EDI: rfa field in SSnn tag non-null")

        self.istd = tag_value[offset:]

    def _decode_odr_audio(self, item):
        tag_value = item['value']

        audio_left, audio_right = struct.unpack("!HH", tag_value)
        self.audio_left = audio_left
        self.audio_right = audio_right

        debugprint("ODRa: L:{} R:{}".format(audio_left, audio_right))

    def get_audio_levels(self):
        """
        Returns a tuple with left and right audio levels, or (None, None) if frame is not valid
        """
        if self.audio_left is None or self.audio_right is None:
            return (None, None)
        else:
            int16_max = 0x7FFF
            try:
                dB_l = round(20*math.log10(float(self.audio_left) / int16_max), 1)
            except ValueError:
                dB_l = -90.0

            try:
                dB_r = round(20*math.log10(float(self.audio_right) / int16_max), 1)
            except ValueError:
                dB_r = -90.0

            return (dB_l, dB_r)



    def _decode_odr_version(self, item):
        tag_value = item['value']

        len_uptime = 4
        len_version = len(tag_value) - len_uptime

        version, uptime = struct.unpack("!{}sI".format(len_version), tag_value)
        self.version = version
        self.uptime = uptime

        debugprint("ODRv: {} up {}".format(version, uptime))


class AFEncoder:
    def __init__(self):
        self.tag_items = []

    def build_afpacket(self, seq, tagpacket_alignment):
        tagpacket = self._build_tagpacket(tagpacket_alignment)

        af = b"AF"
        taglength = len(tagpacket)
        af += struct.pack("!IH", taglength, seq)

        # fill rest of header
        have_crc = True
        AFHEADER_PT_TAG = b'T'
        # AF Packet Major (3 bits) and Minor (4 bits) version
        AFHEADER_VERSION = 0x10 # MAJ=1, MIN=0
        # ar_cf: CRC=1
        af += bytes([((0x80 if have_crc else 0) | AFHEADER_VERSION)])
        af += AFHEADER_PT_TAG

        af += tagpacket

        # calculate CRC over AF Header and payload
        crc_calc = 0xFFFF
        crc_calc = crc16(af, crc_calc)
        crc_calc ^= 0xFFFF

        af += struct.pack("!H", crc_calc)

        return af

    def _build_tagpacket(self, alignment):
        packet = b''.join(self.tag_items)

        if alignment == 0:
            pass # no padding
        elif alignment == 8:
            # Add padding inside TAG packet
            packet += b'\0' * (len(packet) % 8)
            # TS 102 821, 5.1, "padding shall be undefined"
        elif alignment > 8:
            dmy = self._encode_stardmy(alignment - 8)
            packet += dmy
        else:
            raise RuntimeError("Invalid alignment requirement {} defined in TagPacket".format(alignment))

        return packet

    def add_starptr(self, protocol, major, minor):
        """protocol a four-byte string, minor and major are 16-bit integers"""
        tag = b'*ptr\0\0\0\x40' # length is fixed
        tag += struct.pack("!4sHH", protocol, major, minor)
        self.tag_items.append(tag)

    def _encode_stardmy(self, length):
        tag = b'*dmy'
        length_bits = length * 8
        tag += struct.pack("!I", length_bits)
        tag += (b'\0' * length)
        return tag

    def add_dsti(self, dflc, tsta, utco, seconds):
        """Add a DSTI tag.

        0 <= dflc < 5000

        if tsta == 0xFFFFFF, tsta, utco, seconds are ignored"""
        dfctl = dflc % 250
        dfcth = int(dflc / 250)

        stihf = False
        atstf = tsta != 0xFFFFFF
        rfad = b''
        rfadf = len(rfad) > 0

        dstiHeader = dfctl | (dfcth << 8) | (rfadf << 13) | (atstf << 14) | (stihf << 15)

        tagdata = struct.pack("!H", dstiHeader)

        if stihf:
            stat = 0
            spid = 0
            tagdata += struct.pack("!BH", stat, spid)

        if atstf:
            tagdata += struct.pack("!BI", utco, seconds)
            tagdata += bytes([(tsta >> 16) & 0xFF, (tsta >> 8) & 0xFF, tsta & 0xFF])

        if rfadf:
            tagdata += rfad

        tag = b'dsti'

        # calculate and update size
        # remove TAG name and TAG length fields and convert to bits
        tag += struct.pack("!I", len(tagdata) * 8)
        tag += tagdata
        self.tag_items.append(tag)

    def add_ssm(self, stream_id, istd_data):
        """
        Add stream. Stream-ID is 1-indexed!
        """
        rfa = 0
        tid = 0 # See EN 300 797, 5.4.1.1. Value 0 means "MSC sub-channel"
        tidext = 0 # EN 300 797, 5.4.1.3, Value 0 means "MSC audio stream"
        crcstf = False
        stid = 0

        istc = (rfa << 19) | (tid << 16) | (tidext << 13) | ((1 if crcstf else 0) << 12) | stid
        tagdata = bytes([(istc >> 16) & 0xFF, (istc >> 8) & 0xFF, istc & 0xFF])
        tagdata += istd_data

        tag = struct.pack('!2sH', b"ss", stream_id)
        tag += struct.pack("!I", len(tagdata) * 8)
        tag += tagdata

        self.tag_items.append(tag)

    def add_odr_audio(self, audio_left, audio_right):
        length = 2 * 2 # 2 * sizeof(int16_t)
        length_bits = length * 8
        tag = struct.pack("!4sIHH", b'ODRa', length_bits, audio_left, audio_right)
        self.tag_items.append(tag)

    def add_odr_version(self, uptime, version):
        length = len(version) + 4
        tag = struct.pack("!4sI", b'ODRv', length * 8)
        tag += version
        tag += struct.pack("!I", uptime)
        self.tag_items.append(tag)

