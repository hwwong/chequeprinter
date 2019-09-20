# coding=utf-8
import sys

def num2words(num):
    nums_20_90 = ['Twenty', 'Thirty', 'Forty', 'Fifty',
                  'Sixty', 'Seventy', 'Eighty', 'Ninety']
    nums_0_19 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', "Nine", 'Ten',
                 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    nums_dict = {100: 'Hundred', 1000: 'Thousand',
                 1000000: 'Million', 1000000000: 'Billion'}
    if num < 20:
        return nums_0_19[int(num)]
    if num < 100:
        return nums_20_90[int(num/10-2)] + ('' if num % 10 == 0 else ' ' + nums_0_19[int(num % 10)])
    # find the largest key smaller than num
    maxkey = max([key for key in nums_dict.keys() if key <= num])
    return num2words(num/maxkey) + ' ' + nums_dict[maxkey] + ('' if num % maxkey == 0 else ' ' + num2words(num % maxkey))

def currency2chinese(amount):
    cnum_0_10 = [u'零',u'壹',u'貳',u'參',u'肆',u'伍',u'陸',u'柒',u'捌',u'玖',u'拾']
    unit = [u'分',u'角',u'元',u'拾',u'佰',u'仟',u'萬',u'億' ,u'圓'] 
    print ("{:,.2f}".format(amount))
    val = "{:.2f}".format(amount)
    l = len(val)
    print (l)
    print (val)
    val = val[:-3]
    print (val)

    # for i, x in enumerate(reversed(val)):
    #     print  x , i



def currency2words(amount):
    # print amount
    num = num2words(int(amount))
    frac = num2words(int(round((amount % 1)*100, 0)))
    # print frac
    if frac != "Zero":
        num += " And Cents " + frac
    return num + " Only"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        val = float (sys.argv[1])
        print (currency2words(val))
        print (currency2chinese(val))
    


