from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='captchium',
  version='1.0.0',
  description='Python library for solving Google reCAPTCHA challenges',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/d3kxrma/captchium',  
  author='dekxrma',
  author_email='qqdjnuxez@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, recapthca, captcha, solver, selenium',
  packages=find_packages(),
  install_requires=['requests', 'SpeechRecognition', 'selenium'] 
)