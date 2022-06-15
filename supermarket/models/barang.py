from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _barang(models.Model):
    # Atrribute dari class
    _name = 'supermarket.barang'
    _description = 'Class Barang Supermarket'

    id_barang = fields.Char('ID Barang', size=64, required=True, index=True, readonly=True, default='new',
                        states={})
    name = fields.Char('Nama', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    stok = fields.Integer('Stok', required=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    tanggal = fields.Date('Tanggal Barang Masuk', default=fields.Date.context_today)

    harga = fields.Integer('Harga', required=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    expired = fields.Date('Tanggal Expired', default=fields.Date.context_today)

    hari_sebelum_expired = fields.Integer(string="Hari Sebelum Expired", compute="_compute_hari_sebelum_expired", store=True)

    merek_id = fields.Many2one('supermarket.merek', string='Nama Merek', readonly=True, ondelete="cascade",
                            states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")

    kategori_id = fields.Many2one('supermarket.kategori', string='Nama Kategori', readonly=True, ondelete="cascade",
                            states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_unik', 'unique(id_barang)', _('ID barang Must be unique!')),
                        ('cek_harga', 'CHECK (harga>0)', 'Harga Must be Greater than 0!'),
                        ('cek_stok', 'CHECK (stok>0)', 'Stok Harus Lebih Dari 0!')]

    #UPDATE STOK
    detail_transaksi_ids = fields.One2many('supermarket.detail_transaksi', 'barang_id', string='Transaksi')
    sisa_stok = fields.Integer('Sisa Stok', compute="_compute_sisa_stok", store=True, default=0)

    @api.depends('detail_transaksi_ids', 'detail_transaksi_ids.state', 'detail_transaksi_ids.barang_id', 'detail_transaksi_ids.jumlah_barang', 'stok')
    def _compute_sisa_stok(self):
        for _barang in self:
            val = {
                'sisa_stok': _barang.stok
            }
            for rec in _barang.detail_transaksi_ids:
                val['sisa_stok'] -= rec.jumlah_barang
            _barang.update(val)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('expired', 'tanggal')
    def _compute_hari_sebelum_expired(self):
        for _barang in self:
            if _barang.expired and _barang.tanggal:
                for rec in _barang:
                    hari_sebelum_expired = int((rec.expired - rec.tanggal).days)
                    rec.hari_sebelum_expired = hari_sebelum_expired

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "supermarket.barang")])
            if not seq:
                raise UserError(_("supermarket.barang sequence not found, please create supermarket.barang sequence"))
            for val in vals_list:
                val['id_barang'] = seq.next_by_id()
            return super(_barang, self).create(vals_list)