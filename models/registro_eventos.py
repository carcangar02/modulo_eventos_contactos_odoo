from odoo import models, fields, api

class EventRegistrationInherit(models.Model):
    _inherit = 'event.registration'

    partner_id = fields.Many2one('res.partner', string="Partner", help="Enlace con el contacto existente")
    # vat es como se llama el campo donde se almacena el DNI





    @api.model
    def create(self, vals):
        
        #------------------------------------------TUTOR------------------------------------------------
        DNI = vals.get('company_name')
        if DNI:
            # Creamos una cache temporal en el entorno si no existe
            if not hasattr(self.env, 'created_tutors'):
                self.env.created_tutors = {}

            # Buscamos primero en la cache
            partner = self.env.created_tutors.get(DNI)
            if not partner:
                # Si no existe en la cache, buscamos en base de datos
                partner = self.env['res.partner'].search([('vat', '=', DNI)], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({
                        'name': vals.get('name'),
                        'vat': DNI,
                        'phone': vals.get('phone'),
                        'email': vals.get('email'),
                        'is_company': False              
                    })
                # Guardamos en la cache
                self.env.created_tutors[DNI] = partner

            vals['partner_id'] = partner.id
        #------------------------------------------TUTOR------------------------------------------------
       





        #------------------------------------------TUTORIZADO------------------------------------------------
        #Suponiendo en el orden de creacion que el nombre es el primero en ser creado y que el tutor solo tiene 4 preguntas 


        arrayRespuestas = []
        for answer in vals.get('registration_answer_ids', []):
            arrayRespuestas.append(answer[2])
        nombreTutorizado = arrayRespuestas[0]['value_text_box']
        notasInternasRaw = arrayRespuestas[1:-4]
        comment = ", ".join(item['value_text_box'] for item in notasInternasRaw)
        event_id = vals.get('event_id')
        tutor_id = vals.get('partner_id')
        anti_duplicate = self.env['tutorized'].search([('name', '=', nombreTutorizado), ('tutor_id', '=', tutor_id)])
        
        if not anti_duplicate:
            partner = self.env['tutorized'].create({
                'name': nombreTutorizado,
                'notas_internas': comment,
                'tutor_id': tutor_id,
                'event_id': [(4, event_id)],
            })
        else:
            anti_duplicate.write({
            'event_id': [(4, event_id)],
            'notas_internas': comment,
            })
    


        #-------------------------------------------TUTORIZADO------------------------------------------------
        return super(EventRegistrationInherit, self).create(vals)








