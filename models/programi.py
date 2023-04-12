from odoo import fields, models, api


class UniversityProgram(models.Model):
    _name = 'university.program'
    _description = 'Description'
    _rec_name = 'programi'

    emertimi = fields.Char(string="Programi", required=True)
    kurs_ids = fields.Many2many(comodel_name='university.kurs', string='Kurset', required=True)
    tarifa = fields.Integer(string='Tarifa', required=True)
    kredite_detyruara = fields.Integer(string='Kredite te detyruara', required=True)
    viti = fields.Selection(
        [(str(year)+'-'+str(year+1), str(year)+'-'+str(year+1)) for year in range(2010, fields.datetime.now().year + 5)],
        string='Viti', default='%d-%d' % (fields.datetime.now().year, fields.datetime.now().year + 1), required=True)
    student_ids = fields.One2many(comodel_name='university.student', inverse_name='program_id', string='Studentet')
    programi = fields.Char(string='Programi', compute='_compute_rec_name')

    @api.depends('emertimi', 'viti')
    def _compute_rec_name(self):
        for rec in self:
            rec.programi = '%s (%s)' % (rec.emertimi, rec.viti)

    @api.onchange('kredite_detyruara', 'kurs_ids')
    def _onchange_kredite(self):
        self.kredite_detyruara = sum(self.kurs_ids.mapped('kredite'))
