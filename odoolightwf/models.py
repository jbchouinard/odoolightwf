# OdooLightWorkflow, a lightweight workflow engine for Odoo
# Copyright (C) 2016 Savoir-faire Linux

# This file if part of OdooLightWorkflow.
#
# OdooLightWorkflow is free software: you can redistribute it and/or modify it
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
from functools import partial

from openerp import api, models
from transitions import Machine


CALLBACK_CATEGORIES = ('conditions', 'unless', 'before', 'after', 'prepare')


def normalize_transition(t):
    if isinstance(t, list):
        newtrans = {
            'trigger': t[0],
            'source': t[1],
            'dest': t[2],
            'conditions': (len(t) > 3 and t[3]) or [],
            'unless': (len(t) > 4 and t[4]) or [],
            'before': (len(t) > 5 and t[5]) or [],
            'after': (len(t) > 6 and t[6]) or [],
            'prepare': (len(t) > 7 and t[7]) or [],
        }
    elif isinstance(t, dict):
        newtrans = {
            'trigger': t['trigger'],
            'source': t['source'],
            'dest': t['dest'],
            'conditions': t.get('conditions', None) or [],
            'unless': t.get('unless', None) or [],
            'before': t.get('before', None)or [],
            'after': t.get('after', None) or [],
            'prepare': t.get('prepare', None) or [],
        }
    else:
        raise TypeError('Not a valid transition: %s' % t)
    for cat in CALLBACK_CATEGORIES:
        item = newtrans[cat]
        if not isinstance(item, list):
            newtrans[cat] = [item]
    return newtrans


class WorkflowModel(models.BaseModel):
    _auto = True
    _register = False
    _transient = False

    _machine = None

    @api.multi
    def _create_machine(self):
        self.ensure_one()
        callbacks = []
        ts = []
        for t in self._transitions:
            norm_t = normalize_transition(t)
            for cat in CALLBACK_CATEGORIES:
                callbacks += norm_t[cat]
            norm_t['after'].append('_update_model_state')
            ts.append(norm_t)

        states = [t[0] for t in self._states]
        machine = Machine(
            states=states, transitions=ts, initial=self.state)

        # TODO: _update_model_state shouldn't be in callbacks to begin with
        callbacks = set(callbacks) - set(('_update_model_state',))
        for cb in callbacks:
            setattr(machine, cb, partial(getattr(self, cb)))

        def _update_model_state():
            self.state = machine.state

        machine._update_model_state = _update_model_state
        return machine

    @property
    def machine(self):
        if not self._machine:
            self._machine = self._create_machine()
        return self._machine
