from odoo import models, fields, api, _

class _admin(models.Model):
    # Atrribute dari class
    _name = 'perpus.admin'
    _description = 'Class Admin Perpustakaan'

    id_admin = fields.Char('ID Admin', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    name = fields.Char('Nama Admin', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    email_admin = fields.Char('Email Admin', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    no_telepon_admin = fields.Char('No Telepon Admin', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    alamat_admin = fields.Char('Alamat Admin', size=64, required=True, index=True, readonly=True,
                         states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('name_unique', 'unique(id_admin)', _('ID Admin Must be Unique'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'