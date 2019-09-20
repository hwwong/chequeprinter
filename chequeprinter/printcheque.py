from python2printer import pyprinter
import datetime
from amount2words import currency2words


class TextField:

    def __init__(self, name=None, text=None, top=0, right=0, fontheight=100, width=0):
        self.name = name
        self.text = text
        self.top = top
        self.right = right
        self.fontheight = fontheight
        self.width = width

    def __str__(self):
        return self.name

    def toWording(self):
        line = []
        line.append(currency2words(float(self.text)))
        return line

    def toAmount(self):
        return '**{:,.2f}**'.format(float(self.text))

    def get_field(self):
        return {'name': self.name, 'text': self.text, 'top': self.top,
                'right': self.right, 'fontheight': self.fontheight, 'width': self.width}


class PrintCheque(pyprinter):

    def __init__(self):
        super().__init__()
        self.drawframe = False
        self.drawcross = True
        self.orbearer = True

    def CreateDoc(self, title, template):
        self.template = template
        self.LoadTemplate(template)
        self.width = template['cheque']['width']
        self.height = template['cheque']['height']
        super().CreateDoc(title, (self.width, self.height), False)
        super().SetOffset(template['cheque']
                          ['offset_x'], template['cheque']['offset_y'])

    def SetTextField(self, TextFields):
        self.payee = TextFields['payee']
        self.amount = TextFields['amount']
        self.line1 = TextFields['line1']
        self.line2 = TextFields['line2']
        self.day = TextFields['day']
        self.month = TextFields['month']
        self.year = TextFields['year']
        self.or_bearer2 = TextFields['or_bearer2']
        self.or_bearer1 = TextFields['or_bearer1']

    def LoadTemplate(self, template):
        for key, value in template['front'].items():
            # if key in ('payee', 'amount', 'line1', 'line2', 'day', 'month', 'year', 'or_bearer1', 'or_bearer2'):
            tf = TextField(key)
            tf.top = value['top']
            tf.right = value['right']
            tf.fontheight = value['fontheight']
            tf.width = value['width']
            template[key] = tf
        self.SetTextField(template)

    def draw_textfields(self, TextFields: TextField):

        for tf in TextFields:
            super().SetFontSize(tf.fontheight)
            if tf.name == 'amount':
                txt = '**%s**' % tf.toAmount()
            else:
                txt = tf.text
            super().Text(tf.top, tf.right, txt, self.drawframe)

    def AddSlip(self, acc_name, contact, bank, acc_no):

        self.template['back']['account_name']['text'] = acc_name
        self.template['back']['contact']['text'] = contact
        self.template['back']['bank']['text'] = bank
        self.template['back']['account_no']['text'] = acc_no

        if self.drawframe:
            super().DrawBox(0, 0, *(self.width, self.height))

        for x, v in self.template['back'].items():
            super().SetFontSize(v['fontheight'])
            super().Text(v['right'], v['top'], v['text'], self.drawframe)

    def AddCheque(self, payee, amount, date):

        super().AddPage()
        if self.drawframe:
            super().DrawBox(0, 0, *(self.width, self.height))

        if self.orbearer:
            super().SetFontSize(self.or_bearer1.fontheight)
            self.or_bearer1.text = "X" * \
                int(self.or_bearer1.width / super().GetTextSize('X')[0])
            super().Text(self.or_bearer1.right, self.or_bearer1.top,
                         self.or_bearer1.text, self.drawframe)

            super().SetFontSize(self.or_bearer2.fontheight)
            self.or_bearer2.text = "X" * \
                int(self.or_bearer2.width / super().GetTextSize('X')[0])
            super().Text(self.or_bearer2.right, self.or_bearer2.top,
                         self.or_bearer2.text, self.drawframe)

        super().SetFontSize(self.payee.fontheight)
        super().Text(self.payee.right, self.payee.top, payee, self.drawframe)

        super().SetFontSize(self.amount.fontheight)
        self.amount.text = amount
        txt1 = self.amount.toAmount()[:-4]
        l1, fh1 = super().GetTextSize(txt1)
        l2 = ('{:.2f}'.format(amount))[-2:]
        super().Text(self.amount.right, self.amount.top,
                     txt1 + '    **', self.drawframe)

        fh2 = (self.amount.fontheight * 0.8)
        super().SetFontSize(int(fh2))
        super().Text(self.amount.right + l1, int(self.amount.top + fh1 - fh2) - 4,
                     l2, self.drawframe)

        super().SetFontSize(self.line1.fontheight)
        txt = "**" + currency2words(amount) + "**"
        words = txt.split()
        x = len(words)
        l1 = txt
        while super().GetTextSize(l1)[0] > self.line1.width:
            x -= 1
            l1 = (" ").join(words[0:x])
        l1 = (" ").join(words[0:x])
        l2 = (" ").join(words[x:len(words)])
        super().Text(self.line1.right, self.line1.top, l1, self.drawframe)
        super().Text(self.line2.right, self.line2.top, l2, self.drawframe)

        super().SetFontSize(self.day.fontheight)
        super().Text(self.day.right, self.day.top, str(date.day).zfill(2), self.drawframe)
        super().Text(self.month.right, self.month.top,
                     str(date.month).zfill(2), self.drawframe)
        super().Text(self.year.right, self.year.top,
                     str(date.year).zfill(4), self.drawframe)

        if self.drawcross:
            lw = self.LineWeight
            super().SetLineWidth(3)
            super().DrawLine(150, 0, 0, 150)
            super().DrawLine(200, 0, 0, 200)
            super().SetLineWidth(lw)

        super().EndPage()


