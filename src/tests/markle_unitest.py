import unittest
import tools
import os

from helper import _print

path = os.path.abspath(os.path.join(__file__, '..', '..'))

class TestMarkle(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_markle_witness(self):
        # block 542213
        # aa21a9ed4a657fcaa2149342376247e2e283a55a6b92dcc35d4d89e4ac7b74488cb63be2
        # witness 4a657fcaa2149342376247e2e283a55a6b92dcc35d4d89e4ac7b74488cb63be2
        hashs = ["00" * 32, "66beaceb4be99da1e9824448231ab4fd37bacaee912381e779b37cf0e1dadad7", "aecb37e25954e15489e25548eb663ffdfd8a1362cac757ad62e9614453d2a577", "5b211bc589cbdf5ad86cab1e2fe91f01c8ab934d21536b35864d30a3ff778456"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'4a657fcaa2149342376247e2e283a55a6b92dcc35d4d89e4ac7b74488cb63be2' == hash}")
        self.assertEqual('4a657fcaa2149342376247e2e283a55a6b92dcc35d4d89e4ac7b74488cb63be2', hash)

        # minha
        # witness c7863adedb3ec9b29cc79e219aedb21e4bfc3aea5fcd8760c517d8d8a8b9b2c3
        hashs = ["00" * 32, "89e5a529855dc65c42f556601488f183df6d6213502652dfae91e27991d773c0"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'c7863adedb3ec9b29cc79e219aedb21e4bfc3aea5fcd8760c517d8d8a8b9b2c3' == hash}")
        self.assertEqual('c7863adedb3ec9b29cc79e219aedb21e4bfc3aea5fcd8760c517d8d8a8b9b2c3', hash)

        # minha
        # witness a475671cfb8a42d64c54f1d02e9ebfbd58c7082d3bea860ac3b0360236dd2613
        hashs = ["00" * 32, "d3746b35c794c243e3550114b0a06f2b060995ec80117567b1825472ddde4d73"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'a475671cfb8a42d64c54f1d02e9ebfbd58c7082d3bea860ac3b0360236dd2613' == hash}")
        self.assertEqual('a475671cfb8a42d64c54f1d02e9ebfbd58c7082d3bea860ac3b0360236dd2613', hash)
        
        # minha
        # witness 53ace8b55a2bc6fbc2f095dffa2ffc124c5165a8ed7f4d4be00cb4b5d589d4d2
        hashs = ["00" * 32, "db915752b1787d4c81de6ec9e802492d71ffcebca970fcb25d2960620a69a1b2", "201959054f6b7d786eba7bc323e1991b0de42e914c97192c66bbd10af615c0b3", "a3851be31cedd132e160b3fbd943a8f89e9d084a7ed157897daa93b484e2a681", "d3746b35c794c243e3550114b0a06f2b060995ec80117567b1825472ddde4d73"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'53ace8b55a2bc6fbc2f095dffa2ffc124c5165a8ed7f4d4be00cb4b5d589d4d2' == hash}")
        self.assertEqual('53ace8b55a2bc6fbc2f095dffa2ffc124c5165a8ed7f4d4be00cb4b5d589d4d2', hash)

        # minha
        # witness 7b5541aa4d28dc3c37fc89c6da97fae70645b551db37644a17d4b74eb5268a15
        hashs = ["00" * 32, "db915752b1787d4c81de6ec9e802492d71ffcebca970fcb25d2960620a69a1b2", "26ea034080eb9f1b8f08020fc898cef88ee2b22c9eed24954758174cc97bc5c2", "201959054f6b7d786eba7bc323e1991b0de42e914c97192c66bbd10af615c0b3", "a3851be31cedd132e160b3fbd943a8f89e9d084a7ed157897daa93b484e2a681", "d3746b35c794c243e3550114b0a06f2b060995ec80117567b1825472ddde4d73"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'7b5541aa4d28dc3c37fc89c6da97fae70645b551db37644a17d4b74eb5268a15' == hash}")
        self.assertEqual('7b5541aa4d28dc3c37fc89c6da97fae70645b551db37644a17d4b74eb5268a15', hash)

        # minha
        # witness d9cec79475935de059590d7a1fc38ebedf9d2d20edd18ecd0fc2efcd20ca2416
        hashs = ["00" * 32, "db915752b1787d4c81de6ec9e802492d71ffcebca970fcb25d2960620a69a1b2", "26ea034080eb9f1b8f08020fc898cef88ee2b22c9eed24954758174cc97bc5c2", "201959054f6b7d786eba7bc323e1991b0de42e914c97192c66bbd10af615c0b3", "6d2f55293bc4cbab01631bfa0ac45aec8f3c667f3e3d45032e0b54a440c9b0b7", "a3851be31cedd132e160b3fbd943a8f89e9d084a7ed157897daa93b484e2a681", "d3746b35c794c243e3550114b0a06f2b060995ec80117567b1825472ddde4d73"]
        hash = tools.calc_markle_witness(hashs)
        _print("TEST HASH", f"{'d9cec79475935de059590d7a1fc38ebedf9d2d20edd18ecd0fc2efcd20ca2416' == hash}")
    
    def test_markle_root(self):
        pass


def _main():
    unittest.main(__name__)