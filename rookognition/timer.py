#Rookognition - A web-based chess vision exercise.
#Copyright (C) 2025 Nick Edner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
import time

class Timer:
    def __init__(self):
        self.start_time = time.perf_counter_ns()

    def elapsed(self, radix=5):
        return round((time.perf_counter_ns() - self.start_time)/1000000000,int(radix))
