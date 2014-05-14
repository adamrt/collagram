import os
import unittest
from collagram import Collage, InvalidUserError, PrivateUserError


USER = 'adamrt'
USER_ID = '19226776'
INVALID_USER = 'jfjfjfjfjfjfjfjfij'
PRIVATE_USER = '83howell83'
PRIVATE_USER_ID = '243978586'

TAG = 'vurbranch'
INVALID_TAG = 'jjjjjjjjjjjjjjjjjjjj'

PATH_USERS = '/tmp/collagram/media/users/'
PATH_TAGS = '/tmp/collagram/media/tags/'


class TestCollage(unittest.TestCase):

    def setUp(self):
        self.user = Collage(username=USER, path_users=PATH_USERS)
        self.invalid_user = Collage(username=INVALID_USER, path_users=PATH_USERS)
        self.private_user = Collage(username=PRIVATE_USER, path_users=PATH_USERS)

        self.tag = Collage(tag=TAG)
        self.invalid_tag = Collage(tag=INVALID_TAG)

        self.user_path = Collage(username=USER, path_users=PATH_USERS)
        self.tag_path = Collage(tag=TAG, path_tags=PATH_TAGS)

    def test_init(self):
        self.assertRaises(AttributeError, Collage)
        self.assertRaises(AttributeError, Collage, username=USER, tag=TAG)
        self.assertRaises(Exception, Collage, token=None)

    def test_dimensions(self):
        c = Collage(username=USER)
        self.assertEqual(c.dimension, 150)
        self.assertEqual(c.height, 300)
        self.assertEqual(c.width, 1500)

        c = Collage(username=USER, columns=4, rows=4, size="low_resolution")
        self.assertEqual(c.dimension, 306)
        self.assertEqual(c.height, 1224)
        self.assertEqual(c.width, 1224)

    def test_name(self):
        self.assertEqual(self.user.name, '@' + USER)
        self.assertEqual(self.tag.name, '#' + TAG)

    def test_user_id(self):
        self.assertEqual(self.user.user_id, USER_ID)
        self.assertEqual(self.invalid_user.user_id, None)
        self.assertEqual(self.private_user.user_id, PRIVATE_USER_ID)
        self.assertEqual(self.tag.user_id, None)

    def test_validate(self):
        self.assertRaises(InvalidUserError, self.invalid_user.validate)

    def test_media_json(self):
        self.assertEqual(len(self.user.media_json()), 20)
        self.assertEqual(self.invalid_user.media_json(), None)
        self.assertRaises(PrivateUserError, self.private_user.media_json)

    def test_filename(self):
        custom = Collage(username=USER, columns=4, rows=4)
        large = Collage(username=USER, path_users=PATH_USERS, size='standard_resolution')
        invalid = Collage(username=USER, path_users=PATH_USERS, size='invalid_size')

        assert self.user.filename.endswith('%s_thumbnail_10x2.jpg' % USER)
        assert custom.filename.endswith('%s_thumbnail_4x4.jpg' % USER)
        assert invalid.filename.endswith('%s_thumbnail_10x2.jpg' % USER)
        assert large.filename.endswith('%s_standard_resolution_10x2.jpg' % USER)

        self.assertEqual(self.user_path.filename, "%s%s_thumbnail_10x2.jpg" % (PATH_USERS, USER))

    def test_path(self):
        self.user_path.ensure_path()
        self.assertEqual(os.path.exists(PATH_USERS), True)
        self.tag_path.ensure_path()
        self.assertEqual(os.path.exists(PATH_TAGS), True)

    def test_generate(self):
        self.user.generate()
        self.assertEqual(os.path.exists(self.user.filename), True)
        self.tag.generate()
        self.assertEqual(os.path.exists(self.tag.filename), True)

        self.assertRaises(PrivateUserError, self.private_user.generate)
        self.assertRaises(InvalidUserError, self.invalid_user.generate)


if __name__ == '__main__':
    unittest.main()
