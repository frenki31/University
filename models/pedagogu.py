from odoo import fields, models, api


class UniversityPedagog(models.Model):
    _name = 'university.pedagog'
    _description = 'Description'
    _rec_name = 'emer_mbiemer'

    emri = fields.Char(string="Emri", required=True)
    mbiemri = fields.Char(string="Mbiemri", required=True)
    ditelindja = fields.Date(string='Ditelindja')
    email = fields.Char(string='Email')
    departament_id = fields.Many2one(comodel_name='university.departament', string='Departament')
    status = fields.Selection(string='Status',
                              selection=[('in', 'I brendshem'),
                                         ('out', 'I jashtem')
                                         ])
    emer_mbiemer = fields.Char(string='Emeri i plote', compute='_compute_emri')

    @api.depends('emri', 'mbiemri')
    def _compute_emri(self):
        for rec in self:
            rec.emer_mbiemer = '%s %s' % (rec.emri, rec.mbiemri)