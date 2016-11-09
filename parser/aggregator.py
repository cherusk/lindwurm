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

        self.aggr_run = ''
        self.gather_sub_revelation("nmap")
        #inter closu
        self.aggr_run = "%s ," % (self.aggr_run)
        self.gather_sub_revelation("mtr")

        self.aggr_run = Aggregator.encaps_run(self.aggr_run, 'run')

        print self.aggr_run 

    def gather_sub_revelation(self, revelation):
        is_first = {"out_p" : True, "node" : True } 
        out_dir = self.conf.get(self.conf_section, revelation + '_out')

        for root, dirs, files in os.walk(out_dir):
            if root != out_dir:
                revealing_node = os.path.basename(root)
                aggr_revel_n = ''
                for f in files: 
                    fmt = "%s %s" if is_first['out_p'] else "%s, %s"
                    aggr_revel_n = fmt % \
                            (aggr_revel_n, self.parsers[revelation].parse(root + '/' + f))
                    is_first['out_p'] = False
                is_first['out_p'] = True
                self.encaps_revel_node_out(is_first['node'], aggr_revel_n, revealing_node)
                is_first['node'] = False

        self.aggr_run ="\"%s\" : { %s }" % (revelation, self.aggr_run)

    def encaps_revel_node_out(self, is_first, aggr_revel_n, revealing_node):
        fmt = ''
        if is_first: 
            fmt = "%s \"%s\" : [ %s ]"
        else:
            fmt = "%s , \"%s\" : [ %s ]" 
        self.aggr_run = fmt % (self.aggr_run, revealing_node, aggr_revel_n)

    @staticmethod
    def encaps_run(aggr_run, run_spec):
        aggr_run = '{ "%s" : { %s }}' % (run_spec, aggr_run)
        return aggr_run
