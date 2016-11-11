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

class Cohesion(Construer):
    """
    Depicting insights regarding distributed nodes cohesion 
    on several net stack layers
    """
    def __init__(self, aggreg_run_data):
        self.run_data = aggreg_run_data

    def do_graphical(self):
        raise  NotImplementedError

    def do_term(self, args):
        inter_data = json.loads(self.run_data)

        print (">>objective: [%s]" % (args.curr_subcmd))

        run = inter_data["run"]
        
        self.visit_ctx = [ ]

        for scaffold_node in run["nmap"]:
            print ( Fore.BLUE + "--- scaffold_node: %s" % (scaffold_node))
            print(Style.RESET_ALL)
            for scan in run["nmap"][scaffold_node]:
                scan_content = scan ["nmaprun"] 
                if type(scan_content["host"]) == dict:
                    self.do_term_host_p(scan_content["host"])
                else:
                    for scanned_host in scan_content["host"]:
                        self.do_term_host_p(scanned_host)

            for out in self.visit_ctx:
                print "%s \n %s \n %s \n " % (out["repres"], \
                        out["conn"], out["disj"])
            self.visit_ctx = []
  
    def do_term_host_p(self, scanned_host): 
        ports = scanned_host["ports"]
        for srv in ports["port"]:
            if srv["@portid"] not in [ ctx_elem["@portid"] for ctx_elem in self.visit_ctx ]:
                repres = "* srv: %s (%s)" % (srv["service"]["@name"], srv["@portid"])
                self.form_visit_ctx(repres , srv["@portid"])
            curr_ctx = filter(lambda x: srv["@portid"] == x["@portid"], self.visit_ctx)[0]
            if scanned_host["hostnames"] is None:
                continue
            #TODO REFACTOR
            if type(scanned_host["hostnames"]["hostname"]) == dict:
                host_name = scanned_host["hostnames"]["hostname"]
                if host_name["@type"] == "user":
                    if srv["state"]["@state"] == "open":
                        curr_ctx["conn"] = "%s %s" % (curr_ctx["conn"], host_name["@name"])
                    else:
                        curr_ctx["disj"] = "%s %s" % (curr_ctx["disj"], host_name["@name"])
                continue
            for host_name in scanned_host["hostnames"]["hostname"]:
                if host_name["@type"] == "user":
                    if srv["state"]["@state"] == "open":
                        curr_ctx["conn"] = "%s %s" % (curr_ctx["conn"], host_name["@name"])
                    else:
                        curr_ctx["disj"] = "%s %s" % (curr_ctx["disj"], host_name["@name"])

    def form_visit_ctx(self, repres, p_id):
        new_ctx = { "@portid": p_id, "repres": repres, "conn" : "connected", "disj" : "disjoined" } 
        self.visit_ctx.append(new_ctx)
        
