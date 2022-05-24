from odoo import models, fields, api, _
class mk(models.Model):
    _name = 'nilai.mk'
    _description = 'class untuk menyimpan data mata kuliah'

    name = fields.Char('Nama MK', size = 10, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    code = fields.Char('Kode MK', size=60, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    credit = fields.Integer('Jumlah SKS', required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik', 'unique(name)', _('Nama MK must be unique!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'