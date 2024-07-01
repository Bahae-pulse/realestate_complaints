import random
from odoo import models, fields, api, _


class Complaint(models.Model):
    _name = 'realestate.complaint'
    _description = 'Tenant Complaint'

    name = fields.Char(string='Complaint Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    tenant_name = fields.Char(string='Tenant Name', required=True)
    tenant_email = fields.Char(string='Tenant Email', required=True)
    flat_address = fields.Char(string='Address', required=True)
    complaint_type = fields.Selection([
        ('question', 'Question'),
        ('electrical_issue', 'Electrical Issue'),
        ('heating_issue', 'Heating Issue'),
        ('other', 'Other'),
    ], string='Complaint Type', required=True)
    description = fields.Text(string='Description', required=True)
    stage_id = fields.Many2one('realestate.complaint.stage', string='Stage', default=lambda self: self._default_stage())
    stage_state = fields.Selection(related='stage_id.state', string='Stage State', store=True)
    
    action_plan = fields.Text(string='Action Plan')
    user_id = fields.Many2one('res.users', string='Assigned to')
    message_to_tenant = fields.Text(string='Message to Tenant', store=True)
    tag_ids = fields.Many2many('realestate.complaint.tag', string='Tags')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('realestate.complaint') or _('New')

        # Automatic assignment to a customer service representative
        user = self._get_available_user()
        vals['user_id'] = user.id if user else False

        complaint = super(Complaint, self).create(vals)
        complaint.tag_ids = [(6, 0, [self.env.ref('realestate_complaints.tag_new').id])]
        complaint.send_confirmation_email()
        return complaint

    @api.model
    def _get_available_user(self):
        # Fetch all active users who can be assigned complaints and belong to 'Customer Service' group
        customer_service_group = self.env.ref('realestate_complaints.group_customer_service_representative')
        users = self.env['res.users'].search([
            ('share', '=', False),
            ('active', '=', True),
            ('groups_id', 'in', customer_service_group.id)
        ])

        # If no users are found, return False
        if not users:
            return False

        # Use round-robin
        last_complaint = self.search([], order="create_date desc", limit=1)

        if last_complaint and last_complaint.user_id:
            last_user = last_complaint.user_id

            if last_user.id in users.ids:
                next_user_index = (users.ids.index(last_user.id) + 1) % len(users.ids)
                next_user = users[next_user_index]
                return next_user
            else:
                return random.choice(users)
        else:
            return random.choice(users)

    # Func to make the in_review status
    def action_review(self):
        for complaint in self:
            complaint.stage_id = self.env.ref('realestate_complaints.stage_in_review')
            complaint.tag_ids = self.env.ref('realestate_complaints.tag_waiting')

    # Func to make the in_progress status
    def action_progress(self):
        for complaint in self:
            complaint.stage_id = self.env.ref('realestate_complaints.stage_in_progress')
            complaint.tag_ids = self.env.ref('realestate_complaints.tag_progress')

    # Func to make the solved status
    def action_solve(self):
        for complaint in self:
            complaint.stage_id = self.env.ref('realestate_complaints.stage_solved')
            complaint.tag_ids = self.env.ref('realestate_complaints.tag_answered')

    # Func to make the dropped status
    def action_drop(self):
        for complaint in self:
            complaint.stage_id = self.env.ref('realestate_complaints.stage_dropped')
            complaint.tag_ids = self.env.ref('realestate_complaints.tag_wrong')

    # Func to send confirmation mail
    def send_confirmation_email(self):
        template = self.env.ref('realestate_complaints.mail_complaint_confirmation')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)

    # Func to send message mail to tenant
    def message_tenant_and_close(self):
        if self.complaint_type == 'question':
            # Customize the email content based on the message parameter
            email_body = f"Dear {self.tenant_name},\n\nThank you for your question. Here is the response regarding your complaint {self.name}:\n\n{self.message_to_tenant}"
            
            # Send email to tenant
            template = self.env.ref('realestate_complaints.message_complaint_answer')
            if template:
                template.write({
                    'body_html': email_body,
                })
                template.send_mail(self.id, force_send=True)

            # Update the complaint with the message and change stage to 'solved' and tag to 'answered'
            self.write({
                'message_to_tenant': self.message_to_tenant,
                'stage_id': self.env.ref('realestate_complaints.stage_solved'),
                'tag_ids' : self.env.ref('realestate_complaints.tag_answered')
            })

            # Display notification of sent success
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Mail sent successfully!'),
                    'type':'success',
                    'sticky': False,
                },
            }
            return notification

    @api.model
    def _default_stage(self):
        stage = self.env['realestate.complaint.stage'].search([], order='sequence', limit=1)
        return stage

    # Func to print the work order report
    def print_work_order(self):
        # Logic to trigger report generation
        report_action = self.env.ref('realestate_complaints.action_report_work_order').report_action(self)

        # Logic to Send email with template
        template_id = self.env.ref('realestate_complaints.mail_complaint_work_order').id
        complaint = self.env['realestate.complaint'].browse(self.ids)
        if template_id:
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(complaint.id, force_send=True)
            self.write({
                'stage_id': self.env.ref('realestate_complaints.stage_solved'),
                'tag_ids' : self.env.ref('realestate_complaints.tag_answered'),
            })

        return report_action

class ComplaintStage(models.Model):
    _name = 'realestate.complaint.stage'
    _description = 'Complaint Stage'

    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order stages.")
    state = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('dropped', 'Dropped'),
    ], string='State', default='new', required=True)


class RealEstateComplaintTag(models.Model):
    _name = 'realestate.complaint.tag'
    _description = 'Real Estate Complaint Tag'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')