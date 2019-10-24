import warnings


MANDARIN_NUM_MAPPING = {
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "千": 1000,
    "万": 10000,
    "亿": 10000*10000,
}

NUM_UPPER = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九')
NUM_UNIT = ('十', '百', '千')

SPECIAL_UNIT = ('万', '亿')

DECIMAL_LENGTH = 2

SPECAIL_NUM0 = 0
SPECIAL_NUM0_UPPER = "零"
SPECIAL_NUM1_UPPER = "一"

SPECIAL_NUM1_UNIT = "十"

WARNING_MANDARIN = "亿亿"

DOT = "点"

# 十一 --> 一十一
_add_start_ten = lambda x: (SPECIAL_NUM1_UPPER + x) if x.startswith(SPECIAL_NUM1_UNIT) else x

_is_digit_mandarin = lambda x: x.count(DOT) == 0

_split_float_mandarin = lambda x: x.split(DOT)

_is_empty = lambda x: True if len(x) == 0 else False


def _get_float_amount(amount_mandarin):
    if amount_mandarin == SPECIAL_NUM0_UPPER:
        return SPECAIL_NUM0
    # 只需要前两位
    amount_mandarin = amount_mandarin[:2]

    BASIC_MULTIPLIER = 1e-1
    multiplier = 1
    amout_sum = 0
    for char in amount_mandarin:
        multiplier *= BASIC_MULTIPLIER
        num = MANDARIN_NUM_MAPPING.get(char, None)
        if num is None:
            raise ValueError("输入部分数值异常 : {}".format(amount_mandarin))
        amout_sum += multiplier * num
    
    # 计算过程中会出现精度问题, 最高保留到百分位
    return round(amout_sum, DECIMAL_LENGTH)

def _get_digit_amount(amount_mandarin):
    amount_mandarin = _add_start_ten(amount_mandarin)
    amount_sum = 0
    amount_stack = []
    for each in amount_mandarin:
        if each == SPECIAL_NUM0_UPPER:
            continue
        elif each in NUM_UPPER:
            amount_stack.append(MANDARIN_NUM_MAPPING.get(each))
        elif each in NUM_UNIT:
            amount_stack.append(amount_stack.pop() * MANDARIN_NUM_MAPPING.get(each))
        elif each in SPECIAL_UNIT:
            # 一万亿 --> 1e12 √
            if _is_empty(amount_stack):
                amount_sum *= MANDARIN_NUM_MAPPING.get(each)
                continue
            amount_sum += sum(amount_stack) * MANDARIN_NUM_MAPPING.get(each)
            amount_stack.clear()
        else:
            raise ValueError("输入部分数值异常 : {}".format(amount_mandarin))
    amount_sum += sum(amount_stack)
    return amount_sum

def conv_mandarin_to_amount(amount_mandarin):

    if WARNING_MANDARIN in amount_mandarin:
        warnings.warn("数字大于1亿亿，无法保证转换正确 : {}".format(amount_mandarin))

    if _is_digit_mandarin(amount_mandarin):
        amount_mandarin += DOT + SPECIAL_NUM0_UPPER

    # 有多个DOT只处理第一个DOT前后内容
    digit_part_mandarin, float_part_mandarin, *_ = _split_float_mandarin(amount_mandarin)
    digit_part = _get_digit_amount(digit_part_mandarin)
    float_part = _get_float_amount(float_part_mandarin)
    return digit_part + float_part

    


