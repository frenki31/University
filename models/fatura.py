from odoo import fields, models, api
from odoo.exceptions import UserError


class UniversityFatura(models.Model):
    _name = 'university.fatura'
    _description = 'Description'
    _sql_constraints = [
        ('unique_fature_viti', 'unique(student_id, viti)', 'Cdo student ka faturen perkatese')
    ]

    nr_fature = fields.Integer(string='Numri i fatures')
    student_id = fields.Many2one(comodel_name='university.student', string='Studenti', required=True)
    tarifa = fields.Integer(related='student_id.program_id.tarifa', string='Tarifa')
    bursa = fields.Float(string='Bursa (%)')
    pagesa = fields.Float(string='Tarifa pas burses', compute='_compute_to_be_paid', store=True)
    viti = fields.Selection(
        [(str(year) + '-' + str(year + 1), str(year) + '-' + str(year + 1)) for year in range(2020, fields.datetime.now().year + 20)],
        string='Viti', default='%d-%d' % (fields.datetime.now().year, fields.datetime.now().year + 1), required=True)
    status = fields.Selection(string='Status', default='draft',
                              selection=[('draft', 'Papaguar'), ('done', 'Paguar')])

    @api.depends('tarifa','bursa')
    def _compute_to_be_paid(self):
        for rec in self:
            rec.pagesa = rec.tarifa - rec.tarifa * (rec.bursa/100)

    @api.onchange('tarifa', 'student_id')
    def _onchange_tarifa(self):
        self.tarifa = self.student_id.program_id.tarifa

    def unlink(self):
        raise UserError('Nuk mund te fshihen faturat!')
        return super(UniversityFatura, self).unlink()