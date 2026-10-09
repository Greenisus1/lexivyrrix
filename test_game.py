import unittest
from lexivyrrix import Game,score,WORDS
class Tests(unittest.TestCase):
 def test_duplicate(self):self.assertEqual(score('apple','allee'),[2,1,0,0,2])
 def test_no_extra_yellow(self):self.assertEqual(score('civic','vivid'),[0,2,2,2,0])
 def test_win(self):
  g=Game('apple');g.submit('apple');self.assertTrue(g.won);self.assertTrue(g.over)
 def test_loss(self):
  g=Game('apple')
  for _ in range(6):g.submit('bread')
  self.assertTrue(g.over);self.assertFalse(g.won);self.assertEqual(len(g.guesses),6)
 def test_reject(self):
  g=Game('apple');g.submit('ab');g.submit('zzzzz');self.assertEqual(g.guesses,[])
 def test_keyboard_best(self):
  g=Game('apple');g.submit('apple');self.assertEqual(g.keyboard['p'],2)
 def test_wordlist(self):self.assertEqual(len(WORDS),len(set(WORDS)));self.assertGreater(len(WORDS),300)
 def test_bounds(self):
  with self.assertRaises(ValueError):score('abc','abc')
 def test_uppercase(self):g=Game('apple');g.submit('APPLE');self.assertTrue(g.won)
 def test_limit(self):
  g=Game('apple')
  for _ in range(7):g.submit('bread')
  self.assertEqual(len(g.guesses),6)
