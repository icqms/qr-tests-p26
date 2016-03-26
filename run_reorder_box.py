from __future__ import division
import iotbx.pdb
import os
from cctbx import uctbx

"""
Re-order PDB files that were obtained from XYZ files, then place in P1 box.
"""

def reorder(path, prefix):
  pdb_inp = iotbx.pdb.input(file_name="%s%s.pdb"%(path,prefix))
  h = pdb_inp.construct_hierarchy()
  rg = list(h.residue_groups())
  rg.reverse()
  #
  c = iotbx.pdb.hierarchy.chain(id="A")
  for rg_ in rg:
    c.append_residue_group(rg_.detached_copy())
  #
  r = iotbx.pdb.hierarchy.root()
  m = iotbx.pdb.hierarchy.model()
  r.append_model(m)
  m.append_chain(c)  
  atoms = r.atoms()
  #
  box = uctbx.non_crystallographic_unit_cell_with_the_sites_in_its_center(
    sites_cart=atoms.extract_xyz(),
    buffer_layer=3.)
  atoms.set_xyz(new_xyz=box.sites_cart)
  #
  fo = open("%s-new.pdb"%prefix,"w")
  print >> fo, iotbx.pdb.format_cryst1_record(
    crystal_symmetry=box.crystal_symmetry())
  for a in atoms:
    a = a.set_b(30.)
    print >> fo, a.format_atom_record()
  fo.close()
  
def run():
  path = "../00_original_pdb/"
  for f in os.listdir(path):
    if(f.endswith(".pdb")):
      prefix = f[:-4]
      reorder(path = path, prefix = prefix) 
 

if __name__ == "__main__":
  run()
  
