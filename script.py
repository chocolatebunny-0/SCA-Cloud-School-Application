import os
import platform
import shutil
import subprocess
import requests
import tempfile
import tarfile
from enum import Enum

HOME = os.path.expanduser('~')

programsToInstall = {
  'wget': '1.5.3',
  'curl': '7.50.3',
  'nodejs': '' #install latest nodejs
}

class SupportedOS(Enum):
  WINDOWS = 'Windows'
  LINUX = 'Linux'
  MACOS = 'Darwin'

def checkIsInstalled(program):
  return shutil.which(program) != None

def makeSystemCall(cmd):
  subprocess.call(cmd, shell=True)

def installWget(osType, version):
  print('Installing wget binary for {0}...'.format(osType))
  if(osType == SupportedOS.LINUX.value or osType == SupportedOS.MACOS.value):
    # create tempfile to store our downloaded source code in
    fd, path = tempfile.mkstemp()

    print('Downloading wget sourcefiles...')

    r = requests.get('https://ftp.gnu.org/gnu/wget/wget-{0}.tar.gz'.format(version))

    currentWD = os.getcwd()
    wgetInstallPath = '{0}/wget-{1}'.format(HOME, version)

    try:
        with os.fdopen(fd, 'wb') as tmp:
          # save request response in temp file
          tmp.write(r.content)
          # switch to HOME directory
          os.chdir(HOME)
          print('Extracting source files for wget...')
          tf = tarfile.open(path)
          tf.extractall()
          print('wget extracted to {0}...'.format(wgetInstallPath))
          print('Building wget...')
          
          os.chdir(wgetInstallPath)

          makeSystemCall("./configure --prefix=$HOME && make -f ./Makefile")

          os.environ['PATH'] += ':'+wgetInstallPath

    finally:
        # clean up tempfile
        os.remove(path)
        os.chdir(currentWD)
  else:
    print('support for windows not yet implemented')

def installCurl(osType, version):
  if (osType == SupportedOS.LINUX.value or osType == SupportedOS.MACOS.value):
    print('Installing curl binary for {0}...'.format(osType))

     # create tempfile to store our downloaded source code in
    fd, path = tempfile.mkstemp()

    r = requests.get('http://curl.haxx.se/download/curl-{0}.tar.gz'.format(version))

    currentWD = os.getcwd()

    curlInstallPath = '{0}/curl-{1}'.format(HOME, version)

    try:
      with os.fdopen(fd, 'wb') as tmp:
         # save request response in temp file
        tmp.write(r.content)
        # switch to HOME directory
        os.chdir(HOME)
        print('Extracting source files for curl...')
        tf = tarfile.open(path)
        tf.extractall()
        print('curl extracted to {0}...'.format(curlInstallPath))
        print('Building curl...')
        os.chdir(curlInstallPath)
        makeSystemCall("./configure && make")
    finally:
        # clean up tempfile
        os.remove(path)
        os.chdir(currentWD)

  else:
    print('support for windows not yet implemented')

def installNodeJS(osType):
  if (osType == SupportedOS.MACOS.value):
    # See https://nodejs.org/en/download/package-manager/#macos
    subprocess.call('curl "https://nodejs.org/dist/latest/node-${VERSION:-$(wget -qO- https://nodejs.org/dist/latest/ | sed -nE \'s|.*>node-(.*)\.pkg</a>.*|\1|p\')}.pkg" > "$HOME/Downloads/node-latest.pkg" && sudo installer -store -pkg "$HOME/Downloads/node-latest.pkg" -target "/"')

  elif (osType == SupportedOS.LINUX.value):
    subprocess.call('curl-o-https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash')
  else:
    print('os type not implemeted yet...')

def installDependencies():
  currentOS = platform.system()

  for program, version in programsToInstall.items():
    if(checkIsInstalled(program)):
      print('Found {0}, skipping installation...'.format(program))
    else: 
      # install program
      print('Starting installation for {0}...'.format(program))
      if(program == 'wget'):
        installWget(currentOS, version)
      elif(program == 'curl'):
        installCurl(currentOS, version)
      elif(program == 'nodejs'):
        installNodeJS(currentOS)

# Declare the main function
def main():
  installDependencies()

# Call the main function
if __name__ == "__main__":
  main()
