#    Copyright 2018 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
from random import randint, choice
import jsonschema

from dwave_structural_imbalance_demo.interfaces import GlobalSignedSocialNetwork, _qpu
from dwave_structural_imbalance_demo.json_schema import json_schema


class TestInterfaces(unittest.TestCase):
    gssn = GlobalSignedSocialNetwork()

    def test_get_node_link_data_output(self):
        subgroup = choice(['Global', 'Syria', 'Iraq'])
        year = randint(2007, 2016)
        output = self.gssn.get_node_link_data(subgroup, year)
        jsonschema.validate(output, json_schema)

    def test_solve_structural_imbalance_output(self):
        subgroup = 'Syria'
        year = 2013
        output = self.gssn.solve_structural_imbalance(subgroup, year)
        jsonschema.validate(output, json_schema)

    def test_invalid_subgroup(self):
        subgroup = 'unknown_subgroup'
        self.assertRaises(KeyError, self.gssn.get_node_link_data, subgroup)
        self.assertRaises(KeyError, self.gssn.solve_structural_imbalance, subgroup)

    def test_invalid_year(self):
        year = 'not_an_integer'
        self.assertRaises(ValueError, self.gssn.get_node_link_data, year=year)
        self.assertRaises(ValueError, self.gssn.solve_structural_imbalance, year=year)

    def test_year_zero(self):
        year = 0
        output = self.gssn.get_node_link_data(year=year)
        self.assertFalse(output['nodes'])
        self.assertFalse(output['links'])

    @unittest.skipIf(not _qpu, "Requires access to QPU via dwave-system")
    def test_year_zero_qpu(self):
        year = 0
        output = self.gssn.solve_structural_imbalance(year=year)
        self.assertFalse(output['nodes'])
        self.assertFalse(output['links'])

    @unittest.skipIf(_qpu, "Can only be tested if dwave-system isn't installed")
    def test_qpu_without_dwave_system(self):
        self.assertRaises(NameError, GlobalSignedSocialNetwork, True)
