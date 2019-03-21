from app import app
import unittest
import os

class FlaskTestCase(unittest.TestCase):
	
	# Ensure that flask was setup properly
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	# Ensure that the login page loads correctly
	def test_login_page_load(self):
		tester = app.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertIn(b'Please login', response.data)

	# Ensure login behaves correctly given correct credentials
	def test_correct_login(self):
		tester = app.test_client()
		response = tester.post(
			'/login',
			data=dict(username="admin", password="admin"),
			follow_redirects=True
		)
		self.assertIn(b'You were logged in!', response.data)

	# Ensure login behaves correctly given incorrect credentials
	def test_incorrect_login(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login',
			data=dict(username="wrong", password="wrong"),
			follow_redirects=True
		)
		self.assertIn(b'Invalid Credentials. Please try again.', response.data)

	# Ensure logout behaves correctly
	def test_logout(self):
		tester = app.test_client(self)
		response = tester.post(
			'/login',
			data=dict(username="admin", password="admin"),
			follow_redirects=True
		)
		response = tester.get('/logout', follow_redirects=True)
		self.assertIn(b'You were logged out.', response.data)

	# Ensure that the main page requres login
	def test_main_route_requires_login(self):
		tester = app.test_client(self)
		response = tester.get('/', follow_redirects=True)
		self.assertIn(b'You need to login first.', response.data)


	# Ensure that posts show up on main page
	def test_post_data_display(self):
		tester = app.test_client()
		response = tester.post(
			'/login',
			data=dict(username="admin", password="admin"),
			follow_redirects=True
		)
		self.assertIn(b'hholoszyc', response.data)


if __name__=='__main__':
	print(os.name)
	unittest.main()


