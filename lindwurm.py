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
import jinja2


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

        #Todo: sane defs.
        # and better mainten
        self.cohesion_parser.add_argument('--n_prots', help=guidance['cohesion']['args_descr']['--n_prots'])
        self.cohesion_parser.add_argument('--t_serv' , help=guidance['cohesion']['args_descr']['--t_serv'])
        self.cohesion_parser.add_argument('--t_ports', help=guidance['cohesion']['args_descr']['--t_ports'])
        self.cohesion_parser.add_argument('-f', '--format', help=guidance['cohesion']['args_descr']['--format'], default='Plain')

        self.quality_parser = self.lw_subparsers.add_parser('quality', description=guidance['quality']['descr'])

        self.substance_parser = self.lw_subparsers.add_parser('substance', description=guidance['substance']['descr'])

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

    def param_revealer(self, **seed_args):
        # roles loc
        modules_root = self.conf.get('revealer', 'modules_root')
        templateLoader = jinja2.FileSystemLoader( searchpath=modules_root)
        templateEnv = jinja2.Environment( loader=templateLoader )

        reveal_mod_cfg_template_f = os.path.join(modules_root, 'core', 'templates', 'cnfg.j2')
        reveal_mod_cfg_template = templateEnv.get_template( reveal_mod_cfg_template_f )

        # ONLY FROM ARGS OR MORE?
        conf_seed = seed_args 

        conf_seed_data = reveal_mod_cfg_template.render( conf_seed )

        conf_seed_f = os.path(modules_root, self.args.curr_subcmd, 'vars', 'main.yml')
        with open(conf_seed_f, 'wb') as out_f:
            out_f.write(conf_seed_data)

    def run(self):
        construer = self.illustrator.conjure(self.args.curr_subcmd)

        #construer.do_graphical()

        construer.do_term(self.args)

if __name__ == "__main__":
    lindwurm = Lindwurm()

    lindwurm.parse_args()

    lindwurm.run()
