from odoo import http
from odoo.http import request

class ComplaintController(http.Controller):

    # Define the logic for the website form
    @http.route(['/complaint/form'], type='http', auth="public", website=True)
    def complaint_form(self, **kwargs):
        return request.render("realestate_complaints.complaint_form_template")

    # Define the logic for the website success submit form
    @http.route(['/complaint/submit'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def complaint_submit(self, **post):
        complaint = request.env['realestate.complaint'].sudo().create({
            'tenant_name': post.get('tenant_name'),
            'tenant_email': post.get('tenant_email'),
            'flat_address': post.get('flat_address'),
            'complaint_type': post.get('complaint_type'),
            'description': post.get('description'),
        })
        return request.render("realestate_complaints.complaint_success_template", {'complaint': complaint})