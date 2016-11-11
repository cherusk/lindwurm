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

import argparse
import ConfigParser
import os
from illustrator.illustrator_core import Illustrator

class Lindwurm:
    def __init__(self):

        self.load_cnfg()

        # Todo descriptions
        self.lw_parser = argparse.ArgumentParser(description='Lindwurm')
        self.lw_subparsers = \
                self.lw_parser.add_subparsers(description='subcommands:', dest='curr_subcmd')

        self.cohesion_parser = self.lw_subparsers.add_parser('cohesion', description='cohesion')
        self.cohesion_parser.add_argument('objectives', metavar='obj', nargs='+', choices=['link', 'net', 'transport']) 

        #Todo: sane defs.
        self.cohesion_parser.add_argument('--n_prots')
        self.cohesion_parser.add_argument('--t_serv')
        self.cohesion_parser.add_argument('--t_ports')

        self.illustrator = Illustrator(self.config)

    def parse_args(self):
        self.args = self.lw_parser.parse_args()

    def load_cnfg(self):
        mod_path = os.path.abspath(__file__) 
        conf_dir_path = os.path.dirname(mod_path)
        conf_file = "lindwurm.cfg" 
        cnfg_loc = [ conf_dir_path + '/' + conf_file ]

        self.config = ConfigParser.SafeConfigParser()
        parsed_cnfg_f = self.config.read(cnfg_loc)

        if not parsed_cnfg_f:
            raise RuntimeError("no config file")

    def run(self):
        construer = self.illustrator.conjure(self.args.curr_subcmd)

        construer.do_term(self.args)

if __name__ == "__main__":
    lindwurm = Lindwurm()

    lindwurm.parse_args()

    lindwurm.run()
