import unittest
from chat_storage import save_chat, get_chat_by_id, delete_chat_by_id

class TestChatStorage(unittest.TestCase):
    def setUp(self):
        """Set up a test user and dummy chat before each test."""
        self.user_id = "709d304c-bac8-45b4-9810-790fb741ffa9"  # Replace with a real test user UUID if needed
        self.title = "UnitTest Chat"
        self.messages = [{"role": "user", "type": "text", "content": "Hello"}]

    def test_save_and_get_chat(self):
        chat_id = save_chat(self.user_id, self.title, self.messages)
        chat = get_chat_by_id(chat_id)
        self.assertIsNotNone(chat)
        self.assertEqual(chat["title"], self.title)

    def test_delete_chat(self):
        chat_id = save_chat(self.user_id, "Chat to delete", self.messages)
        delete_chat_by_id(chat_id)
        chat = get_chat_by_id(chat_id)
        self.assertIsNone(chat)

if __name__ == "__main__":
    unittest.main()
