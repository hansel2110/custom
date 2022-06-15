from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    poin = fields.Integer('Poin', compute="_compute_poin", store=True, default=0)

    #UPDATE POIN
    transaksi_ids = fields.One2many('supermarket.transaksi', 'customer_id', string='Transaksi')

    @api.depends('transaksi_ids', 'transaksi_ids.penggunaan_poin', 'transaksi_ids.total_transaksi', 'poin')
    def _compute_poin(self):
        for ResPartner in self:
            val = {
                'poin': 0
            }
            for rec in ResPartner.transaksi_ids:
                if rec.penggunaan_poin == 'tidak':
                    val['poin'] += (rec.total_transaksi * 0.01)
                else:
                    val['poin'] = 0
            ResPartner.update(val)