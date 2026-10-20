import random
import matplotlib.pyplot as plt


def generate_random_data(length):
    data = " "

    for i in range(length):
        bit = random.randint(0, 1)
        data += str(bit)
    return data



def generate_data_with_zeros(length, zero_count):
    if zero_count not in (4, 8):
        raise ValueError("zero_count must be either 4 or 8")

    if length < zero_count:
        raise ValueError("Length must be at least zero_count")

    data = generate_random_data(length - zero_count)

    position = random.randint(0, len(data))

    data = data[:position] + ("0" * zero_count) + data[position:]

    return data

def expand_around_center(data, left, right):
    while (
    left >= 0
    and right < len(data)
    and data[left] == data[right]
    ):
        left -= 1
        right += 1

        return data[left + 1:right]

def longest_palindrome(data):
    if not data:
     return ""

    longest = ""

    for i in range(len(data)):
        
        odd = expand_around_center(data, i, i)

        
        even = expand_around_center(data, i, i + 1)

        if len(odd) > len(longest):
            longest = odd

        if len(even) > len(longest):
            longest = even

    return longest



def encode_nrz_l(data):
    signal = []
    for bit in data:
        if bit == '1':
            signal.append(+1)
        else:
            signal.append(-1)

    return signal




def plot_signal(data, signal, title="Digital Signal", samples_per_bit=1):
    time = [
        i / samples_per_bit
        for i in range(len(signal) + 1)
    ]

    levels = signal + [signal[-1]]

    plt.figure(figsize=(12, 4))

    plt.step(time, levels, where="post")

    plt.xticks(range(len(data) + 1))
    plt.yticks([-1, 0, 1])

    plt.ylim(-1.5, 1.5)
    plt.xlim(0, len(data))

    plt.xlabel("Time (bit intervals)")
    plt.ylabel("Voltage level")
    plt.title(title)

    plt.grid(True)
    plt.show()

def encode_nrz_i(data):
    signal = []
    current_level = -1

    for bit in data:
        if bit == '1':
            current_level *= -1

        signal.append(current_level)

    return signal


def encode_manchester(data):
    signal = []

    for bit in data:
        if bit == '1':
            signal.extend([-1, 1])
        else:
            signal.extend([1, -1])

    return signal


def encode_differential_manchester(data):
    signal = []
    current_level = 1

    for bit in data:
        if bit == '0':
            current_level *= -1

        signal.append(current_level)

        current_level *= -1

        signal.append(current_level)

    return signal

# n = int(input("Enter total number of bits: "))
# zero_count = int(input("Enter consecutive zeros required (4 or 8):" ))

# data = generate_data_with_zeros(n, zero_count)

# print("Generated data:", data)
# print("Length:", len(data))
# print("Contains required zeros:", "0" * zero_count in data)


# data = input("Enter a binary sequence: ")

# signal = encode_nrz_l(data)

# print("Digital data:", data)
# print("Encoded signal:", signal)
# plot_signal(data, signal)



# data = input("Enter a binary sequence: ")

# signal = encode_nrz_i(data)

# print("Digital data:", data)
# print("NRZ-I signal:", signal)

# plot_signal(data, signal, title="NRZ-I Encoding")


# data = input("Enter a binary sequence: ")

# signal = encode_manchester(data)

# print("Digital data:", data)
# print("Manchester signal:", signal)

# plot_signal(
#     data,
#     signal,
#     title="Manchester Encoding",
#     samples_per_bit=2
# )


def encode_ami(data):
    signal = []
    last_pulse = -1

    for bit in data:
        if bit == '1':
            last_pulse *= -1
            signal.append(last_pulse)
        else:
            signal.append(0)

    return signal





# data = input("Enter a binary sequence: ")

# signal = encode_differential_manchester(data)

# print("Digital data:", data)
# print("Differential Manchester signal:", signal)

# plot_signal(
#     data,
#     signal,
#     title="Differential Manchester Encoding",
#     samples_per_bit=2
# )


