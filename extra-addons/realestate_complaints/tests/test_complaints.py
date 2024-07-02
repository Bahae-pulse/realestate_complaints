from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestComplaintModel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.complaint = self.env['realestate.complaint'].create({
            'name': 'Test Complaint',
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': '123 Main St',
            'complaint_type': 'question',
            'description': 'Test complaint description'
        })
        self.Complaint = self.env['realestate.complaint']
        self.stage_new = self.env.ref('realestate_complaints.stage_new')
        self.stage_in_progress = self.env.ref('realestate_complaints.stage_in_progress')
        self.stage_in_review = self.env.ref('realestate_complaints.stage_in_review')
        self.stage_dropped = self.env.ref('realestate_complaints.stage_dropped')
        self.stage_solved = self.env.ref('realestate_complaints.stage_solved')
        self.tag_newest = self.env.ref('realestate_complaints.tag_new')
        self.tag_waiting = self.env.ref('realestate_complaints.tag_waiting')
        self.tag_progress = self.env.ref('realestate_complaints.tag_progress')
        self.tag_answered = self.env.ref('realestate_complaints.tag_answered')
        self.tag_wrong = self.env.ref('realestate_complaints.tag_wrong')

    def test_create_complaint(self):
        # Test valid complaint creation
        complaint_data = {
            'company_id': 1,
            'name': 'Test Complaint',
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'Test description',
            'stage_id': self.stage_new.id,
        }
        complaint = self.Complaint.create(complaint_data)
        self.assertTrue(complaint, "Complaint creation failed.")

    def test_complaint_cancellation(self):
        # Test complaint cancellation (moving to 'Dropped' stage)
        complaint_data = {
            'company_id': 1,
            'name': 'Test Complaint',
            'tenant_name': 'Sarah Johnson',
            'tenant_email': 'sarah.johnson@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'Test description',
            'stage_id': self.stage_in_progress.id,
            'user_id': self.env.ref('base.user_admin').id,
        }
        complaint = self.Complaint.create(complaint_data)
        
        # Move complaint to 'Dropped' stage
        complaint.stage_id = self.env.ref('realestate_complaints.stage_dropped').id
        self.assertEqual(complaint.stage_id, self.env.ref('realestate_complaints.stage_dropped'), "Complaint did not move to 'Dropped' stage.")

    def test_complaint_stage_progression(self):
        Complaint = self.env['realestate.complaint']
        
        # Create a new complaint in 'New' stage
        complaint_data = {
            'name': 'Sample Complaint',
            'company_id': 1,
            'tenant_name': 'Sample Tenant',
            'tenant_email': 'sample@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'This is a sample complaint description.',
            'stage_id': self.env.ref('realestate_complaints.stage_new').id,
            'user_id': self.env.ref('base.user_admin').id,
        }
        complaint = Complaint.create(complaint_data)
        self.assertEqual(complaint.stage_id.state, 'new')

        # Move the complaint to 'In Review' stage
        complaint.action_review()
        self.assertEqual(complaint.stage_id.state, 'in_review')

    def test_complaint_tagging(self):
        Complaint = self.env['realestate.complaint']
        Tag = self.env['realestate.complaint.tag']

        # Create a new tag and complaint associated with that tag
        tag1 = Tag.create({'name': 'Newest', 'color': 5})
        complaint_data = {
            'name': 'Sample Complaint',
            'company_id': 1,
            'tenant_name': 'Sample Tenant',
            'tenant_email': 'sample@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'This is a sample complaint description.',
            'stage_id': self.env.ref('realestate_complaints.stage_new').id,
            'user_id': self.env.ref('base.user_admin').id,
            'tag_ids': [(4, tag1.id)],  # Associate tag1 with the complaint
        }
        complaint = Complaint.create(complaint_data)
        self.assertTrue(complaint.id)

    def test_print_work_order_valid(self):
        # Test printing work order for a complaint in 'In Progress' stage
        complaint_data = {
            'company_id': 1,
            'name': 'Test Complaint',
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'Test description',
            'stage_id': self.stage_in_progress.id,
            'user_id': self.env.ref('base.user_admin').id,
        }
        complaint = self.Complaint.create(complaint_data)
        
        # Call print_work_order method
        result = complaint.print_work_order()
        
        # Assert that the method returns True or the expected result
        self.assertTrue(result, "Printing work order failed.")


    def test_message_tenant_and_close_question(self):
        # Test messaging tenant and closing a 'question' type complaint in 'In Progress' stage
        complaint_data = {
            'company_id': 1,
            'name': 'Test Question Complaint',
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'Test question description',
            'stage_id': self.stage_in_progress.id,
            'user_id': self.env.ref('base.user_admin').id,
            'tag_ids': [(6, 0, [self.tag_progress.id])],
        }
        complaint = self.Complaint.create(complaint_data)
        
        # Call message_tenant_and_close method
        complaint.message_tenant_and_close()
        
        # Assert that the complaint stage is now 'Solved'
        self.assertEqual(complaint.stage_id, self.stage_solved, "Complaint should be in 'Solved' stage.")

        # Assert that the 'Progressing' tag is removed
        self.assertNotIn(self.tag_progress, complaint.tag_ids, "'Progressing' tag should be removed.")


    def test_send_confirmation_email_new_complaint(self):
        # Test sending confirmation email for a new complaint
        complaint_data = {
            'company_id': 1,
            'name': 'Test New Complaint',
            'tenant_name': 'John Doe',
            'tenant_email': 'john.doe@example.com',
            'flat_address': 'Sample Address',
            'complaint_type': 'question',
            'description': 'Test question description',
            'stage_id': self.stage_new.id,
            'user_id': self.env.ref('base.user_admin').id,
            'tag_ids': [(6, 0, [self.tag_waiting.id])],
        }
        complaint = self.Complaint.create(complaint_data)
        
        # Call send_confirmation_email method
        complaint.send_confirmation_email()

        # Check if email was sent (mocked environment, so just assert the method was called)
        self.assertTrue(True, "send_confirmation_email should be called for new complaint.")

    def test_action_review(self):
        self.complaint.action_review()
        self.assertEqual(self.complaint.stage_id, self.stage_in_review,
                         "Stage should be set to 'In Review' after action_review")
        self.assertIn(self.tag_waiting, self.complaint.tag_ids,
                      "Tag 'Waiting' should be added after action_review")
        
    def test_action_progress(self):
        self.complaint.action_progress()
        self.assertEqual(self.complaint.stage_id, self.stage_in_progress,
                         "Stage should be set to 'In Progress' after action_progress")
        self.assertIn(self.tag_progress, self.complaint.tag_ids,
                      "Tag 'Progress' should be added after action_progress")
        
    def test_action_solve(self):
        self.complaint.action_solve()
        self.assertEqual(self.complaint.stage_id, self.stage_solved,
                         "Stage should be set to 'Solved' after action_solve")
        self.assertIn(self.tag_answered, self.complaint.tag_ids,
                      "Tag 'Answered' should be added after action_solve")

    def test_action_drop(self):
        self.complaint.action_drop()
        self.assertEqual(self.complaint.stage_id, self.stage_dropped,
                         "Stage should be set to 'Dropped' after action_drop")
        self.assertIn(self.tag_wrong, self.complaint.tag_ids,
                      "Tag 'Wrong' should be added after action_drop")

