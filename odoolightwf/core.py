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
from openerp import api
from openerp.exceptions import ValidationError
from transitions import MachineError


class WorkflowError(ValidationError):
    def __init__(self, msg):
        super(WorkflowError, self).__init__(msg)


def trigger(fname, fdoc=None):
    @api.multi
    def func(self):
        self.ensure_one()
        try:
            res = getattr(self.machine, fname)()
        except MachineError:
            state = dict(self._states)[self.state]
            action = fdoc if fdoc else fname
            msg = 'Action "%s" cannot be done from state "%s"'
            msg = msg % (action, state)
            raise WorkflowError(msg)
        if not res:
            action = fdoc if fdoc else fname
            msg_parts = ['These conditions must be met to %s:' % action]
            t = [t for t in self._transitions
                 if t['trigger'] == fname and t['source'] == self.state][0]
            conds = t.get('conditions', [])
            for cd in conds:
                cdfunc = getattr(self, cd)
                msg = getattr(cdfunc, '__doc__', cdfunc.__name__)
                if msg:
                    msg_parts.append(msg)
            raise WorkflowError('\n'.join(msg_parts))
        return res
    func.__name__ = fname
    func.__doc__ = fdoc
    return func
