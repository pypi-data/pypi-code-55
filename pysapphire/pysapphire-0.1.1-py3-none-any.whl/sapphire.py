def encrypt(key, data):
    """Encrypt data using a Saphire II stream cipeher

    Args:
        key (bytearray): key to use for encryption
        data (bytearray): data to encrypt
    Returns:
        bytearray: encrypted data
    """
    sph = Sapphire(key)
    encrypted_bytes = []
    for b in data:
        encrypted_bytes.append(sph.encrypt(b))
    return bytearray(encrypted_bytes)


def decrypt(key, data):
    """Decrypt data using a Saphire II stream cipeher

    Args:
        key (bytearray): key to use for decryption
        data (bytearray): data to decrypt
    Returns:
        bytearray: decrypted data
    """
    sph = Sapphire(key)
    decrypted_bytes = []
    for b in data:
        decrypted_bytes.append(sph.decrypt(b))
    return bytearray(decrypted_bytes)


class Sapphire:
    def __init__(self, key=None):
        """Construct a Sapphire Stream Cipher from a key, possibly None or b''

        Args:
            key (bytearray): key to use for cipher
        """
        self.__cards = [0]*256
        if len(key) > 0:
            self.__initialize(key)
        else:
            self.hashInit()
    
    def __del__(self):
        self.burn()

    def encrypt(self, b):
        """Encrypt a single byte, presumably the next.

        Args:
            b (int): byte to encrypt

        Returns:
            int: encrypted byte
        """
        # Picture a single enigma rotor with 256 positions, rewired
        # on the fly by card-shuffling.

        # This cipher is a variant of one invented and written
        # by Michael Paul Johnson in November, 1993.

        # Convert from a byte to an int, but prevent sign extension.
        # So -16 becomes 240
        b_val = b & 0xFF

        # Shuffle the deck a little more.
        self.__shuffle()

        # Output one byte from the state in such a way as to make it
        # very hard to figure out which one you are looking at.
        self.__last_cipher = self.__get_hidden_byte(b_val)

        self.__last_plain = b_val

        return self.__last_cipher

    def decrypt(self, b):
        """Decrypt a single byte, presumably the next.

        Args:
            b (int): byte to decrypt

        Returns:
            int: decrypted byte
        """
        # Convert from a byte to an int, but prevent sign extension.
        # So -16 becomes 240
        b_val = b & 0xFF

        # Shuffle the deck a little more.
        self.__shuffle()

        # Output one byte from the state in such a way as to make it
        # very hard to figure out which one you are looking at.
        self.__last_plain = self.__get_hidden_byte(b_val)

        self.__last_cipher = b_val

        return self.__last_plain

    def burn(self):
        """Destroy key and state information in RAM.

        This function is automatically called by the destructor.
        """
        for i in range(len(self.__cards)):
            self.__cards[i] = 0
        self.__rotor = 0
        self.__ratchet = 0
        self.__avalanche = 0
        self.__last_plain = 0
        self.__last_cipher = 0

    def hash_final(self, length):
        hash = []
        for i in range(255, -1, -1):
            self.decrypt(i)

        for i in range(length):
            hash.append(self.decrypt(0))

        return hash

    def __initialize(self, key):
        """Initializes self.__cards to be deterministically random

        Key size may be up to 256 bytes.
        Passphrases may be used directly, with longer length compensating for
        the low entropy expected in such keys.
        Alternatively, shorter keys hashed from a pass pharse or generated
        randomly may be used.
        For random keys, lengths of 4 to 16 bytes are recommended, depending
        on how secure you want this to be.

        Args:
            key (str): key to use for randomization (up to 256 bytes)
        """
        for i in range(256):
            self.__cards[i] = i

        self.__keypos = 0
        self.__rsum = 0
        for i in range(255,-1,-1):
            to_swap = self.__keyrand(i, key)
            swap_temp = self.__cards[i]
            self.__cards[i] = self.__cards[to_swap]
            self.__cards[to_swap] = swap_temp

        # Initialize the indices and data dependencies.
        # Indicies are set to different values instead of all 0
        # to reduce what is known about the state of the cards
        # when the first byte is emitted.
        self.__rotor = self.__cards[1]
        self.__ratchet = self.__cards[3]
        self.__avalanche = self.__cards[5]
        self.__last_plain = self.__cards[7]
        self.__last_cipher = self.__cards[self.__rsum]

        # Ensure no useful values to those that snoop
        to_swap = 0
        swap_temp = 0
        self.__rsum = 0
        self.__keypos = 0

    def __hash_init(self):
        """Initialize non-keyed hash computation."""
        # Initialize the indices and data dependencies.
        self.__rotor = 1
        self.__ratchet = 3
        self.__avalanche = 5
        self.__last_plain = 7
        self.__last_cipher = 11

        # Start with cards all in inverse order
        for i in range(256):
            self.__cards[i] = 255 - i

    def __keyrand(self, limit, key):
        if limit == 0:
            return 0  # Avoid divide by zero error

        retry_limiter = 0

        # Fill mask with enough bits to cover the desired range.
        mask = 1
        while mask < limit:
            mask = (mask << 1) + 1

        while True:
            # Convert a byte from the key to an int, but prevent sign extension
            # so -16 becomes 240
            # Also keep self.__rsum in the range of 0-255
            # The C++ code relied on overflow of an unsigned char
            self.__rsum = (self.__cards[self.__rsum] + (key[self.__keypos] & 0xFF)) & 0xFF
            self.__keypos += 1

            if self.__keypos >= len(key):
                self.__keypos = 0
                self.__rsum += len(key)
                self.__rsum &= 0xFF

            u = mask & self.__rsum

            retry_limiter += 1
            if retry_limiter > 11:
                u %= limit  # Prevent very rare long loops

            if not u > limit:
                break
        return u

    def __shuffle(self):
        # Shuffle the deck a little more.
        self.__ratchet += self.__cards[self.__rotor]
        self.__rotor += 1
        # Keep ratchet and rotor in range of 0-255
        # The C++ code relied on overflow of an unsigned char
        self.__ratchet &= 0xFF
        self.__rotor &= 0xFF

        swaptemp = self.__cards[self.__last_cipher]
        self.__cards[self.__last_cipher] = self.__cards[self.__ratchet]
        self.__cards[self.__ratchet] = self.__cards[self.__last_plain]
        self.__cards[self.__last_plain] = self.__cards[self.__rotor]
        self.__cards[self.__rotor] = swaptemp
        self.__avalanche += self.__cards[swaptemp]
        # Keep self.__avalanche in the range of 0-255
        self.__avalanche &= 0xFF

    def __get_hidden_byte(self, b_val):
        return (
            b_val
            ^ self.__cards[
                (self.__cards[self.__ratchet] + self.__cards[self.__rotor]) & 0xFF
                ]
            ^ self.__cards[
                self.__cards[
                    (self.__cards[self.__last_plain]
                    + self.__cards[self.__last_cipher]
                    + self.__cards[self.__avalanche]) & 0xFF
                    ]
                ]
        )
