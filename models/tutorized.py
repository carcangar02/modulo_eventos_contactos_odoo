from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date

class Tutorized(models.Model):
    _name = "tutorized"
    _description = "Menor de edad Tutorizado"
    
    name = fields.Char("Nombre", required=True)
    birth_date = fields.Date("Fecha de Nacimiento")
    actual_age = fields.Integer(string="Edad", compute='_compute_age', store=True)
    tutor_id = fields.Many2one('res.partner',  string="Tutor encargado del menor", domain=[('is_company', '=', False)])
    is_relative = fields.Boolean('¿Es hijo/a del tutor')
    medical_condition = fields.Char(string="Especificar si existe alguna condición médica / alergia o intolerancia / toma alguna medicina / dieta especial")
    notas_internas = fields.Text("Notas internas", help="Notas internas del menor, no visibles para el usuario")
    event_id = fields.Many2many('event.event', readonly= True, string="Evento al que pertenece")
    genre = fields.Selection([
        ('male', 'Hombre'),
        ('female', 'Mujer')
    ], string="Género")
    vaccine = fields.Char("¿Vacunas al día? (especificar)")
    school = fields.Char("Colegio")
    has_course = fields.Selection([
        ('1_pri', '1º Primaria'),
        ('2_pri', '2º Primaria'),
        ('3_pri', '3º Primaria'),
        ('4_pri', '4º Primaria'),
        ('5_pri', '5º Primaria'),
        ('6_pri', '6º Primaria'),
        ('1_eso', '1º ESO'),
        ('2_eso', '2º ESO'),
        ('3_eso', '3º ESO'),
        ('4_eso', '4º ESO'),
        ('otros', 'Otros'),
    ], string="Ha Cursado")
    english_level = fields.Selection([
        ('basic', 'Básico'),
        ('medium', 'Intermedio'),
        ('high', 'Alto'),
        ('bilingual', 'Bilingüe'),
        ('native', 'Nativo'),
        ('not_sure', 'No estoy seguro'),
    ], string="Nivel de Inglés")


    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.actual_age = relativedelta(today, record.birth_date).years
            else:
                record.actual_age = 0

    @api.constrains
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
