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
from asciitree import LeftAligned
from collections import OrderedDict as OD
from asciitree.drawing import BoxStyle, BOX_HEAVY

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
    def traverse(obj, callback=None, **ctx):
        cb_res = callback(obj, **ctx)

        if cb_res == "recurse":
            pass
        else:
            return obj
        
        if isinstance(obj, dict):
            {k: Construer.traverse(v, callback, **ctx)
                     for k, v in obj.items()}
        elif isinstance(obj, list):
            [Construer.traverse(elem, callback, **ctx)
                     for elem in obj]
        else:
            return obj 

class TermTreeConvCb(Callable):
    def __init__(self):
        pass

    def __call__(self, obj):
        progress = self.predicate(obj)

        if 'convers' == progress:
            new_form = { 'connected' : [], 'disjoined' : [] }
            for conn, disj in map(None, obj['connected'], obj['disjoined']):
                if conn:
                    new_form['connected'].append( tuple( [ conn, {} ] ) )
                if disj:
                    new_form['disjoined'].append( tuple( [ disj, {} ] ) )

            obj['connected'] = OD( new_form['connected'] )
            obj['disjoined'] = OD( new_form['disjoined'] )

            del obj['srv']

            progress = 'return'

        return progress 

    def predicate(self, obj):
        if isinstance(obj, dict) and 'srv' in obj.keys():
            return 'convers'
        else:
            return 'recurse'

class CohesionTermCb(Callable):
    def __init__(self):
        self.data_refining = { 'scaffolding' : {  } }
        self.service_fmt = "* srv: %s (%s)"
        self.curr_host = None
        self.curr_conn = Set([])
        self.curr_disj = Set([])

    def __call__(self, obj, **ctx):

        progress = self.predicate(obj)

        if progress == "service":
            scaff_node = ctx['scaff_node'] 
            self.ensure_def_scaff_n(scaff_node)
            if obj["@portid"] not in self.data_refining['scaffolding'][scaff_node]:
                srv = obj["service"]
                self.form_refined_entry(srv, obj["@portid"], scaff_node)

            if obj["state"]["@state"] == "open":
                self.curr_conn.add(obj["@portid"])
            else:
                self.curr_disj.add(obj["@portid"])

            # ugily depending on order
            #in next host: so replenish cached conn/host data
            self.replenish(scaff_node)

        elif progress == "host":
            hostname = obj["hostname"]
            if isinstance(hostname, list):
                for variant in hostname:
                    if variant["@type"] == "user":
                        self.curr_host = variant["@name"]
            elif isinstance(hostname, dict):
                self.curr_host = hostname["@name"]

        return progress

    # TODO consider Lists
    @staticmethod
    def append_str(str1, str2):
        fmt = "%s %s"
        str1 = fmt % (str1, str2)
        return str1

    def ensure_def_scaff_n(self, scaff_node):
        if scaff_node not in self.data_refining['scaffolding'].keys():
            self.data_refining['scaffolding'][scaff_node] = {  } 

    def replenish(self, scaff_node):
        # map since no zip_longest
        curr_scaff_n = self.data_refining['scaffolding'][scaff_node]
        for port_disj, port_con in map(None, self.curr_disj, self.curr_conn): 
            if port_con:
                curr_scaff_n[str(port_con)]["connected"].append(self.curr_host)
            if port_disj:
                curr_scaff_n[str(port_disj)]["disjoined"].append(self.curr_host)
        self.curr_conn = Set([])
        self.curr_disj = Set([])

    def predicate(self, obj):
        if isinstance(obj, dict) and "@portid" in obj.keys():
            return "service"
        elif isinstance(obj, dict) and "hostname" in obj.keys():
            return "host"
        else:
            return "recurse"

    def form_refined_entry(self, srv, p_id, scaff_node):
        new_entry = { "srv" : srv, "connected" : [], "disjoined" : [] }
        self.data_refining['scaffolding'][scaff_node][p_id] = new_entry

    def show(self, what):

        print self.data_refining

        if len(what) == 0 or 'Plain' in what:
            scaffold_nodes = self.data_refining['scaffolding']
            for scaffold_node, ports in scaffold_nodes.items():
                print ( Fore.BLUE + "--- scaffold_node: %s" % (scaffold_node))
                print(Style.RESET_ALL)
                for p_id, ctx in ports.items(): 
                    print self.service_fmt % ( ctx["srv"]['@name'], p_id)
                    for key in [ 'connected', 'disjoined' ]:
                        print CohesionTermCb.append_str(key, " ".join(ctx[key]))

            print "\n"

        # JSON 
        if 'Json' in what:
            print 'JSON \n'
            print json.dumps(self.data_refining)
        
        # maybe deep copy if data reused
        if 'Tree' in what:
            # TREE
            Construer.traverse(self.data_refining, TermTreeConvCb())
            tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY))
            print(tr(self.data_refining))

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

        cb = CohesionTermCb()
        for scaffold_node in run["nmap"]:
            Construer.traverse(run['nmap'][scaffold_node], cb, scaff_node=scaffold_node)
        cb.show(args.format)
