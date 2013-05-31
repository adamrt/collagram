import os
import unittest
from collagram import Collage, InvalidUserError, PrivateUserError


USER = 'adamrt'
USER_ID = '19226776'
BAD_USER = 'jfjfjfjfjfjfjfjfij'
PRIV_USER = '83howell83'
PRIV_USER_ID = '243978586'

TAG = 'vurbranch'
BAD_TAG = 'jjjjjjjjjjjjjjjjjjjj'

PATH_USERS = '/tmp/collagram/media/users/'
PATH_TAGS = '/tmp/collagram/media/tags/'


class TestCollage(unittest.TestCase):

    def setUp(self):
        self.user = Collage(username=USER, path_users=PATH_USERS)
        self.bad_user = Collage(username=BAD_USER, path_users=PATH_USERS)
        self.priv_user = Collage(username=PRIV_USER, path_users=PATH_USERS)

        self.tag = Collage(tag=TAG)
        self.bad_tag = Collage(tag=BAD_TAG)

        self.size = Collage(username=USER, columns=4, rows=4)

        self.user_path = Collage(username=USER, path_users=PATH_USERS)
        self.tag_path = Collage(tag=TAG, path_tags=PATH_TAGS)

    def test_attributes(self):
        self.assertRaises(AttributeError, Collage)
        self.assertRaises(AttributeError, Collage, username=USER, tag=TAG)
        self.assertRaises(Exception, Collage, token=None)


    def test_columns_and_rows(self):
        self.assertEqual(self.user.columns, 10)
        self.assertEqual(self.user.rows, 2)

        self.assertEqual(self.size.columns, 4)
        self.assertEqual(self.size.rows, 4)

    def test_name(self):
        self.assertEqual(self.user.name, '@' + USER)
        self.assertEqual(self.tag.name, '#' + TAG)

    def test_user_id(self):
        self.assertEqual(self.user.user_id, USER_ID)
        self.assertEqual(self.bad_user.user_id, None)
        self.assertEqual(self.priv_user.user_id, PRIV_USER_ID)
        self.assertEqual(self.tag.user_id, None)

    def test_media_json(self):
        self.assertEqual(len(self.user.media_json()), 20)
        self.assertEqual(self.bad_user.media_json(), None)
        self.assertRaises(PrivateUserError, self.priv_user.media_json)

    def test_filename(self):
        assert self.user.filename.endswith('users/' + USER + '.jpg')
        assert self.bad_user.filename.endswith('users/' + BAD_USER + '.jpg')
        assert self.priv_user.filename.endswith('users/' + PRIV_USER + '.jpg')
        self.assertEqual(self.user_path.filename, PATH_USERS + USER + '.jpg')

    def test_path(self):
        self.user_path.ensure_path()
        self.assertEqual(os.path.exists(PATH_USERS), True)
        self.tag_path.ensure_path()
        self.assertEqual(os.path.exists(PATH_TAGS), True)

    def test_generate(self):
        self.user.generate()
        self.assertEqual(os.path.exists(self.user.filename), True)
        self.assertRaises(PrivateUserError, self.priv_user.generate)
        self.assertRaises(InvalidUserError, self.bad_user.generate)

    def test_dimensions(self):
        self.assertEqual(self.user.width, 1500)
        self.assertEqual(self.user.height, 300)

if __name__ == '__main__':
    unittest.main()
