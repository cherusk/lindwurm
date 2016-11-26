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

from parser.aggregator import Aggregator
from cohesion_construer import Cohesion
from substance_construer import Substance
from quality_construer import Quality 
import ConfigParser
import os

class Illustrator:
    """ Hub module for depicting revealer aggregated intelligence 
        in various facettes. 
    """
    def __init__(self, settings):
        #Todo partition settings
        self.aggregator = Aggregator(settings) 

    def conjure(self, submodule):
        self.aggreg_data = self.aggregator.run() 
        #print self.aggreg_data

        former = getattr(self, submodule, "unknown")

        if former == "unknown":
            raise RuntimeError("unknown submodule")

        construer = former()

        return  construer

    def cohesion(self):
        return Cohesion(self.aggreg_data)
    
    def substance(self):
        return Quality(self.aggreg_data)

    def substance(self):
        return Substance()
