import unittest
from db import init_supabase

class TestDB(unittest.TestCase):
    def test_init_supabase(self):
        supabase = init_supabase(cache_buster="test")
        self.assertIsNotNone(supabase)

if __name__ == "__main__":
    unittest.main()
