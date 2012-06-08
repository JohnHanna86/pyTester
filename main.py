'''
Created on Jun 5, 2010

@author: johnnabil
'''
from VanillaSentenceAligner import VanillaSentenceAligner 
from HunalignSentenceAligner import HunalignSentenceAligner
from GMASentenceAligner import GMASentenceAligner
from CTKSentenceAligner import CTKSentenceAligner
from BilingualSentenceAligner import BilingualSentenceAligner


import unittest  


if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(VanillaSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(HunalignSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(GMASentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(CTKSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(BilingualSentenceAligner)
    unittest.TextTestRunner(verbosity=2).run(suite)
