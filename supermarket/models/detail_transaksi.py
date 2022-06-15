from odoo import models, fields, api, _

class _detail_transaksi(models.Model):
    _name = 'supermarket.detail_transaksi'
    _description = 'Class Detail Transaksi Supermarket'

    diskon_barang = fields.Integer('Diskon Barang (%)', store=True, default=0)
    jumlah_barang = fields.Integer('Jumlah Barang', store=True, default=0)
    harga_barang = fields.Integer('Harga', related='barang_id.harga')
    total_harga_barang = fields.Integer(string="Total Harga Barang", compute="_compute_total_harga_barang", store=True)

    transaksi_id = fields.Many2one('supermarket.transaksi', string='ID Transaksi', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    barang_id = fields.Many2one('supermarket.barang', string='Nama Barang', readonly=True, ondelete="cascade",
                            states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    temp = fields.Integer('Temp')

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('harga_barang', 'jumlah_barang', 'diskon_barang')
    def _compute_total_harga_barang(self):
        for _detail_transaksi in self:
            val = {
                'total_harga_barang': 0,
            }
            for rec in _detail_transaksi:
                val['total_harga_barang'] = (rec.harga_barang - ((rec.harga_barang * rec.diskon_barang)/100)) * rec.jumlah_barang
            _detail_transaksi.update(val)