{
    'name': 'modulo_contacts_newpa',
    'version': '1.0',
    'summary': 'Organización de tutores y tutorizados en el módulo de contactos',
    'author': 'NorthDelta',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['base', 'event', 'website_event'],
    'data': [
        'views/tutorized_views.xml',
        'views/res_partner_views.xml',
        'security/ir_model_access.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
