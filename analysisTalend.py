import cast.analysers.ua
from cast.analysers import log as Print, CustomObject, Bookmark,create_link
from fileinput import filename
from os.path import basename, splitext
import cast.analysers
from cast.analysers import log, CustomObject, external_link, create_link
import csv
import os
from collections import defaultdict
import re
from setuptools.sandbox import _file
import xml.etree.ElementTree as ET
from Cython.Compiler.Options import annotate
import random 


class TalendExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.name = ""
        self.fielPath = ""
        self.Talend_Template_fullname = "" 
        self.Processtext=""
        self.contextname = ""
        self.Processxmltext=""
      
    def start_analysis(self):
        Print.debug("Inside start_analysis")
        
        
    
    def start_file(self,file):
        Print.debug("Inside start_file")
        
        if file.get_name().endswith('.item'):
            try :
                if (os.path.isfile(file.get_path())):
                    tree = ET.parse(file.get_path(), ET.XMLParser(encoding="UTF-8"))
                    root=tree.getroot()
                    for a in root.iter():
                        #Print.debug(a.tag)
                        self.findXMLProcess(a, 'context', file)
                        self.findXMLProcesscontext(a, 'contextParameter', file)
                        self.findXMLProcessparameter(a, 'elementParameter', file)
                        self.findXMLProcessMetadata(a, 'metadata', file)
                        self.findXMLProcessparameter(a, 'column', file)
                        
                        
            except:
                 return     
    def findXMLProcess(self, a, annotext, file):  
        if a.tag == annotext:
            #Print.debug('xml'+a.tag)
            if a.get('name') is not None:
                self.processxmltext ='name'
                self.contextname =a.get(self.processxmltext)
                self.processtext='Talend_PT_Context'
                self.CreateaXMLprocesstype(file,a, annotext)
                
    def findXMLProcessMetadata(self, a, annotext, file):  
        if a.tag == annotext:
            #Print.debug('xml'+a.tag)
            if a.get('name') is not None:
                self.processxmltext ='name'
                self.contextname =a.get(self.processxmltext)
                self.processtext='Talend_PT_Metadata'
                self.CreateaXMLprocesstype(file,a, annotext)
                
    def findXMLProcesscontext(self, a, annotext, file):  
        if a.tag == annotext:
            #Print.debug('xml'+a.tag)
            if a.get('name') is not None:
                self.processxmltext ='name'
                self.processtext='Talend_PT_elementParameter'
                self.CreateaXMLprocessparameter(file,a, annotext)
                
    def findXMLProcessparameter(self, a, annotext, file):  
        if a.tag == annotext:
            #Print.debug('xml'+a.tag)
            if a.get('name') is not None:
                self.processxmltext ='name'
                self.processtext='Talend_PT_contextParameter'
                self.CreateaXMLprocessparameter(file,a, annotext)

    def CreateaXMLprocesstype(self,file, a, xsdtext):
        try :
            if a.tag == xsdtext:
                processObj = cast.analysers.CustomObject()
                processObj.set_name(a.get(self.processxmltext))
                processObj.set_type(self.processtext)
                processObj.set_parent(file)
                parentFile = file.get_position().get_file() 
                self.fielPath = parentFile.get_fullname()
                processObj.set_guid(self.fielPath+a.get(self.processxmltext)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                processObj.save()
                Print.debug('Creating talend '+ xsdtext + ' object '+ a.get(self.processxmltext)) 
                xmlParsing.add_propertyfld(processObj, a, 'TypeName','field', self.contextname )
                #processObj.save_position(Bookmark(file,1,1,-1,-1))
        except:
                 return       
               
    def CreateaXMLprocessparameter(self,file, a, xsdtext):
        try :
            if a.tag == xsdtext:
                processObj = cast.analysers.CustomObject()
                processObj.set_name(a.get(self.processxmltext))
                processObj.set_type(self.processtext)
                processObj.set_parent(file)
                parentFile = file.get_position().get_file() 
                self.fielPath = parentFile.get_fullname()
                processObj.set_guid(self.fielPath+a.get(self.processxmltext)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                processObj.save()
                Print.debug('Creating talend '+ xsdtext + ' object '+ a.get(self.processxmltext)) 
                xmlParsing.add_property(processObj, a, 'TypeName','field', self.contextname)
                #processObj.save_position(Bookmark(file,1,1,-1,-1))
        except:
                 return                      
    
    def end_file(self,file):
        pass   
    
    def end_analysis(self):       
        pass
class xmlParsing():  
    
    @staticmethod
    def add_property(obj, ele, prop,fld, ctx ):
        if ele.get(fld) is not None:
            Print.debug(' - %s: %s' % (prop, ele.get(fld)))
            obj.save_property('ProcessTypeProperties.%s' % prop, ele.get(fld))
        else:
            Print.debug(' - %s: %s' % (prop, ctx))
            obj.save_property('ProcessTypeProperties.%s' % prop, ctx)
         
    @staticmethod
    def add_propertyfld(obj, ele, prop,fldtext ):
        if ele.get(fldtext) is not None:
            Print.debug(' - %s: %s' % (prop, ele.get(fldtext)))
            obj.save_property('ProcessTypeProperties.%s' % prop, ele.get(fldtext))
        else:
            obj.save_property('ProcessTypeProperties.%s' % prop, "None")
        