# lindwurm
#Copyright (C) 2016  Matthias Tafelmeier

#lindwurm is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#lindwurm is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

from parser.aggregator import Aggregator
import ConfigParser
import os

class Illustrator:
    """ Hub module for depicting revealer aggregated intelligence 
        in various facettes. 
    """
    def __init__(self, settings):
        #Todo partition settings
        self.aggregator = Aggregator(settings) 
    def run(self):
        self.aggregator.run() 

mod_parent_path = os.path.abspath(__file__ + "/../")
conf_dir_path = os.path.dirname(mod_parent_path)
conf_file = "lindwurm.cfg" 

cnfg_loc = [ conf_dir_path + '/' + conf_file ]
config = ConfigParser.SafeConfigParser()
cfg_parsed = config.read(cnfg_loc)

if not cfg_parsed:
    raise RuntimeError("no config file")

illustrator = Illustrator(config)
illustrator.run()

