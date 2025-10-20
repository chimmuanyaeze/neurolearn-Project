import unittest
from chat_manager import initialize_chat_state, start_new_chat, append_to_current_chat, get_current_chat

class TestChatManager(unittest.TestCase):
    def setUp(self):
        initialize_chat_state()

    def test_start_new_chat(self):
        start_new_chat()
        chat = get_current_chat()
        self.assertEqual(chat, [])

    def test_append_message(self):
        start_new_chat()
        append_to_current_chat("user", "text", "Test message")
        chat = get_current_chat()
        self.assertEqual(len(chat), 1)
        self.assertEqual(chat[0]["content"], "Test message")

if __name__ == "__main__":
    unittest.main()
