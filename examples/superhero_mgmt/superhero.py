# OdooLightWorkflow, a lightweight workflow engine for Odoo
# Copyright (C) 2016 Savoir-faire Linux

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
from openerp import fields

from . import odoolightwf as ltwf


class SuperHero(ltwf.WorkflowModel):
    _name = 'superhero'
    _states = [
        ('x', 'Not Certified'),
        ('a', 'Rank A'),
        ('b', 'Rank B'),
        ('c', 'Rank C'),
        ('d', 'Rank D'),
        ('e', 'Rank E'),
    ]
    _transitions = [
        # Transitions can be lists of the form:
        # [trigger, source, dest, conditions, unless, before, after, prepare]
        # where everything after dest is optional
        ['certify', 'x', 'a', 'valid_phone', None, None, 'gain_prestige'],
        ['promote', 'source', 'a', 'b', None, None, None, 'gain_prestige'],
        ['promote', 'source', 'b', 'c', None, None, None, 'gain_prestige'],
        ['promote', 'source', 'c', 'd', None, None, None, 'gain_prestige'],
        ['promote', 'source', 'd', 'e', None, None, None, 'gain_prestige'],
        # Alternatively, they can be dicts:
        {'trigger': 'demote', 'source': 'e', 'dest': 'd'},
        {'trigger': 'demote', 'source': 'd', 'dest': 'c'},
        {'trigger': 'demote', 'source': 'c', 'dest': 'b'},
        {'trigger': 'demote', 'source': 'b', 'dest': 'a'},
        {'trigger': 'disbar', 'source': '*', 'dest': 'x', 'after': ['shame']},
    ]

    name = fields.Char('Name')
    phone = fields.Char('Phone Number')
    state = fields.Selection(
        _states, 'State', default='x', required=True, readonly=True)
    prestige = fields.Integer('Prestige')

    certify = ltwf.trigger('certify', 'Certify Hero')
    promote = ltwf.trigger('promote', 'Promote Hero')
    demote = ltwf.trigger('demote', 'Demote Hero')
    disbar = ltwf.trigger('disbar', 'Disbar Hero')

    def gain_prestige(self):
        self.write({'prestige': self.prestige + 10})

    def shame(self):
        self.write({'prestige': 0})

    def valid_phone(self):
        """Hero must have a valid phone number."""
        return self.phone and bool(len(self.phone))
