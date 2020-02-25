import cast.application
import logging
import ast
import re
from unicodedata import category
from cast.application.internal import application
from cast.application import ApplicationLevelExtension, create_link, ReferenceFinder
from cast.analysers import log, CustomObject, external_link, create_link
from _overlapped import NULL
import datetime
from cast.analysers.internal.plugin import fullname
from pprint import pprint 
from distutils.log import Log

class ApplicationExtension(ApplicationLevelExtension):

    def end_application(self, application):
     pass
  

if __name__ == '__main__':
    pass
