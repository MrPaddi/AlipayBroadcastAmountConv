'''
人民币数字转大写汉字
'''

import re
import sys
import warnings

# 局部不能>=万
MAX_LOCAL_LENGTH = 4
# 全局不能>=亿亿, 否则警告
MAX_LENGTH = MAX_LOCAL_LENGTH*4
# 小数只保留2位，无视四舍五入
DECIMAL_LENGTH = 2

SPECIAL_NUM0 = "0"
SPECIAL_NUM0_UPPER = "零"

SPECIAL_NUM1_UPPER = "一"
SPECIAL_NUM1_UNIT = "十"

SPECIAL_NUMB_UNIT = "亿"
SPECIAL_NUMB_UPPER_UNIT = "零亿"

DOT = "点"
DOT_NUM = "."

NUM_UPPER = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九')
NUM_UNIT = ('', '十', '百', '千')

BIG_UNIT = ("万", "亿")

_clear_repeat_zero = lambda x: re.sub(r"{}+".format(SPECIAL_NUM0_UPPER), SPECIAL_NUM0_UPPER, x)

_clear_end_zero = lambda x: x[:-1] if x.endswith(SPECIAL_NUM0_UPPER) else x

_clear_start_zero = lambda x: re.sub(r"^{}+".format(SPECIAL_NUM0), "", x)

_clear_billion_zero = lambda x: re.sub(r"{}".format(SPECIAL_NUMB_UPPER_UNIT), SPECIAL_NUMB_UNIT, x)

# 以 一十 开头的简读作 十
_clear_start_ten = lambda x: x[1:] if x.startswith(SPECIAL_NUM1_UPPER + SPECIAL_NUM1_UNIT) else x

# 五百零零-> 五百零 -> 五百
_get_standard_upper = lambda x: _clear_end_zero(_clear_repeat_zero(x))

is_legal_amount = lambda x: True if x.replace(DOT_NUM, "").isdigit() else False

def _gen_digit_part(num_str):
    """
    '4020' ->  divmod(4320, pow(10, 3)) -->4 320 -->'四'+ '千' + _gen_digit_part('320')
    '020' ->  '零' + _gen_digit_part('20')
    ...
    '0' -> divmod(0, pow(10, 0)) -->0, 0 --> '零' + '' + _gen_digit_part('')
    """
    if num_str == "" or len(num_str) > MAX_LOCAL_LENGTH:
        return ""
    num_len = len(num_str)
    if num_str.startswith(SPECIAL_NUM0):
        return SPECIAL_NUM0_UPPER + _gen_digit_part(num_str[1:])
    div, mod = divmod(int(num_str), pow(10, num_len-1))
    mod = "" if mod ==0 else str(mod)
    num_upper = NUM_UPPER[div]
    num_unit = NUM_UNIT[num_len-1]
    
    return num_upper + num_unit + _gen_digit_part(num_str[1:])


def _gen_decimal_part(num_str):
    num_str = num_str[:DECIMAL_LENGTH]
    result = ""
    for i in num_str:
        result += NUM_UPPER[int(i)]
    return result

 
def conv_amount_to_mandarin(amount_str):
    '''
    货币数字转大写:
    '1203.05' --> 一千二百零三点零五元
    '''
    if not is_legal_amount(amount_str):
        raise ValueError("输入浮点数或整数对应字符串类型 : {}".format(amount_str))
    amount_str = _clear_start_zero(amount_str)

    if DOT_NUM not in amount_str:
        amount_str += DOT_NUM + SPECIAL_NUM0

    digit_part, decimal_part, *_ = amount_str.split(".")

    if len(digit_part) > MAX_LENGTH:
        warnings.warn("数字大于1亿亿，无法保证表达正确 ：{}".format(amount_str))
    
    digit_part_upper = ""
    BIG_UNIT_LENGTH = len(BIG_UNIT)
    # 用于在亿/万之间切换的标识
    depth = -1
    digit_end_part = digit_part[-4:]
    # 支持大数转换
    while True:
        digit_part = digit_part[:-4]
        current_digit_str =digit_part[-4:]
        if current_digit_str == "":
            break
        depth += 1
        unit = BIG_UNIT[depth%BIG_UNIT_LENGTH]
        current_digit = _get_standard_upper(_gen_digit_part(current_digit_str))
        # '八亿零四千二百一十' √ ; '八亿四千二百一十' ×
        # 十亿零五千零二十五万四千点五
        if current_digit == "" and unit == BIG_UNIT[0]:
            unit = SPECIAL_NUM0_UPPER

        # '十亿零五千零二十五万四千点五'√  '十亿五千零二十五万四千点五'×
        if unit in BIG_UNIT and current_digit_str.endswith(SPECIAL_NUM0):
            unit += SPECIAL_NUM0_UPPER

        digit_part_upper = current_digit + unit + digit_part_upper

    digit_part_upper += _gen_digit_part(digit_end_part)
    # 只有当一十开头会读十，其他位数全部用一十
    digit_part_upper = _clear_start_ten(_get_standard_upper(digit_part_upper))
    # 上述实现会出现 一亿零六百万零五百一十亿零亿零四千五百 情况，将零亿替换为亿
    digit_part_upper = _clear_billion_zero(digit_part_upper)

    decimal_part_upper = _get_standard_upper(_gen_decimal_part(decimal_part))

    if decimal_part_upper != "":
        decimal_part_upper = DOT + decimal_part_upper
    if digit_part_upper == "":
        digit_part_upper = SPECIAL_NUM0_UPPER
    return digit_part_upper + decimal_part_upper

