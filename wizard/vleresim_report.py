from odoo import fields, models, api


class VleresimReport(models.TransientModel):
    _name = 'vleresim.report'
    _description = 'Description'

    student_ids = fields.Many2many(comodel_name='university.student', string='Studentet')
    pike_min = fields.Integer(default=0, string='Piket minimale', required=True)
    pike_max = fields.Integer(default=100, string='Piket maksimale', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "student_ids": self.student_ids.ids,
            "pike_min": self.pike_min,
            "pike_max": self.pike_max,
        }
        return self.env.ref('University.action_report_vleresim').report_action(None, data=data)
