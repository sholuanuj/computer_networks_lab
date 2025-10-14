import random
import time

class GoBackNARQ:
    """
    A simulator for the Go-Back-N ARQ protocol.
    """

    def __init__(self, total_frames, window_size, loss_prob):
        """
        Initializes the simulator.

        Args:
            total_frames (int): The total number of frames to transmit.
            window_size (int): The size of the sending window (N).
            loss_prob (float): The probability of a frame being lost.
        """
        self.total_frames = total_frames
        self.window_size = window_size
        self.loss_prob = loss_prob
        self.base = 0  # Sequence number of the oldest unacknowledged frame
        self.next_seq_num = 0  # Sequence number of the next frame to be sent
        self.buffer = {} # Stores frames that have been sent but not yet acknowledged

    def simulate(self):
        """
        Runs the Go-Back-N ARQ simulation.
        """
        print(f"--- Starting Go-Back-N ARQ Simulation (Window Size = {self.window_size}) ---")

        while self.base < self.total_frames:
            # Send all frames within the current window
            while self.next_seq_num < self.base + self.window_size and self.next_seq_num < self.total_frames:
                self.send_frame(self.next_seq_num)
                self.next_seq_num += 1

            # Simulate waiting for ACKs and potential timeout
            ack_received = self.wait_for_ack()

            if ack_received is not None:
                print(f"Cumulative ACK {ack_received} received. Window slides.")
                self.base = ack_received + 1
            else:
                # Timeout occurred
                print(f"\nTimeout! Frame {self.base} lost or its ACK lost.")
                print(f"Retransmitting frames from {self.base} to {self.next_seq_num - 1}...")
                self.next_seq_num = self.base # Reset next_seq_num to start retransmission
        
        print("\n--- Simulation Complete ---")

    def send_frame(self, frame_number):
        """
        Simulates sending a single frame.
        """
        print(f"Sending Frame {frame_number}...")
        self.buffer[frame_number] = "SENT"
        time.sleep(0.5)

    def wait_for_ack(self):
        """
        Simulates the receiver's response and the wait for a cumulative ACK.
        
        Returns:
            int or None: The sequence number of the cumulative ACK received, 
                         or None if a timeout is simulated.
        """
        # Decide which frames are "lost" in this transmission round
        lost_frame = -1
        for i in range(self.base, self.next_seq_num):
            if random.random() < self.loss_prob:
                lost_frame = i
                print(f"Frame {i} was lost!")
                break
        
        # If a frame was lost, receiver only acknowledges frames up to lost_frame - 1
        if lost_frame != -1:
            if lost_frame == self.base: # The first frame in the window was lost
                return None # Simulates a timeout, no ACK is received
            else:
                # A later frame was lost, so a cumulative ACK for the one before it is sent
                return lost_frame - 1
        else:
            # No loss, cumulative ACK for the whole window is received
            return self.next_seq_num - 1

if __name__ == "__main__":
    # Adjustable parameters [cite: 34]
    TOTAL_FRAMES = 10
    WINDOW_SIZE = 4
    LOSS_PROBABILITY = 0.2

    simulation = GoBackNARQ(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)
    simulation.simulate()