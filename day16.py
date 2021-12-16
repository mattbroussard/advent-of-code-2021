# 12/15/2021
# https://adventofcode.com/2021/day/16

import sys

def read_file():
  fname = sys.argv[1]
  with open(fname, 'r') as f:
    hex_string = f.read().strip()

  bin_string = bin(int(hex_string, 16))[2:]
  bits = [int(c) for c in bin_string]
  return bits

def bits_to_int(bits):
  return int("".join(str(bit) for bit in bits), 2)

class Packet:
  version = None
  type_id = None
  literal = None
  children = None
  length_type_id = None
  raw = None

  def __str__(self):
    if self.type_id == 4:
      payload = "literal %d" % (self.literal,)
    else:
      parts = [str(c) for c in self.children]
      payload = "ltid:%d len:%d [%s]" % (self.length_type_id, len(self.children), ", ".join(parts))
    return "(v:%d t:%d %s)" % (self.version, self.type_id, payload)

def parse_literal(bits, start=0):
  cursor = start
  value_bits = []

  while True:
    have_more = bits[cursor]
    value_bits += bits[cursor+1:cursor+5]
    cursor += 5
    if not have_more:
      break

  return bits_to_int(value_bits), cursor

def parse_packet(bits, start=0):
  cursor = start

  packet = Packet()
  packet.version = bits_to_int(bits[cursor:cursor+3])
  cursor += 3
  packet.type_id = bits_to_int(bits[cursor:cursor+3])
  cursor += 3

  if packet.type_id == 4:
    packet.literal, cursor = parse_literal(bits, cursor)
  else:
    packet.children = []
    packet.length_type_id = bits[cursor]
    cursor += 1

    if packet.length_type_id == 0:
      children_bit_length = bits_to_int(bits[cursor:cursor+15])
      cursor += 15

      end_of_children = cursor + children_bit_length
      while cursor < end_of_children:
        child, cursor = parse_packet(bits, cursor)
        packet.children.append(child)
    else:
      num_children = bits_to_int(bits[cursor:cursor+11])
      cursor += 11

      for _ in range(num_children):
        child, cursor = parse_packet(bits, cursor)
        packet.children.append(child)

  packet.raw = bits[start:cursor]
  return packet, cursor

def sum_versions(packet):
  children = packet.children or []
  child_versions = sum(sum_versions(child) for child in children)
  return packet.version + child_versions

def part1():
  data = read_file()
  packet, _ = parse_packet(data)

  print(sum_versions(packet))
  # print(packet)

def compute_packet_value(packet):
  if packet.type_id == 4: # literal
    return packet.literal
  elif packet.type_id == 0: # sum
    return sum(compute_packet_value(child) for child in packet.children)
  elif packet.type_id == 1: # product
    product = 1
    for child in packet.children:
      product *= compute_packet_value(child)
    return product
  elif packet.type_id == 2: # min
    return min(compute_packet_value(child) for child in packet.children)
  elif packet.type_id == 3: # max
    return max(compute_packet_value(child) for child in packet.children)
  elif packet.type_id == 5: # gt
    a, b = (compute_packet_value(child) for child in packet.children)
    return 1 if a > b else 0
  elif packet.type_id == 6: # lt
    a, b = (compute_packet_value(child) for child in packet.children)
    return 1 if a < b else 0
  elif packet.type_id == 7: # eq
    a, b = (compute_packet_value(child) for child in packet.children)
    return 1 if a == b else 0
  else:
    raise Error('unknown packet type')

def part2():
  data = read_file()
  packet, _ = parse_packet(data)
  print(compute_packet_value(packet))

def main():
  part1()
  part2()

if __name__ == '__main__':
  main()
