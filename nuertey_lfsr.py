# Explanation:
# 
#     __init__(self, seed, taps):
#         Initializes the LFSR object with the initial seed (a list of bits) and the tap positions (a list of indices). 
#     step(self):
#         Calculates the output bit as the leftmost bit of the current state.
#         Calculates the feedback bit by XORing the bits at the specified tap positions.
#         Shifts the register to the left and inserts the feedback bit at the rightmost position.
#         Returns the output bit. 
#     generate(self, length):
#         Calls the step() method repeatedly to generate a sequence of bits of the specified length.

class LFSR:
    def __init__(self, seed, taps):
        self.state = seed
        self.taps = taps

    def step(self):
        """Perform one LFSR step and return the output bit."""
        output_bit = self.state[0]
        feedback_bit = 0
        for tap in self.taps:
            feedback_bit ^= self.state[tap]
        self.state = self.state[1:] + [feedback_bit]
        return output_bit

    def generate(self, length):
        """Generate a sequence of bits of the specified length."""
        output = []
        for _ in range(length):
            output.append(self.step())
        return output

if __name__ == "__main__":
    # Example usage
    lfsr = LFSR([1, 0, 1, 0], [3, 2])  # Seed: 1010, Taps: 3, 2
    sequence = lfsr.generate(10)
    print(sequence)
