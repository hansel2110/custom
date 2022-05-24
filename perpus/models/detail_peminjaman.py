from odoo import models, fields, api, _

class _detail_peminjaman(models.Model):
    _name = 'perpus.detail_peminjaman'
    _description = 'Class Detail Peminjaman Perpustakaan'

    tgl_pengembalian = fields.Date('Tanggal Pengembalian', default=fields.Date.context_today) # ini jadi nama field / kolom dengan tipe data Date, parameter String ini akan jadi caption / label di form odoo
    biaya_peminjaman = fields.Integer(string="Biaya Peminjaman", compute="_compute_biaya_peminjaman", store=True)
    biaya_denda = fields.Integer('Biaya Denda', required=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    biaya_denda_telat = fields.Integer(string="Biaya Denda Telat", compute="_compute_biaya_denda_telat", store=True)
    keterangan = fields.Char('Keterangan', size=64, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    peminjaman_id = fields.Many2one('perpus.peminjaman', string='ID Peminjaman', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    buku_id = fields.Many2one('perpus.buku', string='Judul Buku', readonly=True, ondelete="cascade",
                            states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    tglpeminjaman = fields.Date('Tanggal Peminjaman', related='peminjaman_id.tgl_peminjaman')
    hargabuku = fields.Integer('Harga', related='buku_id.harga')
    durasi_peminjaman = fields.Integer(string="Durasi Peminjaman", compute="_compute_durasi_peminjaman", store=True)

    temp = fields.Integer('Temp')
    _sql_constraints = [('cek_tanggal', 'CHECK (durasi_peminjaman>0)', 'Tanggal Pengembalian harus setelah Tanggal Peminjaman!')]
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('tgl_pengembalian', 'tglpeminjaman')
    def _compute_durasi_peminjaman(self):
        for masuk in self:
            if masuk.tgl_pengembalian and masuk.tglpeminjaman:
                for rec in masuk:
                    durasi_peminjaman = int((rec.tgl_pengembalian - rec.tglpeminjaman).days)
                    rec.durasi_peminjaman = durasi_peminjaman

    @api.depends('hargabuku', 'durasi_peminjaman')
    def _compute_biaya_peminjaman(self):
        for _detail_peminjaman in self:
            val = {
                'biaya_peminjaman': 0,
            }
            for rec in _detail_peminjaman:
                val['biaya_peminjaman'] = rec.durasi_peminjaman * rec.hargabuku
            _detail_peminjaman.update(val)

    @api.depends('biaya_peminjaman', 'durasi_peminjaman')
    def _compute_biaya_denda_telat(self):
        for _detail_peminjaman in self:
            val = {
                'biaya_denda_telat': 0,
                'temp': 0,
            }
            for rec in _detail_peminjaman:
                if rec.durasi_peminjaman >= 5 and rec.durasi_peminjaman <= 10:
                    val['temp'] = rec.biaya_peminjaman * 0.1
                elif rec.durasi_peminjaman > 10:
                    val['temp'] = rec.biaya_peminjaman * 0.2
                val['biaya_denda_telat'] = val['temp']
            _detail_peminjaman.update(val)