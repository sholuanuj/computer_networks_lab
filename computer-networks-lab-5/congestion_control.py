import matplotlib.pyplot as plt

class TCPCongestionControl:
    """
    A simulator for TCP Congestion Window (cwnd) behavior.
    """

    def __init__(self, ssthresh_initial=16, max_rounds=50, timeout_round=20):
        """
        Initializes the simulator.
        
        Args:
            ssthresh_initial (int): Initial slow start threshold.
            max_rounds (int): Total number of transmission rounds to simulate.
            timeout_round (int): The round at which a timeout event occurs.
        """
        self.cwnd = 1  # Initial congestion window size
        self.ssthresh = ssthresh_initial
        self.max_rounds = max_rounds
        self.timeout_round = timeout_round
        self.cwnd_history = []

    def simulate(self):
        """
        Runs the TCP congestion control simulation.
        """
        print("--- Starting TCP Congestion Control Simulation ---")

        for round_num in range(1, self.max_rounds + 1):
            self.cwnd_history.append(self.cwnd)
            print(f"Round: {round_num:2d} | cwnd: {self.cwnd:4d} | ssthresh: {self.ssthresh:4d}")

            # Simulate a timeout event [cite: 47]
            if round_num == self.timeout_round:
                print(f"--- Timeout Event at Round {round_num} ---")
                self.ssthresh = self.cwnd // 2  # Multiplicative decrease [cite: 49]
                self.cwnd = 1  # Reset cwnd to 1
                continue

            # Check if in Slow Start or Congestion Avoidance phase
            if self.cwnd < self.ssthresh:
                # Slow Start phase: cwnd doubles (exponential growth)
                self.cwnd *= 2
            else:
                # Congestion Avoidance phase: cwnd increases by 1 (linear growth)
                self.cwnd += 1
        
        print("\n--- Simulation Complete ---")
        self.plot_results()

    def plot_results(self):
        """
        Plots the cwnd size versus transmission rounds. 
        """
        rounds = list(range(1, self.max_rounds + 1))
        
        plt.figure(figsize=(12, 6))
        plt.plot(rounds, self.cwnd_history, marker='o', linestyle='-', label='cwnd')
        
        # Mark the timeout event
        plt.axvline(x=self.timeout_round, color='r', linestyle='--', label=f'Timeout at Round {self.timeout_round}')
        
        plt.title('TCP Congestion Window (cwnd) Simulation')
        plt.xlabel('Transmission Round')
        plt.ylabel('Congestion Window Size (cwnd)')
        plt.grid(True)
        plt.legend()
        plt.xticks(range(0, self.max_rounds + 1, 5))
        plt.yticks(range(0, max(self.cwnd_history) + 5, 5))
        
        # Save the plot as specified [cite: 55]
        plt.savefig('cwnd_plot.png')
        print("Plot saved as cwnd_plot.png")
        plt.show()

if __name__ == "__main__":
    simulation = TCPCongestionControl(ssthresh_initial=32, max_rounds=40, timeout_round=22)
    simulation.simulate()