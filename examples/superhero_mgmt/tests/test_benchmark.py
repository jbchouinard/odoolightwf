# OdooLightWorkflow, a lightweight workflow engine for Odoo
# Copyright (C) 2017 Savoir-faire Linux

# This file if part of OdooLightWorkflow.
#
# OdooLightWorkflow free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OdooLightWorkflow is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging

from openerp.tests.common import TransactionCase


_logger = logging.getLogger(__name__)
logging.getLogger('transitions.core').propagate = 0


class TestBenchmark(TransactionCase):
    def setUp(self):
        super(TestBenchmark, self).setUp()
        self.hero = self.env['superhero'].create({
            'name': 'One Punch Man',
            'prestige': 0,
            'phone': '5555555555',
        })

    def test_workflow(self):
        self.hero.certify()
        self.hero.promote()
        self.hero.promote()
        self.hero.promote()
        self.hero.promote()
        self.hero.disbar()


for n in range(200):
    setattr(TestBenchmark, 'test_workflow_%i' % n, TestBenchmark.test_workflow)
