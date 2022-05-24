from odoo import models, fields, api, _
from odoo.exceptions import UserError
#_ untuk translate
class idea(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk berlatih ttg idea'
    _order = 'date desc'

    name = fields.Char('Name', size=64, required=True, index=True, readonly=True, default='new', states={})
    date = fields.Date('Date Voting', default=fields.Date.context_today) # ini jadi nama field / kolom dengan tipe data Date, parameter String ini akan jadi caption / label di form odoo
    # att pertama selalu String shg tdk perlu ditulis nama parameter-nya
    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('voted', 'Voted'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    vote = fields.Selection(
        [('yes', 'Yes'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('no', 'No'),
         ('abstain', 'Abstain')], 'State', required=True,
        readonly=True,
        states={'draft':[('readonly', False)]})
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'), ('active', '=', 'True')]")
    idea_date = fields.Date("Idea date", related='idea_id.date', store=True)
    def action_canceled(self):
        self.state = 'canceled'

    def action_voted(self):
        self.state = 'voted'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_("idea.voting sequence not found, please create idea.voting sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id(sequence_date=val['date'])
                # val['name'] = seq.next_by_id()
            return super(idea, self).create(vals_list)