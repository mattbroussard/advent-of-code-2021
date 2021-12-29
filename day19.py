# 12/20/2021
# https://adventofcode.com/2021/day/19

import sys
from collections import defaultdict
import math
import numpy as np
from functools import cache
from itertools import product

PI = math.pi

# https://stackoverflow.com/a/6802723
@cache
def rotation_matrix(axis, theta):
  """
  Return the rotation matrix associated with counterclockwise rotation about
  the given axis by theta radians.
  """
  axis = np.asarray(axis)
  axis = axis / math.sqrt(np.dot(axis, axis))
  a = math.cos(theta / 2.0)
  b, c, d = -axis * math.sin(theta / 2.0)
  aa, bb, cc, dd = a * a, b * b, c * c, d * d
  bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
  rot =   np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                   [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                   [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

  # these 90deg rotation matrices should only contain the values -1, 0, 1 -- essentially just reordering
  # the elements of a vector. Avoid any floating point weirdness by rounding off here.
  rot = rot.round()
  return rot

def rotate(vec, rotation_type):
  # rotation_type is an int [0, 24) describing one of the 24 possible orientations
  # 0 is same orientation
  # for simplicity we assume we are facing positive z (into screen), with pos x right and pos y up
  # 0:  pos-z, 0deg
  # 1:  pos-z, 90deg
  # 2:  pos-z, 180deg
  # 3:  pos-z, 270deg
  # 4:  neg-z, 0deg
  # 5:  neg-z, 90deg
  # 6:  neg-z, 180deg
  # 7:  neg-z, 270deg
  # 8:  pos-x, 0deg
  # 9:  pos-x, 90deg
  # 10: pos-x, 180deg
  # 11: pos-x, 270deg
  # 12: neg-x, 0deg
  # 13: neg-x, 90deg
  # 14: neg-x, 180deg
  # 15: neg-x, 270deg
  # 16: pos-y, 0deg
  # 17: pos-y, 90deg
  # 18: pos-y, 180deg
  # 19: pos-y, 270deg
  # 20: neg-y, 0deg
  # 21: neg-y, 90deg
  # 22: neg-y, 180deg
  # 23: neg-y, 270deg

  axis_rot = np.identity(3)
  if rotation_type > 7 and rotation_type < 16:
    axis_rot = rotation_matrix((0, 1, 0), PI / 2.0)
  elif rotation_type >= 16:
    axis_rot = rotation_matrix((1, 0, 0), PI / 2.0)

  axis_flip = np.identity(3)
  if rotation_type in (4,5,6,7,12,13,14,15,20,21,22,23):
    axis_flip = rotation_matrix((0, 1, 0), PI)

  view_rot = rotation_matrix((0, 0, 1), PI / 2.0 * (rotation_type % 4))

  # @ operator is apparently numpy for matrix multiply?
  combined_rotation = ((axis_rot @ axis_flip) @ view_rot)
  return tuple(combined_rotation @ vec)

def rotate_and_translate(vec, rotation_type, translation):
  return tuple(a + b for a, b in zip(rotate(vec, rotation_type), translation))

def rotation_types():
  return range(24)

def apply_multiple_transforms(vec, transforms):
  for rot, translate, *_ in transforms:
    vec = rotate_and_translate(vec, rot, translate)
  return vec

def test_orientations():
  """
  This is a test case for rotate() -- the idea is if we take a constellation of
  one point in each of the 8 quadrants of 3D space and rotate it each of the 24
  ways, we should end up with 24 unique orderings of points. All the coordinate
  values should be the same as we put in, just with different signs and orderings
  """
  x = (-1, 1)
  test_points = sorted(list(product(x, x, x)))

  rot_set = set()

  for t in range(24):
    rotated = tuple(rotate(vec, t) for vec in test_points)
    if len(set(rotated)) != len(rotated):
      print("ERROR: for orient %d, duplicate constellation points after rotate" % (t,))
    rot_set.add(rotated)
    print("orient %2d: %s" % (t, rotated[-1]))

  print("%d distinct orientations" % (len(rot_set),))

  values_set = set()
  for rot in rot_set:
    for pt in rot:
      for v in pt:
        values_set.add(v)
  print("distinct coordinate values: %s" % (values_set,))

def vec_sub(a, b):
  return tuple(v1 - v2 for v1, v2 in zip(a, b))

def vec_len(v):
  return math.sqrt(sum(x ** 2 for x in v))

class Scanner:
  scanner_id = None
  points = None # (scanner-local) point id -> coord
  num_points = 0
  edge_vecs = None
  edge_vec_set = None

  def __init__(self, id):
    self.scanner_id = id
    self.points = {}
    # vec -> list((ptA, ptB))
    self.edge_vecs = defaultdict(lambda: [])
    # set(edge_vecs.keys())
    self.edge_vec_set = set()

  def add_point(self, pt):
    point_id = "%s_%s" % (self.scanner_id, self.num_points)
    self.num_points += 1
    self.points[point_id] = pt

    for other_point_id, other_point in self.points.items():
      if other_point_id == point_id:
        continue

      # previously, we stored vec_len(vec), not vec as key
      vec = vec_sub(pt, other_point)
      self.edge_vec_set.add(vec)
      self.edge_vecs[vec].append((other_point, pt))

      vec = vec_sub(other_point, pt)
      self.edge_vec_set.add(vec)
      self.edge_vecs[vec].append((pt, other_point))

  def print_rep(self):
    print("scanner %s: %d points, %d unique edge vecs" % (self.scanner_id, self.num_points, len(self.edge_vec_set)))
    for pid, pt in self.points.items():
      print(' - %s: %s' % (pid, pt))

  def compare_to_other_scanner(self, other):
    """
    returns tuple of:
     - integer "rotation type"
     - translation vector
     - number of common points
    ... that convert this scanner's coordinate space into "other's"
    returns (None, None, 0) if there is no mapping
    """
    for rot_type in rotation_types():
      """
      rotated_edge_vecs = {
        rotate(vec, rot_type): [(rotate(a, rot_type), rotate(b, rot_type)) for a, b in v]
        for vec, v in self.edge_vecs.items()
      }
      rotated_edge_vec_set = set(rotated_edge_vecs.keys())
      intersection = rotated_edge_vec_set.intersection(other.edge_vec_set)
      if len(intersection) == 0:
        continue

      # all (rotated) self points involved in any of the vectors in the intersection
      # if there is a true overlap between self and other, some subset of >=12
      # of these points should be just a translation away from some subset of
      # points in other.
      our_rotated_pts = set(
        pt
        for vec in intersection
        for pair in rotated_edge_vecs[vec]
        for pt in pair
      )
      if len(our_rotated_pts) < 12:
        continue
      """

      # test: instead of caring about vector set intersection, let's just
      # rotate + translate all points every time
      our_rotated_pts = [rotate(pt, rot_type) for pt in self.points.values()]

      # now, we compare each possible pair of points and come up with a translation vector. We'll
      # build a histogram/frequency map of those and choose the most frequent.
      # There are 25ish points per scanner so we expect about ~625 iterations of this inner loop.
      #
      # Idea: if there is truly an overlap and this rot_type is correct, at least 12 pairs of
      # points will share the same translation vector between them
      translation_histogram = defaultdict(int)
      for our_point, their_pt in product(our_rotated_pts, other.points.values()):
        translation = vec_sub(their_pt, our_point)
        translation_histogram[translation] += 1
      most_frequent_translation = max(translation_histogram.keys(), key=lambda k: translation_histogram[k])
      num_common_points = translation_histogram[most_frequent_translation]
      if num_common_points < 12:
        if num_common_points > 1:
          # print("scanner %s -> %s, rot=%d: %d common points" % (self.scanner_id, other.scanner_id, rot_type, num_common_points))
          pass
        continue

      return rot_type, most_frequent_translation, num_common_points

    return None, None, 0

def read_file():
  fname = sys.argv[1]

  scanner_id = 0
  scanners = []
  cur_scanner = None

  with open(fname, 'r') as f:
    for line in f:
      if '--- scanner' in line:
        cur_scanner = Scanner(scanner_id)
        scanner_id += 1
        scanners.append(cur_scanner)
        continue

      if ',' in line:
        pt = tuple(int(n) for n in line.split(','))
        cur_scanner.add_point(pt)
        continue

  return scanners

def test_single_intersection():
  scanners = read_file()

  j = 4
  for i, scanner in enumerate(scanners):
    if i == j:
      continue

    rot, trans, num_common = scanner.compare_to_other_scanner(scanners[j])
    if rot is not None:
      print("Found intersection b/w %d and %d: rot=%d, trans=%s, numCommon=%d" % (j, i, rot, trans, num_common))
      break
  else:
    print("No intersection found with scanner 0")

def part1_compute_edges(scanners):
  known = set([0])
  unknown = set(range(1,len(scanners)))

  # (a, b) -> (rot, trans, num_common)
  links = {}

  while len(unknown) > 0:
    found_any = False
    for scan1_id in list(unknown):
      for scan2_id in list(known):
        s1 = scanners[scan1_id]
        s2 = scanners[scan2_id]
        rot, trans, num_common = s1.compare_to_other_scanner(s2)
        if rot is not None:
          unknown.remove(scan1_id)
          known.add(scan1_id)
          links[(scan1_id, scan2_id)] = (rot, trans, num_common)
          print("Found intersection b/w %d and %d: rot=%d, trans=%s, numCommon=%d; %d to go" % (scan1_id, scan2_id, rot, trans, num_common, len(unknown)))
          found_any = True
          break

    if not found_any:
      print("Error: no unknown scanner (%s) intersected any known scanner (%s)" % (list(unknown), list(known)))
      break

  return links

def part1():
  scanners = read_file()
  links = part1_compute_edges(scanners)

  # We hit an error in part1_compute_edges that caused it to not find intersections between all scanners
  if len(links) != len(scanners) - 1:
    return

  def path_from_links(i):
    if i == 0:
      return []
    for edge, transform in links.items():
      a, b = edge
      if a == i:
        return [transform] + path_from_links(b)

  pts = set()
  for i, scanner in enumerate(scanners):
    transform_path = path_from_links(i)
    for pt in scanner.points.values():
      pts.add(apply_multiple_transforms(pt, transform_path))

  print("Total number of points: %d" % (len(pts),))

def main():
  # test_orientations()
  # test_single_intersection()
  part1()

if __name__ == '__main__':
  main()