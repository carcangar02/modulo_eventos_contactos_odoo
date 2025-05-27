from odoo import models, fields, api

class PartnerTutor(models.Model):
    _inherit = "res.partner"

    tutorized_ids = fields.One2many('tutorized', 'tutor_id', string="Tutorizados de este contacto")
    is_tutor = fields.Boolean(compute='_compute_is_tutor', store=True)

    @api.depends('tutorized_ids')
    def _compute_is_tutor(self):
        for partner in self:
            partner.is_tutor = bool(partner.tutorized_ids)
    