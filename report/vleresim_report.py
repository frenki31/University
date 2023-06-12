from odoo import fields, models, api


class UniversityReportVleresim(models.AbstractModel):
    _name = 'report.university.report_vleresim'
    _description = 'Description'

    @api.model
    def _get_report_values(self, docids, data=None):
        student_ids = data['student_ids']
        pike_min = data['pike_min']
        pike_max = data['pike_max']
        domain = [('status', '=', 'done')]
        if student_ids:
            domain += [('student_id', 'in', student_ids)]

        vleresim_object = self.env['university.vleresim'].search(domain)
        vleresim = []
        tot = 0
        for rec in vleresim_object.filtered(lambda r: pike_min <= r.total <= pike_max):
            vleresim.append({
                'student': rec.student_id.emer_mbiemer,
                'kredite': rec.kredite,
                'total': rec.total,
                'nota': rec.nota,
            })
            tot += rec.nota
        if not vleresim:
            return {}
        mesatarja = tot / len(vleresim)

        return {
            'docs': vleresim,
            'mesatarja': mesatarja,
        }
