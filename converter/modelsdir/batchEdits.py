from pymarc import MARCReader, Record, Field
from converter.modelsdir.utilities import utilityFunctions

class batchEdits:


    def __init__(self):
        self.utilities = utilityFunctions()

    def ER_EAI_2nd(self, x, name='ER-EAI-2ND'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-2nd'))
            # ADD local 730, 949 
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a','Early American imprints (Online).', 'n', 'Second series,', 'p','Shaw-Shoemaker.', '5', 'OCU']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec)
            rec = self.utilities.CharRefTrans(rec)
        x = self.utilities.CreateMRC(recs)
        return x


    def ER_EAI_1st(self, x, name='ER-EAI-1st'):
        #iterate over list of Record objects
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-1st'))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'],subfields = ['a','Early American imprints (Online).', 'n', 'First series,','p','Evans.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '506', indicators = ['\\', '\\'], subfields = ['a','Access restricted to users at subscribing institutions']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec, 'Readex')
            rec = self.utilities.CharRefTrans(rec)
        x = self.utilities.CreateMRC(recs)
        return x

########### TODO: add ER_OECD ################


    def ER_OCLC_WCS_SDebk(self, x, name='ER-OCLC-WCS-SDebk'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0','\\'],subfields = ['a','ScienceDirect cBook Series.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '003',data = 'ER-OCLC-WCS-SDebk'))
            rec.add_ordered_field(Field(tag = '002',data = 'OCLC-WCS-SDebk'))
            #change 856 to 956
            rec.add_ordered_field(Field(tag = '956', data = rec['856'].value()))
            rec.remove_field(rec.get_fields('856')[0])
            #add colon to 956$3
            rec['956']['3'] = re.sub(r'ScienceDirect', 'ScienceDirect :', rec['956']['3'])
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec, 'Readex')
            rec = self.utilities.CharRefTrans(rec)
        x = self.utilities.CreateMRC(recs)
        return x

    def ER_NBER(self, x, name='ER-NBER'):
        recs = self.utilities.BreakMARCFile(x)
        # NBER has begun using two 856 fields. DELETE 856 fields with www.nber.org ... RETAIN 856 fields with dx.doi.org
        for rec in recs:
            for field in rec:
                if field.tag == '856' and field['u'].find("nber.org") >= 0:
                    rec.remove_field(field)
            #move value of 001 to 002
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            #rec.add_ordered_field(Field(tag = '830', indicators = ['\\', '0'], subfields = ['a', 'Working paper series (National Bureau of Economic Research : Online)']))
            rec.add_ordered_field(Field(tag = '730', indicators =['0','\\'],subfields = ['a','NBER working paper series online.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '533', indicators = ['\\','\\'],subfields = ['a','Electronic reproduction.', 'b', 'Cambridge, Mass.', 'c', 'National Bureau of Economic Research,', 'd', '200-', 'e', '1 electronic text : PDF file.', 'f', 'NBER working paper series.', 'n', 'Access restricted to patrons at subscribing institutions']))
            rec.add_ordered_field(Field(tag = '003',data = 'ER-NBER'))
            # 530 field, change Hardcopy to Print
            rec['530']['a'] = 'Print version available to institutional subscribers.'
            # 490 and 830 fields lack ISBD punctuation, supply where lacking
            #x = re.sub('(?m)^(=490.*)[^ ;](\$v.*)', '\\1 ;\\2', x)
            four90a = rec['490']['a'] + ' ;'
            rec['490']['a'] = four90a
            eight30a = rec['830']['a'] + ' ;'
            rec['830']['a'] = eight30a
            # delete supplied 690 fields
            rec.remove_field(rec.get_fields('690')[0])
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec, 'NBER')
            rec = self.utilities.CharRefTrans(rec)
            rec = self.utilities.AddEresourceGMD(rec)
        x = self.utilities.CreateMRC(recs)
        return x
