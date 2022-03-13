from lxml import etree


class Validator:

    def __init__(self):
        xmlschema_doc = etree.parse('XMLSchema.xsl')
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path):
        xml_doc = etree.parse(xml_path)
        result = self.xmlschema.validate(xml_doc)

        return result
