from __future__ import division
import iotbx.pdb
import os
from cctbx import uctbx

"""
Find split residues.
"""

def run():
  path = "01b_fixSplit/"
  for f in os.listdir(path):
    if(f.endswith(".pdb")):
      prefix = f[:-4]
      pdb_inp = iotbx.pdb.input(file_name = path+f)
      h = pdb_inp.construct_hierarchy()
      resids = []
      for rg in h.residue_groups():
        resids.append(int(rg.resseq))
      first = resids[0]
      last  = resids[len(resids)-1]
      if(last <= first):
        print f, first, last

if __name__ == "__main__":
  run()
