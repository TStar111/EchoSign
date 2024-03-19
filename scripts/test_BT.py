# import asyncio
# from bleak import BleakClient

# ADDRESS = "02:81:b7:4b:04:26"  # Replace with the address of your Arduino Nano BLE
# SERVICE_UUID = "12345678-1234-1234-1234-123456789ABC"
# CHARACTERISTIC_UUID = "12345678-1234-1234-1234-123456789ABC"

# async def receive_data(address):
#     async with BleakClient(address) as client:
#         print("Before connect")
#         try:
#             await client.connect()
#         except Exception as e:
#             print("Error:", e)
#         print("After connect")
#         value = await client.read_gatt_char(CHARACTERISTIC_UUID)
#         received_data = value.decode('utf-8')  # Decode bytes to string
#         print("Received:", received_data)
#         float_values = [float(x) for x in received_data.split(',')]
#         print("Float values:", float_values)

# async def main():
#     await receive_data(ADDRESS)

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import sys
import time

from bleak import *
#from bleak import BleakScanner, BleakClient
#from bleak.backends.scanner import AdvertisementData
import struct

# Define a function to decode a byte array to multiple floats
def bytes_to_floats(byte_data):
    # Assuming byte_data is a bytes object
    # 'f' format specifier denotes a single precision float (4 bytes)
    # Calculate the number of floats by dividing the total length of byte_data by 4
    num_floats = len(byte_data) // 4
    # Use struct.unpack to convert bytes to floats
    # 'f' format specifier denotes a single precision float (4 bytes)
    floats = struct.unpack('<{}f'.format(num_floats), byte_data)
    return floats

# Example usage:
# byte_data = b'\x00\x00\xa0\x42\x00\x00\x00\x43\x00\x00\x80\x44\x00\x00\xa0\x44\x00\x00\x00\x45'  # Example byte array
# decoded_floats = bytes_to_floats(byte_data)
# print(decoded_floats)  # Output: (100.0, 103.0, 128.0, 160.0, 165.0)



CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
address = "02:81:b7:4b:04:26" # MAC addres of the remove ble device

async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        if client.is_connected():
            print('I\'m connected to the device ! ')

        while True:
            value = await client.read_gatt_char(CHARACTERISTIC_UUID)
            received_data = bytes_to_floats(value)
            print("Received:", received_data)
    except Exception as e:
        print(e)

asyncio.run(main(address))