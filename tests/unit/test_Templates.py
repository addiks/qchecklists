import unittest, os, sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from py.Events import EventDispatcher
from py.Model.Templates import CheckListTemplate

class SomeCoolTest(unittest.TestCase):

    def setUp(self):
        self.dispatcher = EventDispatcher()

    def test_should_create_checklists(self):
        t = CheckListTemplate(self.dispatcher, "Foo")
        
        t.add("bar")
        t.add("baz")
        
        foo1 = t.createChecklist()
        foo2 = t.createChecklist()
    
        self.assertEqual(2, len(foo1.entries()))
        self.assertEqual(2, len(foo2.entries()))
    
        self.assertTrue(foo1.get("bar") != None)
        self.assertTrue(foo1.get("baz") != None)
        self.assertTrue(foo2.get("bar") != None)
        self.assertTrue(foo2.get("baz") != None)
        
if __name__ == '__main__':
    unittest.main()