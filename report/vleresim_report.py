from odoo import fields, models, api


class UniversityReportVleresim(models.AbstractModel):
    _name = 'report.university.report_vleresim'
    _description = 'Description'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('printoi')
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
            })
            tot += rec.total
        if not vleresim:
            print({})
            return {}
        mesatarja = tot / len(vleresim)

        print(data)
        return {
            'docs': vleresim,
            'mesatarja': mesatarja,
        }

        # if data['student_ids']:
        #     domain.append(('student_id', 'in', data['student_ids']))
        #     # studentet = self.env['university.vleresim'].browse(data['student_ids']).mapped("emer_mbiemer")
        #     # name = f'Studentet {", ".join(studentet)}'
        #
        # vleresim_obj = self.env['university.vleresim'].search(domain)
        # vleresim = []
        #
        # tot = 0
        # for rec in vleresim_obj:
        #     vleresim.append({
        #         'student': rec.student_id.emer_mbiemer,
        #         'kredite': rec.kredite,
        #         'total': rec.total,
        #     })
        #     tot += rec.total
        # mesatarja = tot / len(vleresim)
        #
        # print(vleresim)
