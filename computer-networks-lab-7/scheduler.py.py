

# The 'dataclass' decorator automatically creates methods like
# __init__, __repr__ (for printing), etc.
# This is perfect for a simple data container like Packet.
from dataclasses import dataclass
from typing import List

# 1. Class: Packet
@dataclass
class Packet:
    """
    A simple dataclass to represent a network packet.

    Attributes:
        source_ip (str): The IP address of the sender.
        dest_ip (str): The IP address of the recipient.
        payload (str): The data content of the packet.
        priority (int): The priority level (0=High, 1=Medium, 2=Low).
    """
    source_ip: str
    dest_ip: str
    payload: str
    priority: int

# 2. Function: fifo_scheduler
def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Simulates a First-Come, First-Served (FCFS/FIFO) scheduler.

    Args:
        packet_list: A list of Packet objects in the order
                     they arrived at the queue.

    Returns:
        A new list of Packet objects in the order they would be sent.
        For FIFO, this is identical to the arrival order.
    """
    # Since the input list is *already* in arrival order,
    # a FIFO scheduler simply processes them in that exact order.
    # We return a copy to be non-destructive (i.e., we don't
    # modify the original list).
    return packet_list.copy()

# 3. Function: priority_scheduler
def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Simulates a non-preemptive Priority Scheduler.

    Args:
        packet_list: A list of Packet objects that are in the queue.

    Returns:
        A new list of Packet objects sorted by their priority.
        Packets with a lower priority number (e.g., 0) are sent first.
    """
    # We use Python's built-in sorted() function.
    # 'key=lambda p: p.priority' tells sorted() to look at the
    # 'priority' attribute of each Packet object (p) for sorting.
    # Since lower numbers mean higher priority, the default
    # ascending sort (0, 1, 2) is exactly what we want.
    return sorted(packet_list, key=lambda p: p.priority)

# --- Test Case from the assignment ---
if __name__ == "__main__":
    print("--- Testing Output Port Schedulers ---")

    # Create the list of packets as per the test case.
    # We use placeholder IPs, as they don't affect scheduling logic.
    packet_list = [
        Packet(source_ip="10.0.0.1", dest_ip="192.168.1.1", payload="Data Packet 1", priority=2), # Low
        Packet(source_ip="10.0.0.2", dest_ip="192.168.1.2", payload="Data Packet 2", priority=2), # Low
        Packet(source_ip="20.0.0.1", dest_ip="192.168.1.3", payload="VOIP Packet 1", priority=0), # High
        Packet(source_ip="30.0.0.1", dest_ip="192.168.1.4", payload="Video Packet 1", priority=1), # Medium
        Packet(source_ip="20.0.0.2", dest_ip="192.168.1.3", payload="VOIP Packet 2", priority=0)  # High
    ]

    print("Original arrival order (Payload / Priority):")
    for pkt in packet_list:
        print(f"  - {pkt.payload} (Priority: {pkt.priority})")

    # --- Test FIFO ---
    print("\n--- Testing FIFO Scheduler ---")
    fifo_result = fifo_scheduler(packet_list)

    # Extract just the payloads for easy verification
    fifo_payloads = [p.payload for p in fifo_result]

    print("Packets as sent by FIFO:")
    print(f"  -> {fifo_payloads}")

    expected_fifo = ["Data Packet 1", "Data Packet 2", "VOIP Packet 1", "Video Packet 1", "VOIP Packet 2"]
    print(f"Expected order:")
    print(f"  -> {expected_fifo}")
    assert fifo_payloads == expected_fifo
    print("FIFO Test: SUCCESS\n")

    # --- Test Priority ---
    print("--- Testing Priority Scheduler ---")
    priority_result = priority_scheduler(packet_list)

    # Extract just the payloads for easy verification
    priority_payloads = [p.payload for p in priority_result]

    print("Packets as sent by Priority:")
    print(f"  -> {priority_payloads}")

    expected_priority = ["VOIP Packet 1", "VOIP Packet 2", "Video Packet 1", "Data Packet 1", "Data Packet 2"]
    print(f"Expected order:")
    print(f"  -> {expected_priority}")
    assert priority_payloads == expected_priority
    print("Priority Test: SUCCESS")