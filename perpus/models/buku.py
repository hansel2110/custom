from odoo import models, fields, api, _

class _buku(models.Model):
    # Atrribute dari class
    _name = 'perpus.buku'
    _description = 'Class Buku Perpustakaan'

    id_buku = fields.Char('ID Buku', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    name = fields.Char('Judul', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    jumlah_buku = fields.Integer('Jumlah Buku', required=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga', required=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    tahun = fields.Char('Tahun', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_unik', 'unique(id_buku)', _('ID Buku Must be unique!')),
                        ('cek_harga', 'CHECK (harga>0)', 'Harga Must be Greater than 0!')]
    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

