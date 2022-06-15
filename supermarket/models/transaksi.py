from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _transaksi(models.Model):
    # Atrribute dari class
    _name = 'supermarket.transaksi'
    _description = 'Class Transaksi Supermarket'

    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True, default='new',
                        states={})
    tgl_transaksi = fields.Date('Tanggal Transaksi', default=fields.Date.context_today) # ini jadi nama field / kolom dengan tipe data Date, parameter String ini akan jadi caption / label di form odoo
    total_barang = fields.Integer('Total Barang', compute="_compute_total_barang", store=True, default=0)
    total_transaksi = fields.Integer('Total Transaksi', compute="_compute_total_transaksi", store=True, default=0)

    #POIN BARU YANG DIDAPAT KETIKA TRANSAKSI
    poin_baru = fields.Integer('Poin Yang Didapat', compute="_compute_poin_baru", store=True, default=0)

    penggunaan_poin = fields.Selection([('tidak', 'Tidak'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                                        ('iya', 'Iya')], 'Penggunaan Poin', required=True,
                                        readonly=True, default='tidak',
                                        states={'draft':[('readonly', False)]})
    hemat = fields.Integer('Hemat', compute="_compute_hemat", store=True, default=0)


    customer_id = fields.Many2one('res.partner', 'Nama Customer', index=True, readonly=True, states={'draft': [('readonly', False)]})
    pegawai_id = fields.Many2one('hr.employee', 'Nama Pegawai', index=True, readonly=True, states={'draft': [('readonly', False)]})

    detail_transaksi_ids = fields.One2many('supermarket.detail_transaksi', 'transaksi_id', string='ID Detail transaksi')

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    temp = fields.Integer('Temp')

    # Ambil jumlah poin dari customer
    poin = fields.Integer('Poin', compute="_compute_poin", store=True, default=0)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('customer_id', 'poin')
    def _compute_poin(self):
        for _transaksi in self:
            val = {
                'poin': self.customer_id.poin,
            }
            _transaksi.update(val)

    @api.depends('detail_transaksi_ids.jumlah_barang')
    def _compute_total_barang(self):
        for _transaksi in self:
            val = {
                'total_barang': 0,
            }
            for rec in _transaksi.detail_transaksi_ids:
                val['total_barang'] += rec.jumlah_barang
            _transaksi.update(val)

    @api.depends('total_transaksi')
    def _compute_poin_baru(self):
        for _transaksi in self:
            val = {
                'poin_baru': 0,
                'temp': 0,
            }
            for rec in _transaksi:
                if rec.penggunaan_poin == 'tidak':
                    val['poin_baru'] += (rec.total_transaksi * 0.01)
                else:
                    val['poin_baru'] += (rec.total_transaksi * 0.01)
                    val['temp'] = val['poin_baru']
                    val['poin_baru'] = 0
            _transaksi.update(val)

    @api.depends('detail_transaksi_ids.total_harga_barang', 'penggunaan_poin', 'temp')
    def _compute_total_transaksi(self):
        for _transaksi in self:
            val = {
                'total_transaksi': 0,
                'temp': _transaksi.temp,
            }
            for cek in _transaksi:
                if cek.penggunaan_poin == 'tidak':
                    for rec in cek.detail_transaksi_ids:
                        val['total_transaksi'] += rec.total_harga_barang
                    _transaksi.update(val)

                else:
                    for rec in cek.detail_transaksi_ids:
                        val['total_transaksi'] += rec.total_harga_barang - cek.temp
                    _transaksi.update(val)

    @api.depends('detail_transaksi_ids.jumlah_barang', 'detail_transaksi_ids.harga_barang', 'detail_transaksi_ids.diskon_barang', 'temp')
    def _compute_hemat(self):
        for _transaksi in self:
            val = {
                'hemat': 0,
            }
            for hitung in _transaksi:
                for rec in _transaksi.detail_transaksi_ids:
                    val['hemat'] += (rec.jumlah_barang * rec.harga_barang * rec.diskon_barang / 100) + hitung.temp
                _transaksi.update(val)

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "supermarket.transaksi")])
            if not seq:
                raise UserError(_("supermarket.transaksi sequence not found, please create supermarket.transaksi sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id()
            return super(_transaksi, self).create(vals_list)

    def action_wiz_supermarket(self):
        return{
            'type': 'ir.actions.act_window',
            'name': _('Wizard Supermarket Transaksi'),
            'res_model': 'wiz.supermarket.transaksi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    class transaksi_lines(models.Model):
        _name = 'supermarket.transaksi.lines'
        _description = 'class untuk menyimpan data supermarket suatu transaksi'

        transaksi_id = fields.Many2one('supermarket.transaksi', string='Kelas', ondelete="cascade")
        barang_id = fields.Many2one('supermarket.barang', string='Barang', ondelete="cascade")
        jumlah_barang = fields.Integer('Jumlah Barang')
        # _sql_constraints = [('name_unik', 'unique(kelas_id, mhs_id)', _('The student is already exist!'))]

