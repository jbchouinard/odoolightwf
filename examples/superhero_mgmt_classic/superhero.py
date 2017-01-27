# OdooLightWorkflow, a lightweight workflow engine for Odoo
# Copyright (C) 2016,2017 Savoir-faire Linux

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
from openerp import api, fields, models


class SuperHero(models.Model):
    _name = 'superhero.classic'

    _states = [
        ('x', 'Not Certified'),
        ('a', 'Rank A'),
        ('b', 'Rank B'),
        ('c', 'Rank C'),
        ('d', 'Rank D'),
        ('e', 'Rank E'),
    ]

    name = fields.Char('Name')
    phone = fields.Char('Phone Number')
    prestige = fields.Integer('Prestige')
    state = fields.Selection(
        _states, 'State', default='x', required=True, readonly=True)

    @api.multi
    def gain_prestige(self):
        for rec in self:
            rec.write({'prestige': self.prestige + 10})

    @api.multi
    def do_nothing(self):
        pass

    @api.multi
    def shame(self):
        for rec in self:
            rec.write({'prestige': 0})

    @api.multi
    def valid_phone(self):
        self.ensure_one()
        return self.phone and bool(len(self.phone))
