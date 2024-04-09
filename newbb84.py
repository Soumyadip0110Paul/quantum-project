from qiskit import *
from qiskit_aer import *
import numpy as np
import csv

# Function to create a random string of bits
def random_bit_string(length):
    return ''.join(np.random.choice(['0', '1'], size=length))

# Function to encode the qubits by Alice
def alice_encode(qc, bits, bases):
    for i in range(len(bits)):
        if bases[i] == 0:  # Prepare qubit in Z-basis
            if bits[i] == '1':
                qc.x(i)
        elif bases[i] == 1:  # Prepare qubit in X-basis
            if bits[i] == '0':
                qc.h(i)
            else:
                qc.x(i)
                qc.h(i)

# Function to measure qubits by Bob
def bob_measure(qc, bases):
    for i in range(len(bases)):
        if bases[i] == 0:  # Measure qubit in Z-basis
            qc.measure(i, i)
        elif bases[i] == 1:  # Measure qubit in X-basis
            qc.h(i)
            qc.measure(i, i)
            qc.h(i)

# Function to simulate Eve's attack
def eve_attack(qc):
    for i in range(n):
        qc.measure(i, i)

# Function to compare bases between Alice and Bob
def compare_bases(bases_a, bases_b):
    return [bases_a[i] == bases_b[i] for i in range(len(bases_a))]

# Function to extract the key bits agreed upon by Alice and Bob
def extract_key(bits, bases, agreed_bases):
    return ''.join([bits[i] for i in range(len(bits)) if agreed_bases[i]])

# Function to write Alice, Bob, and Eve's messages to a CSV file
def write_to_csv(alice_message, bob_message, eve_message):
    with open('bb84_messages.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Alice Message', 'Bob Message', 'Eve Message'])
        for a, b, e in zip(alice_message, bob_message, eve_message):
            writer.writerow([a, b, e])

# Parameters
n = 20  # Number of qubits
alice_bases = [np.random.randint(2) for _ in range(n)]  # Random bases for Alice
bob_bases = [np.random.randint(2) for _ in range(n)]  # Random bases for Bob

# Random bits for Alice
alice_bits = random_bit_string(n)
alice_message = [chr(int(alice_bits[i:i+8], 2)) for i in range(0, len(alice_bits), 8)]

# Quantum circuit setup
qc = QuantumCircuit(n, n)

# Alice encodes her bits
alice_encode(qc, alice_bits, alice_bases)

# Eve intercepts and measures the qubits
eve_attack(qc)

# Bob measures the qubits
bob_measure(qc, bob_bases)

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1, memory=True)  # Specify memory=True to get individual measurement outcomes
result = job.result()
counts = result.get_counts()

# Extract Bob's bits from measurement outcomes
bob_bits_measured = list(counts.keys())[0]  # Bob's bits as a binary string

# Convert Bob's bits to bytes
bob_message = [bob_bits_measured[i:i+8] for i in range(0, len(bob_bits_measured), 8)]

# Convert Alice's bits to bytes
alice_bits_binary = ''.join([alice_bits[i] for i in range(len(alice_bits)) if alice_bases[i] == 0])

# Compare bases and extract the final key
agreed_bases = compare_bases(alice_bases, bob_bases)
final_key = extract_key(alice_bits_binary, alice_bases, agreed_bases)

# Write Alice, Bob, and Eve's messages to a CSV file
write_to_csv(alice_message, bob_message, alice_message)

# Print the results
print("Alice's message:", ''.join(alice_message))
print("Bob's message:", ''.join([chr(int(byte, 2)) for byte in bob_message]))
print("Final Key:", final_key)
