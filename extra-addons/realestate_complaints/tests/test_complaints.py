from odoo.tests.common import TransactionCase
from odoo import exceptions

class TestComplaint(TransactionCase):

    def setUp(self):
        super(TestComplaint, self).setUp()
        self.Complaint = self.env['realestate.complaint']
        self.Stage = self.env['realestate.complaint.stage']
        self.Tag = self.env['realestate.complaint.tag']
        self.User = self.env['res.users']
        self.company = self.env.user.company_id

        # Create stages
        self.stage_new = self.Stage.create({'name': 'New', 'sequence': 1, 'state': 'new'})
        self.stage_in_review = self.Stage.create({'name': 'In Review', 'sequence': 2, 'state': 'in_review'})
        self.stage_in_progress = self.Stage.create({'name': 'In Progress', 'sequence': 3, 'state': 'in_progress'})
        self.stage_solved = self.Stage.create({'name': 'Solved', 'sequence': 4, 'state': 'solved'})
        self.stage_dropped = self.Stage.create({'name': 'Dropped', 'sequence': 5, 'state': 'dropped'})

        # Create tags
        self.tag_answered = self.Tag.create({'name': 'Answered', 'color': 1})
        self.tag_wrong = self.Tag.create({'name': 'Wrong', 'color': 2})

    def test_create_complaint(self):
        complaint = self.Complaint.create({
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main Street',
            'complaint_type': 'question',
            'description': 'This is a test complaint.',
            'company_id': self.company.id,
        })
        self.assertEqual(complaint.name, 'New', "The complaint name should be 'New'")
        self.assertEqual(complaint.stage_id, self.stage_new, "The complaint should be in 'New' stage")

    def test_action_review(self):
        complaint = self.Complaint.create({
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main Street',
            'complaint_type': 'question',
            'description': 'This is a test complaint.',
            'company_id': self.company.id,
        })
        complaint.action_review()
        self.assertEqual(complaint.stage_id, self.stage_in_review, "The complaint should be in 'In Review' stage")

    def test_action_progress(self):
        complaint = self.Complaint.create({
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main Street',
            'complaint_type': 'question',
            'description': 'This is a test complaint.',
            'company_id': self.company.id,
        })
        complaint.action_progress()
        self.assertEqual(complaint.stage_id, self.stage_in_progress, "The complaint should be in 'In Progress' stage")

    def test_action_solve(self):
        complaint = self.Complaint.create({
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main Street',
            'complaint_type': 'question',
            'description': 'This is a test complaint.',
            'company_id': self.company.id,
        })
        complaint.action_solve()
        self.assertEqual(complaint.stage_id, self.stage_solved, "The complaint should be in 'Solved' stage")
        self.assertIn(self.tag_answered, complaint.tag_ids, "The complaint should have 'Answered' tag")

    def test_action_drop(self):
        complaint = self.Complaint.create({
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main Street',
            'complaint_type': 'question',
            'description': 'This is a test complaint.',
            'company_id': self.company.id,
        })
        complaint.action_drop()
        self.assertEqual(complaint.stage_id, self.stage_dropped, "The complaint should be in 'Dropped' stage")
        self.assertIn(self.tag_wrong, complaint.tag_ids, "The complaint should have 'Wrong' tag")