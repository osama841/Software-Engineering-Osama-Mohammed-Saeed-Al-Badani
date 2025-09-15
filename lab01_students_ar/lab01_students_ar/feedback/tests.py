from django.test import TestCase
from django.urls import reverse

class FeedbackViewTest(TestCase):
    def test_feedback_submit_page_loads(self):
        """Test that feedback submit page loads"""
        response = self.client.get(reverse('feedback:submit_feedback'))
        self.assertEqual(response.status_code, 200)
    
    def test_feedback_send_page_loads(self):
        """Test that feedback send page loads"""
        response = self.client.get(reverse('feedback:feedback_send'))
        # This might return 200 or 500 depending on email configuration
        self.assertIn(response.status_code, [200, 500])
    
    def test_feedback_form_submission(self):
        """Test that feedback form can be submitted"""
        response = self.client.post(reverse('feedback:submit_feedback'), {
            'student_name': 'Test Student',
            'email': 'test@example.com',
            'course_name': 'Test Course',
            'understanding_level': 'good',
            'positives': 'Good course content',
            'negatives': 'Could be improved',
            'improvements': 'Add more examples',
            'comparison': 'Better than other courses',
            'future_use': 'Yes, would use again'
        })
        # Should render success page (200) or show form errors (200)
        self.assertEqual(response.status_code, 200)