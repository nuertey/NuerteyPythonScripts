import timeit

def convert_to_bytes(bit_list):
    """Converts a list of 0s and 1s to a list of bytes."""
    
    byte_list = []
    for i in range(0, len(bit_list), 8):
        byte = int(''.join(map(str, bit_list[i:i+8])), 2)
        byte_list.append(byte)
    return byte_list

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
        output = [0] * length
        for i in range(length):
            output[i] = self.step()

        byte_list = convert_to_bytes(output)
        
        hex_byte_list = [f"{num:#0{4}x}" for num in byte_list]            
            
        return hex_byte_list

# Key Points:
# 
#     The tap positions determine the feedback polynomial, which affects the properties of the generated sequence.
#     To achieve maximal period, the feedback polynomial should be primitive.
#     You can use the pylfsr library for more advanced LFSR implementations and analysis.

# TAP COUNTING IS FROM LEFT TO RIGHT!!

# TAP DESIGNATION # IS THE EXACT SHOWN WITHIN EACH SINGLE BIT DELAY ON THE LOGIC DIAGRAM!!!

# THE RIGHTMOST BIT OF THE LFSR IS CALLED THE OUTPUT BIT, WHICH IS ALWAYS ALSO A TAP!!!

# The initial value of the LFSR is called the seed, and because the operation of the register is deterministic, 
# the stream of values produced by the register is completely determined by its current (or previous) state. 
# Likewise, because the register has a finite number of possible states, it must eventually enter a repeating cycle.

# The bit positions that affect the next state are called the taps. 
# The rightmost bit of the LFSR is called the output bit, which is always also a tap. 
# To obtain the next state, the tap bits are XOR-ed sequentially; then, all bits are shifted one place to the right, 
# with the rightmost bit being discarded, and that result of XOR-ing the tap bits is fed back into the now-vacant 
# leftmost bit. To obtain the pseudorandom output stream, read the rightmost bit after each state transition.

def wrapper():
    length_of_sequence_desired = 255*8
    lfsr = LFSR([1, 1, 1, 1, 1, 1, 1, 1], [7, 5, 3, 0])
    return lfsr.generate(length_of_sequence_desired)
    
if __name__ == "__main__":
    # Example usage

    # 10.4 SEQUENCE SPECIFICATION
    # 
    # 10.4.1 The pseudo-random sequence shall be generated using the following polynomial:
    # h(x) = x8 + x7 + x5 + x3 + 1
    
    # Perfect results!
    #lfsr = LFSR([1, 1, 1, 1, 1, 1, 1, 1], [7, 5, 3, 0])  # Seed: 0xFF, Taps: 7, 5, 3, 0 (From corrected CCSDS 131.0-B-5!! Do NOT use CCSDS 131.0-B-3!!!)
    #sequence = lfsr.generate(260*8)
    #print(sequence)

    time_taken = timeit.timeit('wrapper', 'from __main__ import wrapper')
    
    print(f'time_taken = {time_taken}')
    print()

