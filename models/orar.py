from odoo import fields, models, api


class UniversityOrar(models.Model):
    _name = 'university.orar'
    _description = 'Description'

    kurs_id = fields.Many2one(comodel_name='university.kurs', string='Kurs', required=True,
                              domain="[('semester','=', semester)]")
    ora = fields.Selection(string='Ora', required=True,
                           selection=[('pare', '09:00-11:00'),
                                      ('dyte', '11:00-13:00'),
                                      ('trete', '13:00-15:00'),
                                      ])
    pedagog_id = fields.Many2one(comodel_name='university.pedagog', string='Pedagogu', required=True)
    orar_id = fields.Many2one(comodel_name='university.orari', string='Orari')
    semester = fields.Selection(string='Semester', related='orar_id.semester', store=True)


class UniversityOrari(models.Model):
    _name = 'university.orari'
    _description = 'Description'

    viti = fields.Selection(
        [(str(year) + '-' + str(year + 1), str(year) + '-' + str(year + 1)) for year in range(2020, fields.datetime.now().year + 20)],
        string='Viti', default='%d-%d' % (fields.datetime.now().year, fields.datetime.now().year + 1), required=True)
    semester = fields.Selection(string='Semester', required=True,
                                selection=[('pranvere', 'Pranvere'), ('dimer', 'Dimer')])
    dita = fields.Selection(string='Dita', required=True,
                            selection=[('hene', 'E hene'),
                                       ('marte', 'E marte'),
                                       ('merkure', 'E merkure'),
                                       ('enjte', 'E enjte'),
                                       ('premte', 'E premte'),
                                       ])
    orar_ids = fields.One2many(comodel_name='university.orar', inverse_name='orar_id', string='Oret')

