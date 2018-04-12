from pymarc import MARCReader, Record, Field
from converter.modelsdir.utilities import utilityFunctions

class batchEdits:

    def __init__(self):
        utilities = utilityFunctions()

    def ER_EAI_2nd(self, x, name='ER-EAI-2ND'):
        print('\nRunning change script '+ name + '\n')
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-2nd'))
            # ADD local 730, 949 before supplied 008
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a','Early American imprints (Online).', 'n', 'Second series,', 'p','Shaw-Shoemaker.', '5', 'OCU']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec)
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x


    def ER_EAI_1st(self, x, name='ER-EAI-1st'):
        print('\nRunning change script '+ name + '\n')
        #iterate over list of Record objects
        recs = utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002, and add 003
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            rec.remove_field(rec.get_fields('001')[0])
            rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-EAI-1st'))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'],subfields = ['a','Early American imprints (Online).', 'n', 'First series,','p','Evans.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '506', indicators = ['\\', ''], subfields = ['a','Access restricted to users at subscribing institutions']))
            rec.remove_field(rec.get_fields('008')[0])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec, 'Readex')
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x

########### TODO: add ER_OECD ################


    def ER_OCLC_WCS_SDebk(self, x, name='ER-OCLC-WCS-SDebk'):
        print('\nRunning change script '+ name + '\n')
        recs = utilities.BreakMARCFile(x)
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
            #x = re.sub('(?m)\$3ScienceDirect', '$3ScienceDirect :', x)
            rec['956']['3'] = re.sub(r'ScienceDirect', 'ScienceDirect :', rec['956']['3'])
            rec = utilities.DeleteLocGov(rec)
            rec = utilities.Standardize856_956(rec, 'Readex')
            rec = utilities.CharRefTrans(rec)
        rec = utilities.SaveToMRK(recs, filename)
        x = utilities.MakeMARCFile(recs, filename)
        return x
