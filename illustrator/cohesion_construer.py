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

#from illustrator.illustrator_core import Construer

import json
from colorama import Fore, Back, Style
import networkx as nx
import matplotlib.pyplot as plt
from collections import Callable
from sets import Set

class Construer:
    """
    Core Construer Iface
    """
    def __init__(self, aggreg_run_data, args):
        pass

    def do_graphical(self):
        raise  NotImplementedError

    def do_term(self, args):
        raise  NotImplementedError

    @staticmethod
    def traverse(obj, callback=None):
        cb_res = callback(obj)

        if cb_res == "recurse":
            pass
        else:
            return obj

        if isinstance(obj, dict):
            {k: Construer.traverse(v, callback)
                     for k, v in obj.items()}
        elif isinstance(obj, list):
            [Construer.traverse(elem, callback)
                     for elem in obj]
        else:
            return obj 

class CohesionTermCb(Callable):
    def __init__(self):
        self.data_refining = {}
        self.service_fmt = "* srv: %s (%s)"
        self.curr_host = None
        self.curr_conn = Set([])
        self.curr_disj = Set([])
        # coe - course of events
        self.coe_track = { "curr_run" : 0,  "num_runs" : 0}

    def __call__(self, obj):

        progress = self.predicate(obj)

        if progress == "service":
            if obj["@portid"] not in self.data_refining.keys():
                srv = obj["service"]
                repres = self.service_fmt % (srv["@name"], obj["@portid"])
                self.form_refined_entry(repres , obj["@portid"])

            if obj["state"]["@state"] == "open":
                self.curr_conn.add(obj["@portid"])
            else:
                self.curr_disj.add(obj["@portid"])

            # ugily depending on order
            self.replenish()

        elif progress == "host":
            self.coe_track["curr_run"] += 1
            hostname = obj["hostname"]
            if isinstance(hostname, list):
                for variant in hostname:
                    if variant["@type"] == "user":
                        self.curr_host = variant["@name"]
            elif isinstance(hostname, dict):
                self.curr_host = hostname["@name"]

        elif progress == "scan":
            self.coe_track["num_runs"] = len(obj)
            #in next host: so replenish cached conn/host data
            # map since no zip_longest
            progress = "recurse"

        #if self.is_last_run():
            #self.replenish()

        return progress

    # TODO consider Lists
    @staticmethod
    def append_str(str1, str2):
        fmt = "%s %s"
        str1 = fmt % (str1, str2)
        return str1

    def replenish(self):
        for port_disj, port_con in map(None, self.curr_disj, self.curr_conn): 
            if port_con:
                self.data_refining[str(port_con)]["conn"] = \
                        CohesionTermCb.append_str(self.data_refining[str(port_con)]["conn"], \
                        self.curr_host)
            if port_disj:
                self.data_refining[str(port_disj)]["disj"] = \
                        CohesionTermCb.append_str(self.data_refining[str(port_disj)]["disj"], \
                        self.curr_host) 
        self.curr_conn = Set([])
        self.curr_disj = Set([])
        self.srv_done = False
        self.hosts_done = False

    def is_last_run(self):
        return self.coe_track["num_runs"] == self.coe_track["curr_run"]

    def is_run_done(self):
        return self.srv_done == True and self.hosts_done == True

    def predicate(self, obj):

        if isinstance(obj, dict) and "@portid" in obj.keys():
            return "service"
        elif isinstance(obj, dict) and "hostname" in obj.keys():
            return "host"
        elif isinstance(obj, list) and "nmaprun" in obj[0].keys():
            return "scan"
        else:
            return "recurse"

    def form_refined_entry(self, repres, p_id):
        new_entry = {"repres": repres, "conn" : "connected", "disj" : "disjoined" } 
        self.data_refining[p_id] = new_entry

    def show(self):
        for out_elem in self.data_refining.values():
            print out_elem["repres"]
            print out_elem["conn"]
            print out_elem["disj"]

class Cohesion(Construer):
    """
    Depicting insights regarding distributed nodes cohesion 
    on several net stack layers
    """
    def __init__(self, aggreg_run_data):
        self.run_data = aggreg_run_data

    def do_graphical(self):
        #G=nx.Graph([(0,1),(1,2),(2,3)])

        #nx.draw(G)
        #plt.savefig(".png")
        raise  NotImplementedError

    def do_term(self, args):
        inter_data = json.loads(self.run_data)
        run = inter_data["run"]

        print (">>objective: [%s]" % (args.curr_subcmd))

        for scaffold_node, scan in run["nmap"].items():
            print ( Fore.BLUE + "--- scaffold_node: %s" % (scaffold_node))
            print(Style.RESET_ALL)
            cb = CohesionTermCb()
            Construer.traverse(scan, cb)
            cb.show()
