from attrs import define 
from dbus_fast import DBusError
from dbus_fast.service import ServiceInterface, dbus_method

@define
class CharacteristicData:
    value: bytes = bytes([0x01, 0x02])

    def read(self, offset: int = 0):
        if (offset < 0 or offset > len(self.value)):
            raise ValueError("Invalid offset")
        return self.value[offset:]

class CharactericInterface(ServiceInterface):
    def __init__(self, data: CharacteristicData):
        super().__init__("org.bluez.GattCharacteristic1")
        self.data = data 

    @dbus_method(name = "ReadValue")
    def read_value(self, options: "a{sv}") -> "ay":
        offset_variant = options.get("offset")
        offset = 0 if offset_variant is None else offset_variant.value 

        try:
            return self.data.read(offset)
        except ValueError as e:
            raise DBusError("org.bluez.Error.InvalidOffset", str(e)) from e