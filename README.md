# OdooLightWorkflow

An alternative, lighter workflow for Odoo models, based on the `transitions`
finite state machine Python module.

## Version

This project is in development and not currently stable.

## Usage

Make your model inherit from `openerp.addons.odoolightwf.WorkflowModel` instead
of `openerp.models.Model` to add workflow functionality to a model.

See the module in the examples directory for a detailed example of worflow usage.
