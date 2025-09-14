import unittest, os, sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from py.Events import EventDispatcher
from py.Model.CheckLists import CheckList

class CheckListTest(unittest.TestCase):

    def setUp(self):
        self.dispatcher = EventDispatcher()

    def test_should_track_lifetime(self):
        foo = CheckList(self.dispatcher, "Foo")
        bar = foo.add("bar")
        baz = foo.add("baz")
        
        self.assertFalse(foo.areAllCheckChecked())
        self.assertFalse(foo.isDoing())
        self.assertFalse(foo.isDone())
        
        bar.check()
        self.assertFalse(foo.areAllCheckChecked())
        self.assertTrue(foo.isDoing())
        self.assertFalse(foo.isDone())
        
        baz.check()
        self.assertTrue(foo.areAllCheckChecked())
        self.assertFalse(foo.isDoing())
        self.assertTrue(foo.isDone())
        
        bar.uncheck()
        self.assertFalse(foo.areAllCheckChecked())
        self.assertTrue(foo.isDoing())
        self.assertFalse(foo.isDone())
        
    def test_should_be_cancellable(self):
        foo = CheckList(self.dispatcher, "Foo")
        bar = foo.add("bar")
        
        self.assertFalse(foo.isCanceled())
        self.assertFalse(foo.isFinished())
        
        foo.cancel()
        self.assertTrue(foo.isCanceled())
        self.assertTrue(foo.isFinished())
        
    
        
if __name__ == '__main__':
    unittest.main()