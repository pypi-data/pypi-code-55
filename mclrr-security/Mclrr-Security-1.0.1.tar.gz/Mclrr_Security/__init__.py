from random import randint
import math

class py_mclrr_security:
    
    __asciiString = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

    # version 1.0.1 of the package
    def Version(self):
        return [1,0,1]

    def Encode(self, password):
        return self.__Encode(password)

    def __Validation(self, password):
        for i in range(len(password)):
            if password[i] not in self.__asciiString:
                return False
        return 5 < len(password) < 21

    def __Encode(self, password):
        if not self.__Validation(password):
            raise Exception("Invalid Password format")
        final = []
        # Add the version on the first 3 numbers
        final.extend(self.Version())
        # Add the length of the password
        final.append(self.__Encode_Length(password))
        # Choose the encoder
        encoder = self.__Choose_Encoder()
        final.extend(encoder)
        # Encode the message
        for i in range(20):
            code = self.__Get_Code(encoder, i)
            temp = 0
            if i < len(password):
                temp = self.__asciiString.index(password[i]) * code
            else :
                temp = randint(0,95) * code
            final.extend([temp % 95, int((temp - temp % 95) / 95)])
        self.__Masking(final,password)
        return self.__To_Ascii(final)
    
    def __Get_Code(self, encoder, i):
        code = 0
        if i < 3:
            code = encoder[0]
        elif i < 6:
            code = encoder[1]
        elif i < 10:
            code = encoder[2]
        elif i < 14:
            code = encoder[3]
        elif i < 18:
            code = encoder[4]
        else:
            code = encoder[5]
        return code

    def __Encode_Length(self,password):
        l = len(password)
        l = l * l / 5
        l = l - l % 1
        return int(l)

    def __Choose_Encoder(self):
        encoder = []
        for _ in range(6):
            encoder.append(randint(1,94))
        return encoder
        
        
    def __To_Int_Array(self, str):
        result = []
        for i in range(len(str)):
            result.append(self.__asciiString.index(str[i]))
        return result      

    def __Masking(self, final, password):
        password_code = self.__To_Int_Array(password)
        for i in range(len(final)):
            final[i] = (final[i] + password_code[i % len(password)]) % 95

    def __To_Ascii(self, encoded):
        result = ''
        for i in encoded:
            result = result + self.__asciiString[i]
        return result

    # Check passwords

    def Check_Password(self, hash, password):
        return self.__Check_Password(hash, password)

    def __Check_Password(self, hash, password):
        encoded = self.__To_Int_Array(hash)
        # Unmasking
        self.__Unmasking(encoded,password)
        # Validators
        if not self.__Validation_Check(encoded, password):
            return False
        # Get Encoder
        encoder = encoded[4:10]
        # Decode Password
        for i in range(len(password)):
            code = self.__Get_Code(encoder, i)
            temp = encoded[10 + i * 2] + 95 * encoded[11 + i * 2]
            if temp / code != self.__asciiString.index(password[i]): 
                return False
        return True

    def __Unmasking(self, encoded, password):
        password_code = self.__To_Int_Array(password)
        for i in range(len(encoded)):
            encoded[i] = (encoded[i] - password_code[i % len(password_code)] + 95) % 95
    
    def __Validation_Check(self, encoded, password):
        return 5 < len(password) < 21 and self.__Decode_Length(encoded[3]) == len(password) and encoded[0] == 1 and encoded[1] == 0

    def __Decode_Length(self, length):
        return int(math.sqrt((length + 1) * 5))