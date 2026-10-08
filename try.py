from attrs import define 
from dbus_fast import DBusError
from dbus_fast.service import ServiceInterface, dbus_method, dbus_property
from dbus_fast.constants import PropertyAccess

@define
class CharacteristicData:
    value: bytes = bytes([0x01, 0x02])

    def read(self, offset: int = 0) -> bytes:
        if (offset < 0 or offset > len(self.value)):
            raise ValueError("Invalid offset")
        return self.value[offset:]

class CharacteristicInterface(ServiceInterface):
    def __init__(self, 
                 data: CharacteristicData, 
                 service_path: str,
                 uuid: str):
        super().__init__("org.bluez.GattCharacteristic1")
        self.data = data 
        self.service_path = service_path
        self.uuid = uuid

    @dbus_method(name = "ReadValue")
    def read_value(self, options: "a{sv}") -> "ay":
        offset_variant = options.get("offset")
        offset = 0 if offset_variant is None else offset_variant.value 

        try:
            return self.data.read(offset)
        except ValueError as e:
            raise DBusError("org.bluez.Error.InvalidOffset", str(e)) from e

    @dbus_property(access = PropertyAccess.READ)
    def Flags(self) -> "as":
        return ["read", "notify"]

    @dbus_property(access = PropertyAccess.READ)
    def Service(self) -> "o":
        return self.service_path

    @dbus_property(access = PropertyAccess.READ)
    def UUID(self) -> "s":
        return self.uuid