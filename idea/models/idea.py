from odoo import models, fields, api, _
from odoo.exceptions import UserError
#_ untuk translate
class idea(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.idea' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    _description = 'class untuk berlatih ttg idea'
    _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    _order = 'date desc'
    #id = fields.Integer() ini otomatis ada di odoo, akan jadi PK

    # membuat attribute field. Field ini punya common parameter

    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new', states={})
    date = fields.Date('Date Release', default=fields.Date.context_today) # ini jadi nama field / kolom dengan tipe data Date, parameter String ini akan jadi caption / label di form odoo
    # att pertama selalu String shg tdk perlu ditulis nama parameter-nya
    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  #tuple di dalam list, nama field harus state spy bisa diakses oleh states

    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')

    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)

    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')
    # sponsor_ids = fields.Many2many('res.partner', 'idea_sponsor_rel', 'idea_id', 'sponsor_id','Sponsors')
    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})

    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")

    def _compute_vote(self):
        for idea in self:
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0
            }
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
                if rec.vote == 'yes':
                    val["total_yes"] += 1
                elif rec.vote == 'no':
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1
            idea.update(val)

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_settodraft(self):
        self.state = 'draft'

    def action_tes(self):
        # self.env['library.book']
        print(self.env.user.name)
        print(self.env.company.name)
        a=self.env["res.partner"].search([('name', 'ilike', 'Gemini')])
        for rec in a:
            print(rec.name)
        a = self.env["res.partner"].search([], limit=2)

        #contoh context
        print(self.env.context.get('lang'))
        t = self.env.context.copy()
        t["keterangan"] = 'Ideku'
        self.with_context(t).action_done()
        b=self.env["perpus.peminjaman"]
        b.with_context(t).tes_bookrent()

        # contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        for data in res:
            print(data[0])

        # contoh browse
        query = "select * from res_partner limit 3"
        self.env.cr.execute(query)
        res = self.env['res.partner'].browse([row[0] for row in self.env.cr.fetchall()])
        for rec in res:
            print(rec.name)