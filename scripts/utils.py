import struct
import simplepyble

# Define a function to decode a byte array to multiple floats
def bytes_to_floats(byte_data):
    # Assuming byte_data is a bytes object
    # 'f' format specifier denotes a single precision float (4 bytes)
    # Calculate the number of floats by dividing the total length of byte_data by 4
    num_floats = len(byte_data) // 4
    # Use struct.unpack to convert bytes to floats
    # 'f' format specifier denotes a single precision float (4 bytes)
    floats = struct.unpack('<{}f'.format(num_floats), byte_data)
    floats_list = list(floats)  # Convert tuple to list
    return floats_list

def initialize_bt(mac=None, uuid = None):
    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    # Query the user to pick an adapter
    print("Please select an adapter:")
    for i, adapter in enumerate(adapters):
        print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    # choice = int(input("Enter choice: "))
    choice = 0
    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    # adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    # Scan for 3 seconds
    adapter.scan_for(3000)
    peripherals = adapter.scan_get_results()

    # Query the user to pick a peripheral
    print("About to query user to pick a peripheral")
    if mac is None:
        print("Please select a peripheral:")
        for i, peripheral in enumerate(peripherals):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")

        choice = int(input("Enter choice: "))
        peripheral = peripherals[choice]
    else:
        for i, peripheral in enumerate(peripherals):
            if peripheral.address() == mac:
                choice = i
                peripheral = peripherals[choice]
                break

    print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
    peripheral.connect()

    print("Successfully connected, listing services...")
    services = peripheral.services()
    service_characteristic_pair = []
    for service in services:
        for characteristic in service.characteristics():
            service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

    # Query the user to pick a service/characteristic pair
    if uuid is None:
        print("Please select a service/characteristic pair:")
        for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
            print(f"{i}: {service_uuid} {characteristic}")
        choice = int(input("Enter choice: "))
    else:
        for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
            if service_uuid == uuid:
                choice = i
                break

    service_uuid, characteristic_uuid = service_characteristic_pair[choice]

    return peripheral, service_uuid, characteristic_uuid