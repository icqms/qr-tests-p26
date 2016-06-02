from __future__ import division
import os, random
from libtbx import easy_run

"""
Perturb models from 01b_fixSplit/*.pdb.
"""

def run():
  path = "../01d_fixSplit_GFA/"
  for i_f, f in enumerate(os.listdir(path)):
    if(f.endswith(".pdb")):
      prefix = f[:-4]
      os.mkdir(prefix)
      os.chdir(prefix)
      for p_size in [0.3, 0.6, 0.9, 1.2, 1.5]:
        p_size = str(p_size)
        os.mkdir(p_size)
        os.chdir(p_size)
        file_name = "../../"+path+f
        print i_f, file_name
        for trial in xrange(10):
          rs = random.randrange(1111111, 9999999)
          cmd = " ".join([
            "phenix.dynamics",
            "%s"%file_name,
            "stop_at_diff=%s"%p_size,
            "number_of_steps=20000",
            "temperature=1000",
            "write_geo_file=False",
            "random_seed=%s"%str(rs),
	   "use_neutron_distances=true",	
            "output_file_name_prefix=%s"%str(trial),
            "> %s.log"%prefix])
          easy_run.call(cmd)
          easy_run.call("rm -rf *.log")
        os.chdir("..")
      os.chdir("..")

if __name__ == "__main__":
  run()
