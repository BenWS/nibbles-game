class ProcessLog:
  def __init__(self):
    pass

  def log(self, error_message, level=None):
    if level == None:
      print('INFO: ',error_message)