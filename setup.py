from setuptools import setup

setup(name='anymesh',
      version='0.4.0',
      description='AnyMesh is a multi-platform, decentralized, auto-discovery, auto-connect mesh networking API.',
      url='https://github.com/AnyMesh/anyMesh-Python.git',
      author='Dave Paul',
      author_email='davepaul0@gmail.com',
      license='MIT',
      packages=['anymesh'],
      install_requires=['twisted'],
      zip_safe=False)