
import sys, os, logging, unittest
from os.path import dirname, abspath

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":

    loader = unittest.TestLoader()
    suite = loader.discover('test')
    unittest.TextTestRunner().run(suite)
    # unittest.main()