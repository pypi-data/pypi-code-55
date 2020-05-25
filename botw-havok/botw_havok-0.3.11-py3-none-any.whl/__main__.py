from . import Havok


hk = Havok.from_file("/home/kreny/IbutsuFireBody.wiiu.hkrb")
hk.deserialize()
hk.serialize()
hk.to_file("/home/kreny/IbutsuFireBody.wiiu.new.hkrb")

print()
