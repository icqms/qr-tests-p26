from __future__ import division
import iotbx.pdb
import os
from cctbx import uctbx
from libtbx import easy_run

"""
Compute MTZ with Fobs from 01b_fixSplit/*.pdb.
"""

def run():
  path = "../01d_fixSplit_GFA/"
  for f in os.listdir(path):
    if(f.endswith(".pdb")):
      prefix = f[:-4]
      xrs = iotbx.pdb.input(file_name=path+f).xray_structure_simple()
      f_calc = \
        xrs.structure_factors(d_min=2.5).f_calc().resolution_filter(d_max=4.0)
      f_obs = abs(f_calc)
      mtz_dataset = f_calc.as_mtz_dataset(column_root_label="F-calc")
      mtz_dataset.add_miller_array(
        miller_array      = f_obs,
        column_root_label = "F-obs")
      mtz_dataset.add_miller_array(
        miller_array      = f_obs.generate_r_free_flags(fraction=0.05),
        column_root_label = "R-free-flags")
      mtz_object = mtz_dataset.mtz_object()
      mtz_object.write(file_name = prefix+".mtz")
      cmd = "phenix.pdb_interpretation  write_geo_file=true  "+path+f
      easy_run.call(cmd) 

if __name__ == "__main__":
  run()
