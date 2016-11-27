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
import subprocess
from illustrator.illustrator_core import Illustrator
import jinja2
from collections import Callable

#description data
guidance = {
        'lindwurm' : """
        Ad hoc distributed systems pervasion and introspection equipment. 
        """,
        'subcmds' : """
        <<< Subcommands >>>
        """,
        'cohesion' : 
        {
            'descr': """
            Module does investigate connection outline of a distributed environment and report outcome in various on purpose variants. 
            """,
            'epilog' : """
            ---
            """,
            'args_descr' : {
                'objectives' : """
                Abstract wayers which the submodule should focus on for this run: link, network, transport
                """,
                '--n_prots' : """
                Protocols to investigate on network level. 
                """,
                '--t_serv' : """
                Services to investigate on transport level.
                """,
                '--t_ports' : """
                Ports to investigate on transport level. (Complementary to --t_serv)
                """ ,
                '--format' : """
                Alternative out formats: Json | Tree | Plain
                """
                }
            },
        'quality' : 
        {
            'descr': """
            """,
            'epilog' : """
            ---
            """,
            'args_descr' : {
                'objectives' : """
                Submodule for doing an ad hoc distributed quality investigation
                """,
                '--n_prots' : """
                """,
                '--t_serv' : """
                """,
                '--t_ports' : """
                """ ,
                '--format' : """
                """
                }
            },
        'substance': 
        {
            'descr': """
            Module to action a distributed tracing run
            """,
            'epilog' : """
            ---
            """,
            'args_descr' : {
                'objectives' : """
                """,
                '--n_prots' : """
                """,
                '--t_serv' : """
                """,
                '--t_ports' : """
                """ ,
                '--format' : """
                """
                }
            }
        }


class ParamsRefineCb(Callable):

    #todo mapping
    lw_to_ans_map = {
        "cohesion" : {
            "opts" : { "args" : [ "n_prots", "t_serv", "t_ports" ] }
        },
        "quality" : {},
        "substance" : {}
    }

    def __init__(self, submodule):
        self.submod = submodule
        self.action =  getattr(self, submodule, "unknown")

        if self.action == "unknown":
            raise RuntimeError("unknown submodule")

    def __call__(self, args):
        params = self.action(args)
        return params 

    def cohesion(self, args):
        params = {}
        #for param in lw_to_ans_map[self.submod]:
            #for arg in param['args']:
                #if param == "opts":
        #if 'link' in args.objectives:
            #l_args = ''

        #if 'network' in args.objectives:
            #n_args= 

        #basic start
        if 'transport' in args.objectives:
            print args
            params["opts"] = '-sS -p '

            if args.t_ports:
                params["opts"] = "\"%s %s \"" % ( params['opts'], args.t_ports )

        return params

    def quality(self, args):
        raise  NotImplementedError

    def substance(self, args):
        raise  NotImplementedError

class Launcher:
    def __init__(self, config):
        self.conf = config
        self.ansible_cmd = ['ansible-playbook']

    def launch(self, submodule, params):
        revealer = "%s_%s%s" % ( submodule, 'revealer', '.yml' )
        revealer_p = os.path.join( self.conf.get('DEFAULT', 'lindwurm_dir'), 'revealer', revealer) 

        self.ansible_cmd.append(revealer_p)

        self.param_revealer(submodule, **params)

        p = subprocess.Popen(" ".join(self.ansible_cmd), stdout=subprocess.PIPE, shell=True)

        #ToDo: make use p communication 
        (out, err) = p.communicate()
        
        print out
        print err

        p_status = p.wait()

    def param_revealer(self, submodule, **seed_args):
        # roles loc
        modules_root = self.conf.get('revealer', 'modules_root')
        templateLoader = jinja2.FileSystemLoader( searchpath=modules_root)
        templateEnv = jinja2.Environment( loader=templateLoader )

        reveal_mod_cfg_template_f = os.path.join('.', 'core', 'templates', 'cnfg.j2')
        reveal_mod_cfg_template = templateEnv.get_template( reveal_mod_cfg_template_f )

        print seed_args
        # ONLY FROM ARGS OR MORE?
        conf_seed = { 'conf_seed' :  seed_args }

        conf_seed_data = reveal_mod_cfg_template.render( conf_seed )

        #todo solve param distribution
        conf_seed_f = os.path.join(modules_root, 'core', 'vars', 'params.yml')
        with open(conf_seed_f, "w+") as out_f:
            out_f.write(conf_seed_data)

class Lindwurm:
    def __init__(self):

        self.load_cnfg()

        # Todo descriptions
        self.lw_parser = argparse.ArgumentParser(description=guidance['lindwurm'])
        self.lw_subparsers = \
                self.lw_parser.add_subparsers(description=guidance['subcmds'], dest='curr_subcmd')

        self.cohesion_parser = self.lw_subparsers.add_parser('cohesion', description=guidance['cohesion']['descr'])
        self.cohesion_parser.add_argument('objectives', metavar='obj', nargs='+', \
                choices=['link', 'net', 'transport'], help=guidance['cohesion']['args_descr']['objectives']) 

        #Todo: sane ggdefs.
        # and better mainten
        self.cohesion_parser.add_argument('--n_prots', help=guidance['cohesion']['args_descr']['--n_prots'])
        self.cohesion_parser.add_argument('--t_serv' , help=guidance['cohesion']['args_descr']['--t_serv'])
        self.cohesion_parser.add_argument('--t_ports', help=guidance['cohesion']['args_descr']['--t_ports'])
        self.cohesion_parser.add_argument('-f', '--format', help=guidance['cohesion']['args_descr']['--format'], default='Plain')

        self.quality_parser = self.lw_subparsers.add_parser('quality', description=guidance['quality']['descr'])

        self.substance_parser = self.lw_subparsers.add_parser('substance', description=guidance['substance']['descr'])

        self.illustrator = Illustrator(self.config)
        self.launcher = Launcher(self.config)

    def parse_args(self):
        self.args = self.lw_parser.parse_args()
        self.params = self.distil_params(self.args)

    def distil_params(self, args):
        distiller = ParamsRefineCb(args.curr_subcmd)
        params = distiller(args)
        return params 

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

        self.launcher.launch(self.args.curr_subcmd, self.params)

        construer = self.illustrator.conjure(self.args.curr_subcmd)

        #construer.do_graphical()

        construer.do_term(self.args)

if __name__ == "__main__":
    lindwurm = Lindwurm()

    lindwurm.parse_args()

    lindwurm.run()
