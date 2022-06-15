from odoo import models, fields, api, _

class Employee(models.Model):

    _inherit = "hr.employee"
    # poin = fields.Integer(string='Poin', store=True)
    tgl_masuk = fields.Date('Tanggal Masuk', default=fields.Date.context_today)