try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = []

setup(name              = 'dispense_bot',
      version           = '1.0.0',
      author            = '',
      author_email      = '',
      description       = '',
      license           = 'MIT',
      url               = '',
      entry_points      = {
          'console_scripts': [
              'dispensebot_receiver = dispense_bot.receiver:run',
              'dispensebot_poller = dispense_bot.poller:run',
              'dispensebot_manual = dispense_bot.manual_dispense:run',
          ],
      },
      dependency_links  = [
          'https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library/tarball/master#egg=Adafruit_MotorHAT-1.4',
          'https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.7',
      ],
      install_requires  = [
          'Adafruit-GPIO>=0.7',
          'Adafruit_MotorHAT>=1.4.0',
          'requests',
      ],
      packages          = find_packages())
