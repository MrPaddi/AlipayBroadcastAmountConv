import unittest
from num2upper import conv_amount_to_mandarin
from upper2num import conv_mandarin_to_amount

class TestNumUpper(unittest.TestCase):

    def test_conv_amount2mandarin(self):
        self.assertEqual(conv_amount_to_mandarin("0.547"), "零点五四")
        self.assertEqual(conv_amount_to_mandarin("0.05"), "零点零五")
        self.assertEqual(conv_amount_to_mandarin("0.5"), "零点五")
        self.assertEqual(conv_amount_to_mandarin("1.5"), "一点五")
        self.assertEqual(conv_amount_to_mandarin("001.5"), "一点五")
        self.assertEqual(conv_amount_to_mandarin("10.5"), "十点五")
        self.assertEqual(conv_amount_to_mandarin("12.50"), "十二点五")
        self.assertEqual(conv_amount_to_mandarin("4010.00"), "四千零一十")
        self.assertEqual(conv_amount_to_mandarin("84010"), "八万四千零一十")
        self.assertEqual(conv_amount_to_mandarin("12305410.54"), "一千二百三十万零五千四百一十点五四")
        self.assertEqual(conv_amount_to_mandarin("8000000012"), "八十亿零一十二")
        self.assertEqual(conv_amount_to_mandarin("1050254000.50"), "十亿零五千零二十五万四千点五")
        self.assertEqual(conv_amount_to_mandarin("100000001000.50"), "一千亿零一千点五")
        self.assertEqual(conv_amount_to_mandarin("9000000500254000.50"), "九千万零五亿零二十五万四千点五")
        self.assertEqual(conv_amount_to_mandarin("9000000050254000.50"), "九千万亿零五千零二十五万四千点五")
        self.assertEqual(conv_amount_to_mandarin("900000000000000001.50"), "九十亿亿零一点五")
        self.assertEqual(conv_amount_to_mandarin("0500"), "五百")
        self.assertEqual(conv_amount_to_mandarin('12305410'), "一千二百三十万零五千四百一十")
        self.assertEqual(conv_amount_to_mandarin('105410'), "十万零五千四百一十")
    
    def test_conv_mandarin2amount(self):
        self.assertEqual(conv_mandarin_to_amount("八十亿零一十二"), 8000000012)
        self.assertEqual(conv_mandarin_to_amount("十万一千零一十"), 101010)
        self.assertEqual(conv_mandarin_to_amount("一千二百三十万零五千四百一十"), 12305410)
        self.assertEqual(conv_mandarin_to_amount("零点五四"), 0.54)
        self.assertEqual(conv_mandarin_to_amount("零点零五"), 0.05)
        self.assertEqual(conv_mandarin_to_amount("零点五"), 0.5)
        self.assertEqual(conv_mandarin_to_amount("一点五"), 1.5)
        self.assertEqual(conv_mandarin_to_amount("十点五"), 10.5)
        self.assertEqual(conv_mandarin_to_amount("十二点五"), 12.5)
        self.assertEqual(conv_mandarin_to_amount("四千零一十"), 4010)
        self.assertEqual(conv_mandarin_to_amount("一千二百三十万零五千四百一十点五四"), 12305410.54)
        self.assertEqual(conv_mandarin_to_amount("十亿零五千零二十五万四千点五"), 1050254000.5)
        self.assertEqual(conv_mandarin_to_amount("九十亿亿零一点五"), 900000000000000001.50)
        self.assertEqual(conv_mandarin_to_amount("九千万亿零五千零二十五万四千点五"), 9000000050254000.50)

    