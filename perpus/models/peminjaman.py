from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _peminjaman(models.Model):
    # Atrribute dari class
    _name = 'perpus.peminjaman'
    _description = 'Class Peminjaman Perpustakaan'

    # name = fields.Char('ID Peminjaman', size=64, required=True, index=True, readonly=True,
    #                     states={'draft': [('readonly', False)]})
    name = fields.Char('ID Peminjaman', size=64, required=True, index=True, readonly=True, default='new',
                        states={})
    tgl_peminjaman = fields.Date('Tanggal Peminjaman', default=fields.Date.context_today) # ini jadi nama field / kolom dengan tipe data Date, parameter String ini akan jadi caption / label di form odoo
    biaya_total = fields.Integer('Biaya Total', compute="_compute_biaya_total", store=True, default=0)
    anggota_id = fields.Many2one('perpus.anggota', string='Nama Anggota', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    admin_id = fields.Many2one('perpus.admin', string='Nama Admin', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    detail_peminjaman_ids = fields.One2many('perpus.detail_peminjaman', 'peminjaman_id', string='ID Detail Peminjaman')
    jumlah_peminjaman = fields.Integer('Jumlah Peminjaman', compute="_compute_jumlah_peminjaman", store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('name_unique', 'unique(name)', _('ID Peminjaman Must be Unique'))]

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('detail_peminjaman_ids.biaya_peminjaman', 'detail_peminjaman_ids.biaya_denda', 'detail_peminjaman_ids.biaya_denda_telat')
    def _compute_biaya_total(self):
        for _peminjaman in self:
            val = {
                'biaya_total': 0,
            }
            for rec in _peminjaman.detail_peminjaman_ids:
                val['biaya_total'] += rec.biaya_peminjaman + rec.biaya_denda + rec.biaya_denda_telat
            _peminjaman.update(val)

    @api.depends('detail_peminjaman_ids.buku_id')
    def _compute_jumlah_peminjaman(self):
        for _peminjaman in self:
            val = {
                'jumlah_peminjaman': 0,
            }
            for rec in _peminjaman.detail_peminjaman_ids:
                val['jumlah_peminjaman'] += len(rec.buku_id)
            _peminjaman.update(val)

    def tes_bookrent(self):
        print("ini di bookrent")
        t = self.env.context.get("keterangan")
        print(t)

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "perpus.peminjaman")])
            if not seq:
                raise UserError(_("perpus.peminjaman sequence not found, please create perpus.peminjaman sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id()
            return super(_peminjaman, self).create(vals_list)