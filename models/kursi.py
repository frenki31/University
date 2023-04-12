from odoo import fields, models, api


class UniversityKurs(models.Model):
    _name = 'university.kurs'
    _description = 'Description'
    _rec_name = 'emertimi'

    emertimi = fields.Char(string='Emertimi')
    semester = fields.Selection(string='Semester',
                                selection=[('pranvere', 'Pranvere'), ('dimer', 'Dimer'),])
    kredite = fields.Integer(string='Kredite', required=True)
