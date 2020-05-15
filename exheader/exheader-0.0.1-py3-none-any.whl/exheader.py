import struct


class Exheader:

    class SCI:
        class CodeSetInfo:
            DATA_SIZE = 0xC

            def __init__(self):
                self.address = 0
                self.page_num = 0
                self.size = 0

            def unpack_from(self, data, offset=0):
                (self.address,
                 self.page_num,
                 self.size) = struct.unpack_from('<III', data, offset)

            def pack_into(self, data, offset=0):
                struct.pack_into('<III', data, offset,
                 self.address,
                 self.page_num,
                 self.size)

        class SystemInfo:
            DATA_SIZE = 0x40

            def __init__(self):
                self.save_data_size = 0
                self.jump_id = 0

            def unpack_from(self, data, offset=0):
                (self.save_data_size,
                 self.jump_id) = struct.unpack_from('<QQ', data, offset)

            def pack_into(self, data, offset=0):
                struct.pack_into('<QQ', data, offset,
                 self.save_data_size,
                 self.jump_id)
                data[offset+0x10:offset+self.DATA_SIZE] = b'\0' * 0x30

        DATA_SIZE = 0x200

        def __init__(self):
            self.app_title = "CtrApp"
            self.is_compress_code = False
            self.is_sd_app = False
            self.remaster_version = 0
            self.section_text = self.CodeSetInfo()
            self.stack_size = 0
            self.section_ro = self.CodeSetInfo()
            self.section_data = self.CodeSetInfo()
            self.bss_size = 0
            self.dependency_modules = []
            self.system_info = self.SystemInfo()
        
        def unpack_from(self, data, offset=0):
            (app_title_raw,
             flags,
             self.remaster_version,
             self.stack_size,
             self.bss_size) = struct.unpack_from('<8s5xBH12xI28xI', data, offset)

            self.app_title = app_title_raw.decode('ascii')
            self.is_compress_code = flags & 1
            self.is_sd_app = (flags >> 1) & 1

            self.section_text.unpack_from(data, offset+0x10)
            self.section_ro.unpack_from(data, offset+0x20)
            self.section_data.unpack_from(data, offset+0x30)

            self.dependency_modules.clear()
            for i in range(48):
                module = struct.unpack_from('<Q', data, offset + 0x40 + i*8)[0]
                if module != 0:
                    self.dependency_modules.append(module)

            self.system_info.unpack_from(data, offset+0x1C0)

        def pack_into(self, data, offset=0):
            struct.pack_into('<8s5xBH12xI28xI', data, offset,
             self.app_title.encode('ascii'),
             self.is_compress_code | self.is_sd_app<<1,
             self.remaster_version,
             self.stack_size,
             self.bss_size)
            
            self.section_text.pack_into(data, offset+0x10)
            self.section_ro.pack_into(data, offset+0x20)
            self.section_data.pack_into(data, offset+0x30)

            for i in range(48):
                if i >= len(self.dependency_modules):
                    struct.pack_into('<Q', data, offset + 0x40 + i*8, 0)
                else:
                    struct.pack_into('<Q', data, offset + 0x40 + i*8, self.dependency_modules[i])
            
            self.system_info.pack_into(data, offset+0x1C0)

    class ACI:
        class Arm11SystemLocalCapabilities:
            DATA_SIZE = 0x170

            def __init__(self):
                self.title_id = 0
                self.core_version = 0
                self.use_cpu_clockrate_804MHz = False
                self.enable_l2c = False
                self.n3ds_system_mode = 0
                self.ideal_processor = 0
                self.affinity_mask = 0
                self.o3ds_system_mode = 0
                self.priority = 0
                self.max_cpu_time = 0
                self.extdata_id = 0
                self.savedata_ids = 0
                self.accessible_savedata_ids = 0
                self.fs_access_info = 0
                self.no_romfs = False
                self.use_extended_savedata_access = False

                self.service_access = []
                self.reslimit_category = 0

            def unpack_from(self, data, offset=0):
                (self.title_id,
                 self.core_version,
                 flag1,
                 flag2,
                 flag0,
                 self.priority,
                 self.max_cpu_time,
                 self.extdata_id,
                 self.savedata_ids,
                 self.accessible_savedata_ids,
                 self.fs_access_info,
                 flags_fs_other) = struct.unpack_from('<QIBBBBB31xQQQII', data, offset)

                self.use_cpu_clockrate_804MHz     = (flag1 >> 0) & 1
                self.enable_l2c                   = (flag1 >> 1) & 1
                self.n3ds_system_mode             = (flag2 >> 0) & 15
                self.ideal_processor              = (flag0 >> 0) & 3
                self.affinity_mask                = (flag0 >> 2) & 3
                self.o3ds_system_mode             = (flag0 >> 4) & 15
                self.no_romfs                     = (flags_fs_other >> 24) & 1
                self.use_extended_savedata_access = (flags_fs_other >> 25) & 1

                self.service_access.clear()
                for i in range(34):
                    srv = struct.unpack_from('<8s', data, offset + 0x50 + i*8)[0].decode('ascii').rstrip('\x00')
                    if srv:
                        self.service_access.append(srv)
                
                self.reslimit_category = struct.unpack_from('<B', data, offset+0x16F)[0]

            def pack_into(self, data, offset=0):
                flag1 = self.use_cpu_clockrate_804MHz | self.enable_l2c << 1
                flag2 = self.n3ds_system_mode
                flag0 = self.ideal_processor | self.affinity_mask << 2 | self.o3ds_system_mode << 4
                flags_fs_other = self.no_romfs << 24 | self.use_extended_savedata_access >> 25

                struct.pack_into('<QIBBBBB31xQQQII', data, offset,
                 self.title_id,
                 self.core_version,
                 flag1,
                 flag2,
                 flag0,
                 self.priority,
                 self.max_cpu_time,
                 self.extdata_id,
                 self.savedata_ids,
                 self.accessible_savedata_ids,
                 self.fs_access_info,
                 flags_fs_other)
                
                for i in range(34):
                    if i >= len(self.service_access):
                        struct.pack_into('<8s', data, offset + 0x50 + i*8, b'\0')
                    else:
                        struct.pack_into('<8s', data, offset + 0x50 + i*8, self.service_access[i].encode('ascii'))
                
                data[offset+0x160:offset+0x16F] = b'\0' * 0xF
                struct.pack_into('<B', data, offset+0x16F, self.reslimit_category)                  

        class Arm11KernelCapabilities:
            DATA_SIZE = 0x80

            class MapRange:
                def __init__(self, start=0, end=0, read_only=False):
                    self.start = start
                    self.end = end
                    self.read_only = read_only

            def __init__(self):
                # category  4
                self.svcs = set()

                # category 6
                self.kernel_ver_major = 0
                self.kernel_ver_minor = 0

                # category 7
                self.handle_table_size = 0

                # category 8
                self.allow_debug = False
                self.force_debug = False
                self.allow_non_alphanum = False
                self.shared_page_writing = False
                self.privilege_priority = False
                self.allow_main_args = False
                self.shared_device_memory = False
                self.runnable_on_sleep = False
                self.memory_type = 0
                self.special_memory = False
                self.has_core2_access = False

                # category 9
                self.map_ranges = []

            def unpack_from(self, data, offset):
                self.__init__() # reset all

                i = 0
                while i < 28:
                    descriptor = struct.unpack_from('<I', data, offset + i*4)[0]
                    if descriptor == 0xFFFFFFFF:
                        i += 1
                        continue

                    if (descriptor>>27) == 0b11110:
                        idx = (descriptor >> 24) & 7
                        for j in range(24):
                            if descriptor & (1 << j):
                                self.svcs.add(j + idx*24)

                    elif (descriptor>>25) == 0b1111110:
                        self.kernel_ver_major = (descriptor >> 8) & 0xFF
                        self.kernel_ver_minor = (descriptor >> 0) & 0xFF
                    
                    elif (descriptor>>24) == 0b11111110:
                        self.handle_table_size = descriptor & 0x7FFFF

                    elif (descriptor>>23) == 0b111111110:
                        self.allow_debug            = (descriptor >> 0) & 1
                        self.force_debug            = (descriptor >> 1) & 1
                        self.allow_non_alphanum     = (descriptor >> 2) & 1
                        self.shared_page_writing    = (descriptor >> 3) & 1
                        self.privilege_priority     = (descriptor >> 4) & 1
                        self.allow_main_args        = (descriptor >> 5) & 1
                        self.shared_device_memory   = (descriptor >> 6) & 1
                        self.runnable_on_sleep      = (descriptor >> 7) & 1
                        self.memory_type            = (descriptor >> 8) & 15
                        self.special_memory         = (descriptor >> 12) & 1
                        self.has_core2_access       = (descriptor >> 13) & 1
                    
                    elif (descriptor>>21) == 0b11111111100:
                        if i >= 27:
                            raise Exception('Unmatched map range start')

                        i += 1
                        end_descriptor = struct.unpack_from('<I', data, offset + i*4)[0]
                        if (end_descriptor>>21) != 0b11111111100:
                            raise Exception('Unmatched map range start')
                        
                        self.map_ranges.append(self.MapRange(descriptor & 0xFFFFF, end_descriptor & 0xFFFFF, (descriptor >> 20) & 1))

                    else:
                        raise Exception('Unimplemented descriptor: %08X' % descriptor)

                    i += 1

            def pack_into(self, data, offset=0):
                descriptors = []
                
                for i in range(7):
                    svc_mask = 0
                    for j in range(24):
                        if (i*24 + j) in self.svcs:
                            svc_mask |= 1 << j
                    if svc_mask:
                        descriptors.append((0b11110 << 27) | (i << 24) | svc_mask)

                for i in self.map_ranges:
                    descriptors.append((0b11111111100 << 21) | (i.read_only << 20) | i.start)
                    descriptors.append((0b11111111100 << 21) | (i.read_only << 20) | i.end)

                kernel_flags = (self.allow_debug << 0) | (self.force_debug << 1) | (self.allow_non_alphanum << 2) \
                               | (self.shared_page_writing << 3) | (self.privilege_priority << 4) | (self.allow_main_args << 5) \
                               | (self.shared_device_memory << 6) | (self.runnable_on_sleep << 7) | (self.memory_type << 8) \
                               | (self.special_memory << 12) | (self.has_core2_access << 13)

                descriptors.append((0b111111110 << 23) | kernel_flags)

                descriptors.append((0b11111110 << 24) | self.handle_table_size)

                descriptors.append((0b1111110 << 25) | self.kernel_ver_major << 8 | self.kernel_ver_minor)

                if len(descriptors) >= 28:
                    raise Exception('Number of ARM11 kernel capability descriptors out of bounds')

                for i in range(28):
                    if i >= len(descriptors):
                        struct.pack_into('<I', data, offset + i*4, 0xFFFFFFFF)
                    else:
                        struct.pack_into('<I', data, offset + i*4, descriptors[i])
                data[offset+0x70:offset+0x80] = b'\0' * 0x10
                
        class Arm9AccessControl:
            DATA_SIZE = 0x10

            def __init__(self):
                self.descriptors = bytearray(15)
                self.descriptor_version = 0

            def unpack_from(self, data, offset):
                self.descriptors = data[offset:offset+15]
                self.descriptor_version = struct.unpack_from('<B', data, offset+15)[0]

            def pack_into(self, data, offset=0):
                data[offset:offset+15] = self.descriptors
                struct.pack_into('<B', data, offset+15, self.descriptor_version)

        DATA_SIZE = 0x200

        def __init__(self):
            self.arm11_local_caps = self.Arm11SystemLocalCapabilities()
            self.arm11_kernel_caps = self.Arm11KernelCapabilities()
            self.arm9_access_ctrl = self.Arm9AccessControl()

        def unpack_from(self, data, offset=0):
            self.arm11_local_caps.unpack_from(data, offset)
            self.arm11_kernel_caps.unpack_from(data, offset+0x170)
            self.arm9_access_ctrl.unpack_from(data, offset+0x1F0)

        def pack_into(self, data, offset=0):
            self.arm11_local_caps.pack_into(data, offset)
            self.arm11_kernel_caps.pack_into(data, offset+0x170)
            self.arm9_access_ctrl.pack_into(data, offset+0x1F0)


    DATA_SIZE = 0x800

    def __init__(self):
        self.sci = self.SCI()
        self.aci = self.ACI()
        self.access_desc_rsa_sig = bytearray(0x100)
        self.ncch_rsa_key = bytearray(0x100)
        self.aci_2 = self.ACI()

    def unpack_from(self, data, offset=0):
        self.sci.unpack_from(data, offset)
        self.aci.unpack_from(data, offset+0x200)
        self.access_desc_rsa_sig = data[offset+0x400:offset+0x500]
        self.ncch_rsa_key = data[offset+0x500:offset+0x600]
        self.aci_2.unpack_from(data, offset+0x600)

    def pack_into(self, data, offset=0):
        self.sci.pack_into(data, offset)
        self.aci.pack_into(data, offset+0x200)
        data[offset+0x400:offset+0x500] = self.access_desc_rsa_sig
        data[offset+0x500:offset+0x600] = self.ncch_rsa_key
        self.aci_2.pack_into(data, offset+0x600)

    def pack(self):
        data = bytearray(self.DATA_SIZE)
        self.pack_into(data)
        return data
