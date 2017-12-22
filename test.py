import unittest
import formatter


class TestFormatter(unittest.TestCase):
    comment: dict = {
        'created_at': '2017-12-22T12:00:14.061Z',
        'commenter': {
            'display_name': 'Zarlach'
        },
        'message': {
            'body': 'Hello world'
        }
    }

    def test_custom_format(self):
        expected: str = '<Zarlach> Hello world'
        output: str = formatter.custom_format('<{commenter[display_name]}> {message[body]}', self.comment)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
