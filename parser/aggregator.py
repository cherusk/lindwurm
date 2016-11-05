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

from parser import *
import os

class Aggregator:
    def __init__(self, conf):
        self.parsers = { "nmap": NmapParser(), "mtr": MtrParser(), "owp" : OwpingParser() } 
        self.conf = conf
        self.conf_section = 'aggregator' 
    #TODO REFACTOR
    def run(self):
        """
        aggregate revealer provided raw intelligence from remote sites
        """

        is_first = True
        nmap_out_dir = self.conf.get(self.conf_section, 'nmap_out')
        aggl_run_json = '{ "run" : { "nmap": [ ' 
        for root, dirs, files in os.walk(nmap_out_dir):
            if root != nmap_out_dir:
                for f in files:
                    if is_first:
                        fmt = "%s %s"
                    else: 
                        fmt = "%s, %s"
                    aggl_run_json = fmt  % \
                            (aggl_run_json, self.parsers['nmap'].parse(root + '/' + f))
                    is_first = False

        is_first = True
        mtr_out_dir = self.conf.get(self.conf_section, 'mtr_out')
        aggl_run_json =  '%s ], "mtr": [ ' % (aggl_run_json)
        for root, dirs, files in os.walk(mtr_out_dir):
            if root != mtr_out_dir:
                for f in files: 
                    if is_first:
                        fmt = "%s %s"
                    else: 
                        fmt = "%s, %s"
                    aggl_run_json = fmt % \
                            (aggl_run_json, self.parsers['mtr'].parse(root + '/' + f))
                    is_first = False

        aggl_run_json = "%s ] }}" % (aggl_run_json)
        print aggl_run_json
