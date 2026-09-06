import tempfile, unittest
from pathlib import Path
from folder_size_story.__main__ import scan
class Tests(unittest.TestCase):
 def test_totals(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); (p/"a.txt").write_bytes(b"abc"); (p/"sub").mkdir(); (p/"sub"/"b.json").write_bytes(b"12345"); result=scan(p)
   self.assertEqual(result["total"],8); self.assertEqual(result["extensions"][0],(".json",5))
if __name__=="__main__": unittest.main()
