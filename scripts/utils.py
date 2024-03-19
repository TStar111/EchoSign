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