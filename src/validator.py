from lxml import etree


class ReportValidator:

    def __init__(self):
        XML_schema_tree = etree.parse('src/XMLSchema.xsl')
        self.validator = etree.XMLSchema(XML_schema_tree)

    def validate(self, report_path):
        report_tree = etree.parse(report_path)
        validity = self.validator.validate(report_tree)
        return validity
