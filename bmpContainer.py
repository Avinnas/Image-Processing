import random

class bmpContainer:
    def __init__(self, path):
        self.data = self.load_image(path)

        self.size_real = self.data.__len__()
        self.size_in_header = int.from_bytes(self.data[2:6], "little")
        self.array_offset = int.from_bytes(self.data[10:14], "little")
        self.DIB_header_size = int.from_bytes(self.data[14:18], "little")

        self.type_of_header = self.detect_type_of_header()

        if self.type_of_header == "INFO":
            self.width = int.from_bytes(self.data[18:22], "little")
            self.height = int.from_bytes(self.data[22:26], "little")
            self.bits_ppx = int.from_bytes(self.data[28:30], "little")
            self.compression = int.from_bytes(self.data[30:34], "little")
            self.raw_size = int.from_bytes(self.data[34:38], "little")
            self.number_of_colors = int.from_bytes(self.data[46:50], "little")
            if self.DIB_header_size > 108:
                self.ICC_profiles_offset = self.data[126:130]
                self.ICC_profiles_size = self.data[130:134]

    def show_data(self):
        print("Real size of file {}B \n".format(self.data.__len__()))
        print("Type of file: ", self.data[0:2].decode("ASCII"))
        print("Size of image: {}B".format(int.from_bytes(self.data[2:6], "little")))
        print("Reserved 1: {}".format(int.from_bytes(self.data[6:8], "little")))
        print("Reserved 2: {}".format(int.from_bytes(self.data[8:10], "little")))
        print("Array of pixels offset: {}B".format(int.from_bytes(self.data[10:14], "little")))
        print("DIB header size: {}B".format(int.from_bytes(self.data[14:18], "little")))
        if self.type_of_header == "INFO":
            self.show_info_header_data()

    def show_info_header_data(self):
        print("Width of image: {}".format(int.from_bytes(self.data[18:22], "little")))
        print("Height of image: {}".format(int.from_bytes(self.data[22:26], "little")))
        print("Number of color planes: {}".format(int.from_bytes(self.data[26:28], "little")))
        print("Bits per pixel: {}b".format(int.from_bytes(self.data[28:30], "little")))
        print("Compression method: {}".format(int.from_bytes(self.data[30:34], "little")))
        print("Raw image size: {}B - if 0 then uncompressed".format(int.from_bytes(self.data[34:38], "little")))
        print(
            "Horizontal resolution: {} pixel per metre".format(int.from_bytes(self.data[38:42], "little", signed=True)))
        print("Vertical resolution: {} pixel per metre".format(int.from_bytes(self.data[42:46], "little", signed=True)))
        print("Number of colors: {} - if 0 then 2^(bits per pixel)".format(int.from_bytes(self.data[46:50], "little")))
        print("Important colors: {} ".format(int.from_bytes(self.data[50:54], "little")))
        if(self.DIB_header_size > 40):
            print("Red channel bit mask: {}".format(self.data[54:58]))
            print("Green channel bit mask: {}".format(self.data[58:62]))
            print("Blue channel bit mask: {}".format(self.data[62:66]))
        if self.DIB_header_size > 52:
            print("Red channel bit mask: {}".format(self.data[66:70]))
        if self.DIB_header_size > 56:
            print("Color space: {}".format(self.data[70:74].decode("ASCII")))
            print("Color Endpoints: {}".format(self.data[74:110]))
            print("Red Gamma Correction: {}".format(self.data[110:114]))
            print("Green Gamma Correction: {}".format(self.data[114:118]))
            print("Blue gamma correction: {}".format(self.data[118:122]))
        if self.DIB_header_size > 108:
            print("Rendering Intent: {}".format(self.data[122:126].decode("ASCII")))
            print("ICC profiles Offset {}B - from DIB header".format(int.from_bytes(self.data[126:130],"little")))
            print("ICC profiles size {}B".format(int.from_bytes(self.data[130:134],"little")))
            print("Reserved space {}".format(int.from_bytes(self.data[134:138],"little")))




    def detect_type_of_header(self):
        if self.DIB_header_size == 12 | self.DIB_header_size == 16 | self.DIB_header_size == 64:
            return "OS"
        else:
            return "INFO"

    def remove_data_from_header(self):
        temp = 0
        self.data[6:10] = temp.to_bytes(4, "little")
        if self.type_of_header == "INFO":
            self.data[38:46] = temp.to_bytes(8, "little")
            if self.DIB_header_size == 124:
                self.data[134:138] = temp.to_bytes(4, "little")


    def remove_first_gap(self):
        header_size = 14
        color_palette = self.calculate_color_palette_size()
        extra_bit_masks = self.calculate_extra_bit_masks_size()

        proper_offset = header_size + self.DIB_header_size + color_palette + extra_bit_masks

        if proper_offset != self.array_offset:
            self.remove_bytes(proper_offset, self.array_offset, proper_offset)

    def update_size(self):
        self.size_real = self.data.__len__()
        self.size_in_header = self.size_real
        self.data[2:6] = self.size_real.to_bytes(4, "little")

    def update_pixels_offset(self, proper_offset):
        self.array_offset = proper_offset
        self.data[10:14] = proper_offset.to_bytes(4, "little")

    def remove_bytes(self, first_index, last_index, proper_offset = None):
        if proper_offset is None:
            proper_offset = self.array_offset
        del [self.data[first_index : last_index]]
        self.update_pixels_offset(proper_offset)
        self.update_size()

    def insert_random_bytes(self, index, number_of_bytes):
        if number_of_bytes> 31:
            a = random.randint(0, 2**31 -1)
        else:
            a = random.randint(0, 2**number_of_bytes - 1)

        information = a.to_bytes(number_of_bytes, "little")

        self.data[index:index] = information

        self.update_size()
        self.update_pixels_offset(self.array_offset + number_of_bytes)
        return information


    def calculate_color_palette_size(self):
        if self.bits_ppx > 8:
            return 0
        if self.number_of_colors != 0:
            return self.number_of_colors * 4
        else:
            return pow(2, self.bits_ppx) * 4

    def calculate_extra_bit_masks_size(self):
        if self.DIB_header_size != 40:
            return 0
        else:
            if self.compression == 3:
                return 12
            if self.compression == 6:
                return 16
            return 0

    def load_image(self, path):
        f = open(path, "rb")
        data = bytearray(f.read())
        f.close()
        return data

    def save_image(self, path):
        f = open(path, "wb")
        f.write(self.data)
        f.close()
