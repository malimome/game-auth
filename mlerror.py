import traceback
import sys
import os

def show_frame(a=0,b=3):
    ret = ""
    for num in range(a,b):
        try:
          frame = sys._getframe(num)
        except:
          continue
        ret += str(num-a)
        ret += "\n  frame     = sys._getframe(%s)" % num
        ret += "\n  function  = %s()" % frame.f_code.co_name
        ret += "\n  file/line = %s:%s" % (frame.f_code.co_filename, frame.f_lineno)
    return ret

class printer():
    """
        Fake logger class to print to screen
    """
    def info(self, text):
        print (text)
    def error(self, text):
        print (text)
    def debug(self, text):
        print (text)

def printErrorStack(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]
    filename = os.path.basename(filename)
    logger = printer()

    logger.error(e)
    logger.error("(type->%s) (%s->%s->%s)" % (exc_type, 
                  filename, func_name, line_num))
    logger.info(show_frame(2, 4))
    return True

class ErrEmptyData(Exception):
  def __init__(self):
    self.message = "Empty data set"

