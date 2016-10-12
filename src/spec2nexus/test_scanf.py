'''
unittest: scanf module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import unittest
from spec2nexus.scanf import scanf


class Test(unittest.TestCase):


    def testName(self):
        fmt = "#X %gKohm (%gC)"
        
        degc_sp = 21.1
        t_sp = 273.15 + degc_sp
        cmd ="#X %gKohm (%gC)" % (degc_sp, t_sp)
        result = scanf(fmt, cmd)
        self.assertIsNot(None, result)
        a, b = result
        self.assertEqual(degc_sp, a)
        self.assertEqual(t_sp, b)
        
        degc_sp = 20
        t_sp = 273.15 + degc_sp
        cmd ="#X %gKohm (%gC)" % (degc_sp, t_sp)
        result = scanf(fmt, cmd)
        self.assertIsNot(None, result, 'could not parse: ' + cmd)
        a, b = scanf(fmt, cmd)
        self.assertEqual(degc_sp, a)
        self.assertEqual(t_sp, b)
        
        self.assertEqual((123.456e-1,), scanf('%g', '123.456e-1'))
        self.assertEqual((123.456,), scanf('%f', '123.456e-1'))
        self.assertEqual((20,), scanf('%g', '20'))
        self.assertEqual((0,), scanf('%g', '0.'))
        self.assertEqual((0,), scanf('%g', '.0'))
        self.assertEqual((0,), scanf('%g', '.0e-21'))
        self.assertEqual(None, scanf('%g', '.'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
