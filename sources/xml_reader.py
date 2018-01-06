#~~~~~~~~~ XML FILE READER ~~~~~~~~~

#~~~~~~ IMPORTS ~~~~~~

#------ Standard library imports ------
from os import path
from lxml import etree


#~~~~~~ INITIALIZATION ~~~~~~

#------ Paths for files ------
path_for_xml_file = path.join(path.abspath('../savegames/'),'template_save_game.xml')
path_for_xsd_file = path.join(path.abspath('../savegames/'),'template_save_game.xsd')

#------ Parsing files ------
xml_tree = etree.parse(path_for_xml_file)
xsd_tree = etree.parse(path_for_xsd_file)

#~~~~~~ SCHEMA VALIDATION ~~~~~~
xsd_schema = etree.XMLSchema(xsd_tree)
validation_result = xsd_schema.validate(xml_tree)

print(validation_result)
