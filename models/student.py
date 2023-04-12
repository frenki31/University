from odoo import fields, models, api


class UniversityStudent(models.Model):
    _name = 'university.student'
    _description = 'Description'
    _rec_name = 'emer_mbiemer'

    emri = fields.Char(string="Emri", required=True)
    mbiemri = fields.Char(string="Mbiemri", required=True)
    ditelindja = fields.Date(string='Ditelindja')
    email = fields.Char(string='Email')
    numri = fields.Char(string='Numri i telefonit')
    program_id = fields.Many2one(comodel_name='university.program', string='Programi i studimit')
    viti_regjistrimit = fields.Selection(related='program_id.viti', string='Viti i regjistrimit')
    emer_mbiemer = fields.Char(string='Emeri i plote', compute='_compute_emri')

    @api.depends('emri', 'mbiemri')
    def _compute_emri(self):
        for rec in self:
            rec.emer_mbiemer = '%s %s' % (rec.emri, rec.mbiemri)

