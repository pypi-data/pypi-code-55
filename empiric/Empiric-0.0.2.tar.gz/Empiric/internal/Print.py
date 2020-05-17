class COLORS:
  DEFAULT = '\033[0m'
  ERROR = '\033[91m'

class Print:
  @staticmethod
  def log(*msgs):
    msg = ''.join(msgs)
    print(f' * {msg}')
  @staticmethod
  def log2(*msgs):
    msg = ''.join(msgs)
    print(f'   {msg}')
  @staticmethod
  def logWarning(*msgs):
    Print.log(COLORS.ERROR, *msgs, COLORS.DEFAULT)
  @staticmethod
  def log2Warning(*msgs):
    Print.log2(COLORS.ERROR, *msgs, COLORS.DEFAULT)
