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

import openerp.addons.odoolightwf as ltwf


# To use a light workflow, all you need is to inherit from WorkflowModel,
# and to set up a few attributes and a 'state' field, as demonstrated in this class.
class SuperHero(ltwf.WorkflowModel):
    _name = 'superhero'

    # The workflow is set up according to the _states and _transitions attributes.
    # No new objects are created in the database, only the 'state' field (defined later) is used
    # to track the workflow.
    _states = [
        # (<technical name>, <pretty name>),
        ('x', 'Not Certified'),
        ('a', 'Rank A'),
        ('b', 'Rank B'),
        ('c', 'Rank C'),
        ('d', 'Rank D'),
        ('e', 'Rank E'),
    ]
    _transitions = [
        # Transitions can be lists of the form:
        # [<trigger>, <source>, <dest>, <conditions>, <unless>, <before>, <after>, <prepare>]
        # where everything after dest is optional.
        # trigger is the name of the trigger. it has to be a valid Python identifier.
        # source and dest are the names of source and destination states
        # conditions and unless's are predicate methods (methods that return true or false)
        # a transition may only occur if all its conditions are true, and all its unless's are false
        # 'prepare' methods happen first, whether conditions are met or not
        # 'before' methods are executed before the state is changed, if conditions are met
        # 'after' methods are executed after the state is changed, if conditions are met
        # (methods are always specified by name, not with a function object.)
        ['certify', 'x', 'a', 'valid_phone', None, None, 'gain_prestige'],
        ['promote', 'a', 'b', None, None, None, 'gain_prestige'],
        ['promote', 'b', 'c', None, None, None, 'gain_prestige'],
        # To execute a multiple methods, simply use a list instead:
        ['promote', 'c', 'd', None, None, None, ['gain_prestige', 'do_nothing']],
        ['promote', 'd', 'e', None, None, None, 'gain_prestige'],
        # Alternatively, transitions can be defined with dicts.
        # dict and list definitions can be mixed in the same workflow:
        {'trigger': 'demote', 'source': 'e', 'dest': 'd'},
        {'trigger': 'demote', 'source': 'd', 'dest': 'c'},
        {'trigger': 'demote', 'source': 'c', 'dest': 'b'},
        {'trigger': 'demote', 'source': 'b', 'dest': 'a'},
        # A transition can have multiple sources, using lists:
        {'trigger': 'disbar', 'source': ['x', 'a', 'b', 'c', 'd', 'e'], 'dest': 'x', 'after': 'shame'},
        # Or it can have all states as source:
        {'trigger': 'disbar', 'source': '*', 'dest': 'x', 'after': 'shame'},
    ]

    # The state field is special. It must be a selection field, with the same
    # selections as the _states attribute. It is recommended to make it
    # readonly and to never write to it from business methods, else the
    # workflow may be bypassed.
    # (Conversely, if you WANT to bypass the workflow, you can simply write the
    # 'state' field directly from a method.)
    state = fields.Selection(
        _states, 'State', default='x', required=True, readonly=True)

    # Just your regular data fields.
    name = fields.Char('Name')
    phone = fields.Char('Phone Number')
    prestige = fields.Integer('Prestige')

    # Currently triggers need to be declared explicitly like this
    # Hopefully we will find a better, less redundant solution
    # Triggers are methods, they can be called from other methods, or
    # from buttons - see superhero.xml for examples.
    certify = ltwf.trigger('certify', 'Certify Hero')
    promote = ltwf.trigger('promote', 'Promote Hero')
    demote = ltwf.trigger('demote', 'Demote Hero')
    disbar = ltwf.trigger('disbar', 'Disbar Hero')

    # Conditions, unless's, before's, after's and prepare's are normal
    # business methods.
    def gain_prestige(self):
        self.write({'prestige': self.prestige + 10})

    def do_nothing(self):
        pass

    def shame(self):
        self.write({'prestige': 0})

    # For conditions and unless methods, the docstring is used as part of the error
    # message when a transition is attempted but conditions are not met.
    def valid_phone(self):
        """Hero must have a valid phone number."""
        return self.phone and bool(len(self.phone))
