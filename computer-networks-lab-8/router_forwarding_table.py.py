

# Import the functions from your first file
try:
    from ip_utils import ip_to_binary, get_network_prefix
except ImportError:
    print("Error: Could not import from ip_utils.py.")
    print("Please make sure ip_utils.py is in the same directory.")
    exit(1)

class Router:
    """
    Simulates a router's forwarding table and LPM lookup process.
    """

    def __init__(self, routes: list):
        """
        Initializes the router with a list of routes.

        Args:
            routes: A list of tuples, where each tuple contains
                    (cidr_prefix_str, output_link_str).
                    e.g., [("223.1.1.0/24", "Link 0"), ...]
        """
        print("Initializing router...")
        # This list will store our processed, sorted forwarding table.
        # It will be a list of tuples: [(binary_prefix, output_link), ...]
        self.__forwarding_table = []

        # Call the private helper method to process the routes
        self.__build_forwarding_table(routes)
        print("Forwarding table built and sorted for Longest Prefix Match.")

    def __build_forwarding_table(self, routes: list):
        """
        (Private) Converts the human-readable routes into an internal,
        optimized format and sorts it for LPM.

        The table is sorted by prefix length, from longest (most specific)
        to shortest (least specific).
        """
        processed_table = []
        for cidr, link in routes:
            # Use our function from Part 1 to get the binary prefix
            binary_prefix = get_network_prefix(cidr)
            if "Error:" in binary_prefix:
                print(f"Skipping invalid route: {cidr} ({binary_prefix})")
                continue

            # Store the binary prefix and its corresponding link
            processed_table.append((binary_prefix, link))

        # --- This is the most critical step for LPM ---
        # We sort the list based on the *length* of the binary prefix (route[0]).
        # 'reverse=True' ensures that the longest prefixes (e.g., /24)
        # come *before* the shorter ones (e.g., /16).
        processed_table.sort(key=lambda route: len(route[0]), reverse=True)

        self.__forwarding_table = processed_table

    def route_packet(self, dest_ip: str) -> str:
        """
        Simulates the Longest Prefix Match (LPM) algorithm for a
        given destination IP address.

        Args:
            dest_ip: A dotted-decimal IP address string (e.g., "223.1.1.100").

        Returns:
            The output link string (e.g., "Link 0") for the *best*
            matching route, or "Default Gateway" if no match is found.
        """

        # (a) Convert the destination IP to its 32-bit binary representation
        binary_dest_ip = ip_to_binary(dest_ip)
        if "Error:" in binary_dest_ip:
            return f"Error: Invalid destination IP {dest_ip}"

        # (b) Iterate through your sorted internal forwarding table
        #     (from longest prefix to shortest)
        for binary_prefix, output_link in self.__forwarding_table:

            # (c) Check if the binary destination IP *starts with* the prefix
            if binary_dest_ip.startswith(binary_prefix):

                # (d) The *first* match we find is the longest match,
                #     so we can immediately return the link.
                return output_link

        # (e) If the loop finishes with no matches, return the default route
        return "Default Gateway"

# --- Test Case from the assignment ---
if __name__ == "__main__":
    print("--- Testing Router Longest Prefix Match ---")

    # The routes table from the assignment
    test_routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]

    # 1. Initialize the Router
    my_router = Router(test_routes)

    print("\n--- Internal Forwarding Table (Sorted by prefix length) ---")
    # Let's peek at the sorted table to confirm
    for prefix, link in my_router._Router__forwarding_table:
         print(f"  Prefix: {prefix:<25} (Length: {len(prefix):<2}) -> {link}")
    print("----------------------------------------------------------\n")

    # 2. Test Cases

    # Test 1: Should match the /24
    ip1 = "223.1.1.100"
    link1 = my_router.route_packet(ip1)
    print(f'Routing "{ip1}" -> {link1}')
    print(f'  Expected: Link 0 (Matches "223.1.1.0/24")\n')

    # Test 2: Should match the other /24
    ip2 = "223.1.2.5"
    link2 = my_router.route_packet(ip2)
    print(f'Routing "{ip2}" -> {link2}')
    print(f'  Expected: Link 1 (Matches "223.1.2.0/24")\n')

    # Test 3: The crucial LPM test
    ip3 = "223.1.250.1"
    link3 = my_router.route_packet(ip3)
    print(f'Routing "{ip3}" -> {link3}')
    print(f'  Expected: Link 4 (ISP) (Matches "223.1.0.0/16")\n')

    # Test 4: No match, should use default
    ip4 = "198.51.100.1"
    link4 = my_router.route_packet(ip4)
    print(f'Routing "{ip4}" -> {link4}')
    print(f'  Expected: Default Gateway (Matches no prefixes)\n')