

def ip_to_binary(ip_address: str) -> str:
    """
    Converts a standard dotted-decimal IP address string into a 32-bit binary string.

    Args:
        ip_address: A string in dotted-decimal format (e.g., "192.168.1.1").

    Returns:
        A 32-bit binary string, with each octet represented by 8 bits
        (e.g., "11000000101010000000000100000001").
    """
    # 1. Split the IP string by the '.' character to get a list of octets
    #    Example: "192.168.1.1" -> ["192", "168", "1", "1"]
    #
    # 2. For each octet string in the list:
    #    a. Convert it to an integer (e.g., "192" -> 192).
    #    b. Format it as an 8-bit binary string, padded with leading zeros.
    #       - f'{...:08b}' is a format specifier:
    #       - 'b' means binary
    #       - '08' means pad with leading '0's to a total width of 8.
    #       Example: 1 -> "00000001"
    #
    # 3. Join all the 8-bit binary strings together to form one 32-bit string.

    binary_octets = [f'{int(octet):08b}' for octet in ip_address.split('.')]
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    """
    Extracts the binary network prefix from a CIDR notation string.

    Args:
        ip_cidr: A string in CIDR format (e.g., "200.23.16.0/23").

    Returns:
        The network prefix portion of the address as a binary string
        (e.g., "11001000000101110001000").
    """
    # 1. Split the CIDR string at the '/' to separate the IP and the prefix length
    #    Example: "200.23.16.0/23" -> ("200.23.16.0", "23")
    try:
        ip_address, prefix_length_str = ip_cidr.split('/')
    except ValueError:
        return "Error: Invalid CIDR format. Expected 'IP/Prefix'."

    # 2. Convert the prefix length to an integer
    try:
        prefix_length = int(prefix_length_str)
        if not 0 <= prefix_length <= 32:
             raise ValueError("Prefix length must be between 0 and 32")
    except ValueError as e:
        return f"Error: Invalid prefix length. {e}"

    # 3. Use our first function to get the full 32-bit binary IP
    full_binary_ip = ip_to_binary(ip_address)

    # 4. Slice the full binary string to get only the first 'prefix_length' bits
    #    Example: full_binary_ip[:23]
    return full_binary_ip[:prefix_length]

# This special block runs only when you execute the script directly
# It's perfect for testing your functions
if __name__ == "__main__":
    print("--- Testing IP Utility Functions ---")

    # Test Case 1: From the assignment
    ip1 = "192.168.1.1"
    binary_ip1 = ip_to_binary(ip1)
    print(f'ip_to_binary("{ip1}"):')
    print(f'  -> {binary_ip1}')
    print(f'  Expected: 11000000101010000000000100000001\n')

    # Test Case 2: An IP with small numbers (to check zero padding)
    ip2 = "10.0.5.1"
    binary_ip2 = ip_to_binary(ip2)
    print(f'ip_to_binary("{ip2}"):')
    print(f'  -> {binary_ip2}')
    print(f'  Expected: 00001010000000000000010100000001\n')

    # Test Case 3: From the assignment
    cidr1 = "200.23.16.0/23"
    prefix1 = get_network_prefix(cidr1)
    print(f'get_network_prefix("{cidr1}"):')
    print(f'  -> {prefix1}')
    print(f'  Expected: 11001000000101110001000\n')

    # Test Case 4: A common /24 prefix
    cidr2 = "192.168.1.0/24"
    prefix2 = get_network_prefix(cidr2)
    print(f'get_network_prefix("{cidr2}"):')
    print(f'  -> {prefix2}')
    print(f'  Expected: 110000001010100000000001\n')

    # Test Case 5: A /16 prefix
    cidr3 = "172.16.0.0/16"
    prefix3 = get_network_prefix(cidr3)
    print(f'get_network_prefix("{cidr3}"):')
    print(f'  -> {prefix3}')
    print(f'  Expected: 1010110000010000\n')