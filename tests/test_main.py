import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from project import models, main
import project.schemas as schemas
from project.crud import (
    create_user,
    create_word,
    get_word,
    update_word,
    delete_word,
    get_all_words_for_user,
    search_words,
)


class TestGetOrCreateDbUser(unittest.TestCase):
    def test_get_or_create_existing_user(self):
        db = MagicMock(spec=Session)
        user_sud = "existing_user"
        mock_user = models.User(user_id=user_sud)

        db.query.return_value.filter_by.return_value.first.return_value = mock_user

        user = create_user(db, user_sud)

        self.assertEqual(user, mock_user)
        db.add.assert_not_called()
        db.commit.assert_not_called()
        db.refresh.assert_not_called()

    def test_get_or_create_new_user(self):
        db = MagicMock(spec=Session)
        user_sud = "new_user"

        db.query.return_value.filter_by.return_value.first.return_value = None

        user = create_user(db, user_sud)

        self.assertEqual(user.user_id, user_sud)
        db.add.assert_called_once_with(user)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(user)



if __name__ == "__main__":
    unittest.main()
