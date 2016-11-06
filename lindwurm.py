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

class Lindwurm:
    def __init__(self):
        # Todo descriptions
        self.lw_parser = argparse.ArgumentParser(description='Lindwurm')
        self.lw_subparsers = \
                self.lw_parser.add_subparsers(description='subcommands:', dest='curr_subcmd')

        self.cohesion_parser = self.lw_subparsers.add_parser('cohesion', description='cohesion')
        self.cohesion_parser.add_argument('objectives', metavar='obj', nargs='+', choices=['link', 'net', 'transport']) 
        self.cohesion_parser.add_argument('--t_serv')
        self.cohesion_parser.add_argument('--t_ports')

    def parse_args(self):
        self.args = self.lw_parser.parse_args()

    def run(self):
        pass

if __name__ == "__main__":
    lindwurm = Lindwurm()

    lindwurm.parse_args()

    lindwurm.run()
