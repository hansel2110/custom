from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _kategori(models.Model):
    # Atrribute dari class
    _name = 'supermarket.kategori'
    _description = 'Class Kategori Supermarket'

    id_kategori = fields.Char('ID Kategori', size=64, required=True, index=True, readonly=True, default='new',
                        states={})
    name = fields.Char('Nama Kategori', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    deskripsi_kategori = fields.Char('Deskripsi', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_kategori_unik', 'unique(id_kategori)', _('ID kategori Must be unique!')),
                        ('id_unik', 'unique(name)', _('Nama kategori Must be unique!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "supermarket.kategori")])
            if not seq:
                raise UserError(_("supermarket.kategori sequence not found, please create supermarket.kategori sequence"))
            for val in vals_list:
                val['id_kategori'] = seq.next_by_id()
            return super(_kategori, self).create(vals_list)