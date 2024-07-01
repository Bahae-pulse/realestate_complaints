###################################################################################
#
#    Odoo Developer Test Case 2024 
#    Bloopark 

###################################################################################

{
    'name': 'RealEstate Complaints Management',
    'version': '1.0',
    'summary': 'Manage tenant complaints for RealEstateX',
    'license': 'LGPL-3',
    'author': 'Bahaeddine',
    
    'depends': ['base', 'mail', 'website', 'l10n_din5008'],

    'data': [

        'data/complaint_sequence.xml',
        'data/mail_template_data.xml',
        'data/complaint_stage_data.xml',
        'data/complaint_tags_data.xml',
        'data/data.xml',

        'security/ir.model.access.csv',

        'views/complaint_views.xml',
        'views/complaint_forms.xml',
        
        'reports/work_order_template.xml',
        'reports/work_order_report.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}