from setuptools import setup

setup(
   name='pnl_report',
   version='0.5.0',
   description='Offers FIFO, LIFO, AVG P&L calculations via a report',
   author='Elie',
   # author_email='foomail@foo.com',
   packages=['pnl_report'],
   install_requires=['numpy', 'pandas', 'functools'],
)