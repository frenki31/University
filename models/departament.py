from odoo import fields, models, api


class UniversityDepartament(models.Model):
    _name = 'university.departament'
    _description = 'Description'
    _rec_name = 'departament'

    departament = fields.Char(string='Departamenti', required=True)
    drejtues_id = fields.Many2one(comodel_name='university.pedagog', string='Drejtues departamenti')
    pedagog_ids = fields.One2many(comodel_name='university.pedagog', inverse_name='departament_id',
                                  string='Pedagoget')
