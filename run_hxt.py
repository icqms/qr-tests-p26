from __future__ import division
import iotbx.pdb
import os
from cctbx import uctbx

"""
Fix duplicate H: rename duplicate H->HXT.
"""

def run():
  path = "../01_reordered_box/"
  for f in os.listdir(path):
    if(f.endswith(".pdb")):
      prefix = f[:-4]
      print f
      pdb_inp = iotbx.pdb.input(file_name = path+f)
      h = pdb_inp.construct_hierarchy()
      rgs = list(h.residue_groups())
      size = len(rgs)
      for i, rg in enumerate(rgs):
        if(i==size-1):
          for a1 in rg.atoms():
            if(a1.name.strip()=="O"):
              for a2 in rg.atoms():
                if(a2.name.strip()=="H"):
                  if(a1.distance(a2)<1.2):
                    a2.name=" HXT"
      h.write_pdb_file(file_name=f,
        crystal_symmetry=pdb_inp.crystal_symmetry())

if __name__ == "__main__":
  run()
