import variables

configFileName = variables.configFileName
def configFileExists():
  try:
    f = open(configFileName, 'r')
    f.close()
    return True
  except FileNotFoundError:
    return False
  

def createConfigFile(googleId, googlePass,webclassId, webclassPass):
  f = open(configFileName,'w')
  f.write("{}\n{}\n{}\n{}".format(googleId,googlePass,webclassId,webclassPass))
  f.close()


def resetConfigFile():
  f = open(configFileName,'w')
  f.write("")
  f.close()

def readConfigFile():
  f = open(configFileName, 'r')
  data = f.readlines()
  return data

