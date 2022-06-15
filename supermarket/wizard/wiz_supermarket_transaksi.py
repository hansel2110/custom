from odoo import models, fields, api, _

# _ untuk translate

class wiztransaksi(models.TransientModel):
    _name = 'wiz.supermarket.transaksi'
    _description = 'class untuk menyimpan data transaksi dan supermarket'

    transaksi_id = fields.Many2one('supermarket.transaksi', String='Transaksi')

    tgl_transaksi = fields.Date(related='transaksi_id.tgl_transaksi')
    total_barang = fields.Integer(related='transaksi_id.total_barang')

    detail_transaksi_ids = fields.One2many('wiz.supermarket.transaksi.lines', 'wiz_header_id', string='Supermarket')

    def action_confirm(self):
       for rec in self.detail_transaksi_ids:
           rec.ref_transaksi_lines_id.jumlah_barang = rec.jumlah_barang
           rec.ref_transaksi_lines_id.diskon_barang = rec.diskon_barang

    @api.model
    def default_get(self, fields_list):
        res = super(wiztransaksi, self).default_get(fields_list)
        res['transaksi_id'] = self.env.context['active_id']
        return res

    @api.onchange('transaksi_id')
    def onchange_transaksi_id(self):
        if not self.transaksi_id:
            return
        vals =[]
        detail_transaksi_ids = self.env['wiz.supermarket.transaksi.lines']
        for rec in self.transaksi_id.detail_transaksi_ids:
            detail_transaksi_ids += self.env['wiz.supermarket.transaksi.lines'].new({
                'wiz_header_id': self.id,
                'barang_id': rec.barang_id.id,
                'ref_transaksi_lines_id': rec.id
            })
        self.detail_transaksi_ids = detail_transaksi_ids

class transaksi_lines_wiz(models.TransientModel):
    _name = 'wiz.supermarket.transaksi.lines'
    _description = 'class untuk menyimpan data supermarket suatu transaksi'

    wiz_header_id = fields.Many2one('wiz.supermarket.transaksi', string='Transaksi')
    barang_id = fields.Many2one('supermarket.barang', string='Nama Barang', ondelete="restrict")
    ref_transaksi_lines_id = fields.Many2one('supermarket.detail_transaksi')
    jumlah_barang = fields.Integer('Jumlah Barang')
    harga_barang = fields.Integer(related='barang_id.harga')
    diskon_barang = fields.Integer('Diskon Barang (%)')
    total_harga_barang = fields.Integer(string='Total Harga Barang', compute="_compute_total_harga_barang")

    @api.depends('harga_barang', 'jumlah_barang', 'diskon_barang')
    def _compute_total_harga_barang(self):
        for transaksi_lines_wiz in self:
            val = {
                'total_harga_barang': 0,
            }
            for rec in transaksi_lines_wiz:
                val['total_harga_barang'] = (rec.harga_barang - ((rec.harga_barang * rec.diskon_barang)/100)) * rec.jumlah_barang
            transaksi_lines_wiz.update(val)