if __name__ == "__main__":

    BOC_template = {'cheque': {'width': 1720, 'height': 900, 'offset_x': -30, 'offset_y': -15},
                    'front': {'payee': {'top': 285, 'right': 150, 'fontheight': 60, 'width': 900},
                              'amount': {'top': 400, 'right': 1270, 'fontheight': 70, 'width': 900},
                              'line1': {'top': 405, 'right': 50, 'fontheight': 50, 'width': 840},
                              'line2': {'top': 525, 'right': 100, 'fontheight': 50, 'width': 900},
                              'day': {'top': 120, 'right': 1170, 'fontheight': 60, 'width': 900},
                              'month': {'top': 120, 'right': 1370, 'fontheight': 60, 'width': 900},
                              'year': {'top': 120, 'right': 1540, 'fontheight': 60, 'width': 900},
                              'or_bearer1': {'top': 270, 'right': 1450, 'fontheight': 40, 'width': 220},
                              'or_bearer2': {'top': 305, 'right': 1450, 'fontheight': 40, 'width': 220}},
                    'back': {'account_name': {'top': 70, 'right': 780, 'fontheight': 60, 'width': 800},
                             'contact': {'top': 240, 'right': 780, 'fontheight': 30, 'width': 350},
                             'bank': {'top': 450, 'right': 780, 'fontheight': 50, 'width': 840},
                             'account_no': {'top': 570, 'right': 780, 'fontheight': 60, 'width': 800}}}

    printer = PrintCheque()

    pt = printer.EnumPrinter()
    for k, x in enumerate(pt):
        print('%s. %s' % (k, x))
    p = int(input("Please select output printer? "))
    print('Printing to %s..... ' % pt[p])
    printer.SetActivePrinter(pt[p])
    printer.drawframe = True

    printer.CreateDoc("Cheques-Front", BOC_template)
    printer.SetFontType('Calibri')
    printer.AddCheque('ABC LIMITED', 43575.2, datetime.datetime.now())
    printer.AddSlip('ABC LIMITED', 'Mr. Wong', 'BOC', '012-123123-4')
    printer.EndDoc()

    printer.ClosePrinter()
    del printer
