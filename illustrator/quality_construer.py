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

from cohesion_construer import Construer

class Quality(Construer):
    """
    Depicting insights as to whether the overall distributed system 
    interconnection quality 
    """
    def __init__(self, aggreg_run_data):
        pass

    def do_graphical(self):
        raise  NotImplementedError

    def do_term(self, args):
        raise  NotImplementedError