def encode_b8zs(data):
    signal = []
    last_pulse = -1
    i = 0

    while i < len(data):
        if data[i:i + 8] == "00000000":
            if last_pulse == 1:
                pattern = [0, 0, 0, 1, -1, 0, -1, 1]
            else:
                pattern = [0, 0, 0, -1, 1, 0, 1, -1]

            signal.extend(pattern)
            last_pulse = pattern[-1]
            i += 8

        else:
            if data[i] == '1':
                last_pulse *= -1
                signal.append(last_pulse)
            else:
                signal.append(0)

            i += 1

    return signal


# data = input("Enter a binary sequence: ")

# signal = encode_ami(data)

# print("Digital data:", data)
# print("AMI signal:", signal)

# plot_signal(
#     data,
#     signal,
#     title="AMI Encoding"
# )




def encode_hdb3(data):
    signal = []
    last_pulse = -1
    pulse_count = 0
    i = 0

    while i < len(data):

        if data[i:i + 4] == "0000":

            if pulse_count % 2 == 0:
                # Even number of nonzero pulses: B00V
                b_pulse = -last_pulse
                v_pulse = b_pulse

                pattern = [b_pulse, 0, 0, v_pulse]

            else:
                # Odd number of nonzero pulses: 000V
                v_pulse = last_pulse

                pattern = [0, 0, 0, v_pulse]

            signal.extend(pattern)
            last_pulse = pattern[-1]

            # Reset pulse count after substitution
            pulse_count = 0
            i += 4

        else:
            if data[i] == '1':
                last_pulse *= -1
                signal.append(last_pulse)
                pulse_count += 1
            else:
                signal.append(0)

            i += 1

    return signal


# data = input("Enter a binary sequence: ")

# signal = encode_b8zs(data)

# print("Digital data:", data)
# print("B8ZS signal:", signal)

# plot_signal(
#     data,
#     signal,
#     title="B8ZS Encoding"
# )


# data = input("Enter a binary sequence: ")

# signal = encode_hdb3(data)

# print("Digital data:", data)
# print("HDB3 signal:", signal)

# plot_signal(
#     data,
#     signal,
#     title="HDB3 Encoding"
# )




def pcm_encode(samples, bits=3):
    levels = 2 ** bits

    min_value = -1.5
    max_value = 2.0

    step_size = (max_value - min_value) / levels

    binary_data = ""
    quantized_values = []

    for sample in samples:
        # Find the quantization index
        index = int((sample - min_value) / step_size)

        # Clamp the index to a valid range
        index = max(0, min(index, levels - 1))

        quantized_value = min_value + (index + 0.5) * step_size

        quantized_values.append(quantized_value)

        # Convert the quantization index into binary
        binary_data += format(index, f"0{bits}b")

    return binary_data, quantized_values


def pcm_decode(binary_data, bits=3):
    levels = 2 ** bits

    min_value = -1.5
    max_value = 2.0

    step_size = (max_value - min_value) / levels

    decoded_values = []

    for i in range(0, len(binary_data), bits):
        chunk = binary_data[i:i + bits]

        if len(chunk) != bits:
            raise ValueError("Invalid PCM bitstream length")

        index = int(chunk, 2)

        if index >= levels:
            raise ValueError("Invalid PCM code")

        value = min_value + (index + 0.5) * step_size

        decoded_values.append(value)

    return decoded_values


def plot_pcm(original_samples, decoded_samples):
    import matplotlib.pyplot as plt

    original_time = list(range(len(original_samples)))
    decoded_time = list(range(len(decoded_samples)))

    plt.figure(figsize=(10, 5))

    plt.plot(
        original_time,
        original_samples,
        marker="o",
        label="Original signal"
    )

    plt.step(
        decoded_time,
        decoded_samples,
        where="mid",
        label="Reconstructed PCM signal"
    )

    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.title("PCM Encoding and Decoding")
    plt.legend()
    plt.grid(True)
    plt.show()


samples = [0.2, 0.8, 1.4, 0.7, -0.5, -1.2]

binary_data, quantized_values = pcm_encode(samples)

signal = encode_nrz_l(binary_data)

print("PCM bitstream:", binary_data)
print("NRZ-L signal:", signal)

plot_signal(
    binary_data,
    signal,
    title="PCM Output Encoded Using NRZ-L"
)