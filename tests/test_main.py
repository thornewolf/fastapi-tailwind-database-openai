import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from project import models, main
import project.schemas as schemas
from project.crud import create_user


class TestGetOrCreateDbUser(unittest.TestCase):
    def test_get_or_create_existing_user(self):
        db = MagicMock(spec=Session)
        user_sub = "existing_user"
        mock_user = models.User(id=user_sub)

        db.query.return_value.filter_by.return_value.first.return_value = mock_user

        user = create_user(db, user_id=user_sub)

        self.assertEqual(user.id, mock_user.id)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    def test_get_or_create_new_user(self):
        db = MagicMock(spec=Session)
        user_sub = "new_user"

        db.query.return_value.filter_by.return_value.first.return_value = None

        user = create_user(db, user_id=user_sub)

        self.assertEqual(user.id, user_sub)
        db.add.assert_called_once_with(user)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(user)


if __name__ == "__main__":
    unittest.main()
