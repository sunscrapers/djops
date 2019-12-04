from django.test import TestCase


class CommonViewsTestCase(TestCase):

    def test_get_admin_index_should_return_200(self):
        response = self.client.get("/admin/", follow=True)

        self.assertEqual(response.status_code, 200)
