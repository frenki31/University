from odoo import fields, models, api
from odoo.exceptions import UserError


class UniversityVleresim(models.Model):
    _name = 'university.vleresim'
    _description = 'Description'
    _sql_constraints = [
        ('unique_student', 'unique(student_id)', 'Cdo student ka pasqyren personale te notave')]

    student_id = fields.Many2one(comodel_name='university.student', string='Studenti', required=True)
    total = fields.Float(string='Mesatarja', compute='_compute_total', store=True)
    vleresim_ids = fields.One2many(comodel_name='university.vleresim.kursi', inverse_name='vleresim_id',
                                   string='Vleresim')
    nota = fields.Float(string='Nota (/10)', compute='_compute_mesatarja', store=True)
    kredite = fields.Integer(string='Kredite')
    status = fields.Selection(string='Status', required=True, default='draft',
                              selection=[('draft', 'Draft'),
                                         ('done', 'Konfirmuar')])

    @api.depends('vleresim_ids')
    def _compute_total(self):
        for rec in self:
            vleresim_ids = rec.vleresim_ids
            count = len(vleresim_ids)
            if count > 0:
                rec.total = sum(vleresim_ids.mapped('total')) / count
            else:
                rec.total = 0.0

    @api.depends('vleresim_ids')
    def _compute_mesatarja(self):
        for rec in self:
            vleresim_ids = rec.vleresim_ids
            count = len(vleresim_ids)
            if count > 0:
                rec.nota = sum(vleresim_ids.mapped('nota')) / count
            else:
                rec.nota = 0

    @api.onchange('kredite', 'vleresim_ids')
    def _onchange_kredite(self):
        self.kredite = sum(self.vleresim_ids.mapped('kredite'))

    def konfirmo(self):
        if self.kredite != self.student_id.program_id.kredite_detyruara:
            raise UserError('Studenti nuk ka plotesuar kreditet e mjaftueshme per te kaluar')
        else:
            self.status = 'done'

    def draft(self):
        self.status = 'draft'

    def unlink(self):
        for rec in self:
            if rec.status != 'draft':
                raise UserError('Nuk mund te fshihet pasqyra e konfirmuar e notave!')
        return super(UniversityVleresim, self).unlink()


class UniversityVleresimKursi(models.Model):
    _name = 'university.vleresim.kursi'
    _description = 'Description'
    _sql_constraints = [
        ('unique_kurs_per_student', 'unique(kurs_id, vleresim_id)',
         'Nuk mund te vleresosh te njejtin kurs dy here per te njejtin student')]

    vleresim_id = fields.Many2one(comodel_name='university.vleresim', string='Vleresim')
    kurs_id = fields.Many2one(comodel_name='university.kurs', string='Kursi', required=True,
                              domain="[('id','in',kurs_ids)]")
    kredite = fields.Integer(string='Kredite')
    projekti = fields.Float(string='Projekti', required=True)
    provimi = fields.Float(string='Provimi', required=True)
    detyra = fields.Float(string='Detyra', required=True)
    total = fields.Float(string='Nota e plote', compute='_compute_total', store=True)
    nota = fields.Integer(string='Nota (/10)', compute='_compute_mesataren')
    kurs_ids = fields.Many2many(related='vleresim_id.student_id.program_id.kurs_ids', string='Mundesite')

    @api.onchange('kurs_id', 'nota')
    def _onchange_kredite(self):
        if self.nota != 4:
            self.kredite = self.kurs_id.kredite
        else:
            self.kredite = 0

    @api.depends('total')
    def _compute_mesataren(self):
        for rec in self:
            if rec.total > 90:
                rec.nota = 10
            elif rec.total <= 90 and rec.total > 80:
                rec.nota = 9
            elif rec.total <= 80 and rec.total > 70:
                rec.nota = 8
            elif rec.total <= 70 and rec.total > 60:
                rec.nota = 7
            elif rec.total <= 60 and rec.total > 50:
                rec.nota = 6
            elif rec.total <= 50 and rec.total >= 45:
                rec.nota = 5
            elif rec.total < 45:
                rec.nota = 4

    @api.depends('projekti', 'provimi', 'detyra')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.projekti + rec.detyra + rec.provimi

    @api.model
    def create(self, values):
        res = super(UniversityVleresimKursi, self).create(values)
        if res.projekti < 0 or res.provimi < 0 or res.detyra < 0 or res.total > 100:
            raise UserError('Piket nuk mund te jene negative dhe nuk i kalojne dot 100 pike ne total')
        return res

    def write(self, values):
        res = super(UniversityVleresimKursi, self).write(values)
        for rec in self:
            if rec.projekti < 0 or rec.provimi < 0 or rec.detyra < 0 or rec.total > 100:
                raise UserError('Piket nuk mund te jene negative dhe nuk i kalojne dot 100 pike ne total')
        return res

    def unlink(self):
        for rec in self:
            if rec.vleresim_id.status != 'draft':
                raise UserError('Nuk mund te fshihen vleresimet e notave te kursit qe jane konfirmuar!')
        return super(UniversityVleresimKursi, self).unlink()
