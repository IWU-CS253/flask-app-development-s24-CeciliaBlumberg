import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_deleting(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category',
        ), follow_redirects=True)
        rv = self.app.post('/delete',data=dict(
            id='1'), follow_redirects=True)
        assert b'&lt;Hello&gt;' not in rv.data
        assert b'<strong>HTML</strong> allowed here' not in rv.data
        assert b'A category' not in rv.data

    def test_edit(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category',
        ), follow_redirects=True)
        rv = self.app.post('/update_entry', data=dict(
            id='1',
            title='<Hello_Updated>',
            text='<strong>HTML UPDATED</strong> allowed here',
            category='A updated category'
        ), follow_redirects=True)
        assert b'&lt;Hello_Updated&gt;' in rv.data
        assert b'<strong>HTML UPDATED</strong> allowed here' in rv.data
        assert b'A updated category' in rv.data
        assert b'&lt;Hello&gt;' not in rv.data
        assert b'<strong>HTML</strong> allowed here' not in rv.data
        assert b'A category' not in rv.data

    def test_sorting(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category',
        ), follow_redirects=True)
        rv = self.app.post('/add', data=dict(
            title='<Hello2>',
            text='<strong>HTML2</strong> allowed here',
            category='A category2',
        ), follow_redirects=True)
        rv = self.app.post('/', data=dict(
            choice='A category2'
        ), follow_redirects=True)
        assert b'&lt;Hello2&gt;' in rv.data
        assert b'<strong>HTML2</strong> allowed here' in rv.data
        assert b'A category2' in rv.data
        assert b'&lt;Hello&gt;' not in rv.data
        assert b'<strong>HTML</strong> allowed here' not in rv.data

    def test_sorting_options(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category',
        ), follow_redirects=True)
        rv = self.app.post('/', data=dict(
            choice='A category3'
        ), follow_redirects=True)
        assert b'&lt;Hello&gt;' not in rv.data
        assert b'<strong>HTML</strong> allowed here' not in rv.data



if __name__ == '__main__':
    unittest.main()