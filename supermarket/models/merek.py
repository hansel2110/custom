from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _merek(models.Model):
    # Atrribute dari class
    _name = 'supermarket.merek'
    _description = 'Class Merek Supermarket'

    id_merek = fields.Char('ID Merek', size=64, required=True, index=True, readonly=True, default='new',
                        states={})
    name = fields.Char('Nama Merek', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    produsen = fields.Char('Produsen', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    deskripsi = fields.Char('Deskripsi', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_merek_unik', 'unique(id_merek)', _('ID Merek Must be unique!')),
                        ('id_unik', 'unique(name)', _('Nama Merek Must be unique!'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "supermarket.merek")])
            if not seq:
                raise UserError(_("supermarket.merek sequence not found, please create supermarket.merek sequence"))
            for val in vals_list:
                val['id_merek'] = seq.next_by_id()
            return super(_merek, self).create(vals_list)