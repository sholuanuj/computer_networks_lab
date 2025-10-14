import random
import time

class StopAndWaitARQ:
    """
    A simulator for the Stop-and-Wait ARQ protocol.
    """

    def __init__(self, total_frames=5, loss_prob=0.3, timeout=2):
        """
        Initializes the simulator.

        Args:
            total_frames (int): The total number of frames to transmit.
            loss_prob (float): The probability of a frame being lost (0.0 to 1.0).
            timeout (int): The timeout duration in seconds.
        """
        self.total_frames = total_frames
        self.loss_prob = loss_prob
        self.timeout = timeout
        self.current_frame = 0

    def simulate(self):
        """
        Runs the Stop-and-Wait ARQ simulation.
        """
        print("--- Starting Stop-and-Wait ARQ Simulation ---")
        while self.current_frame < self.total_frames:
            self.send_frame(self.current_frame)
            
            # Simulate waiting for acknowledgment with a timeout
            ack_received = self.wait_for_ack()

            if ack_received:
                print(f"ACK {self.current_frame} received.")
                self.current_frame += 1
            else:
                # Timeout occurred, retransmit the frame
                print(f"Timeout for Frame {self.current_frame}, retransmitting...")
        
        print("\n--- Simulation Complete ---")

    def send_frame(self, frame_number):
        """
        Simulates sending a frame.
        """
        print(f"\nSending Frame {frame_number}")

    def wait_for_ack(self):
        """
        Simulates waiting for an ACK.
        
        Returns:
            bool: True if ACK is received, False if frame is lost (timeout).
        """
        # Simulate a delay for transmission and processing
        time.sleep(1) 

        # Simulate frame loss based on the loss probability
        if random.random() < self.loss_prob:
            print(f"Frame {self.current_frame} lost on its way to the receiver.")
            return False
        
        # Simulate ACK loss (can be modeled same as frame loss)
        if random.random() < self.loss_prob:
            print(f"ACK for Frame {self.current_frame} lost on its way back.")
            return False

        return True


if __name__ == "__main__":
    # You can adjust parameters here
    simulation = StopAndWaitARQ(total_frames=5, loss_prob=0.3)
    simulation.simulate()