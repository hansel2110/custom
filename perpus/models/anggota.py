from odoo import models, fields, api, _

class _anggota(models.Model):
    # Atrribute dari class
    _name = 'perpus.anggota'
    _description = 'Class Anggota Perpustakaan'

    id_anggota = fields.Char('ID Anggota', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    name = fields.Char('Nama', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    no_telepon = fields.Char('No Telepon', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('name_unique', 'unique(id_anggota)', _('ID Anggota Must be Unique'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'