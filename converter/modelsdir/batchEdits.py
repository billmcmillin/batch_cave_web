from pymarc import MARCReader, Record, Field
from converter.modelsdir.utilities import utilityFunctions
import re

class batchEdits:


    def __init__(self):
        self.utilities = utilityFunctions()


    def ER_ASP_EDIV(self, x, name='ER-ASP-EDIV'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            # Change =001 field to =002,
            rec.add_ordered_field(Field(tag = '002',data = rec['001'].value()))
            # remove 001
            rec.remove_field(rec.get_fields('001')[0])
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-ASP-EDIV'))
            rec.add_ordered_field(Field(tag = '710', indicators = ['\\', '2'], subfields = ['a','Alexander Street Press']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a','Alexander Street Press.','p','Education in video.','5','OCU']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec,'Alexander Street Press' )
            rec = self.utilities.order_007(rec)
            rec = self.utilities.AddEresourceGMD(rec)
        x = self.utilities.CreateMRC(recs)
        return x

    def ER_TF_CRC(self, x, name='ER-T&F-CRC'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
            # Change =001 field to =002,
            rec.add_ordered_field(Field(tag = '002',data = 't&fcrc_' + rec['001'].value()))
            # remove 001
            rec.remove_field(rec.get_fields('001')[0])
            # remove supplied 003
            try:
                rec.remove_field(rec.get_fields('003')[0])
            except:
                a = 1
            # ADD local field: 003, 533, 730, 949
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a','*b3=z;bn=buint;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','uint', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-T&F-CRC'))
            rec.add_ordered_field(Field(tag = '533', indicators = ['\\', '\\'], subfields = ['a', 'Electronic reproduction.']))
            rec.add_ordered_field(Field(tag = '506', indicators = ['\\', '\\'], subfields = ['a', 'Made available through Taylor & Francis. Access restricted to users at licensed institutions']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a','Taylor & Francis (CRC Press).', '5', 'OCU']))
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)
            rec = self.utilities.Standardize856_956(rec, 'Taylor & Francis')
            #rec = self.utilities.DedupRecords(x)

        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_SPRebk(self, x, name='ER-O/L-SPRebk'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-SPRebk'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-SPRebk'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'SpringerLink']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'Springer ebooks.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)

        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_Safari(self, x, name='ER-O/L-Safari'):
        recs = self.utilities.BreakMARCFile(x)
        regexes = [
            re.compile(r'.*EBSCOhost.*\n'),
            re.compile(r'.*OhioLINK.*'),
            re.compile(r'.*SpringerLink.*\n'),
            re.compile(r'.*Wiley.*\n'),
        ]

        for rec in recs:
            for field in rec:
                if field.tag == '856':
                    #if any of the 856 fields match any of the above regex patterns, delete the whole field`
                    if any(regex.match(field.value()) for regex in regexes):
                        rec.remove_field(field)

            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'],subfields = ['l','olink', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'],subfields = ['a','*b3=z;bn=bolin;']))
            rec.add_ordered_field(Field(tag = '730', indicators =['0','\\'],subfields = ['a','Safari books online.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '003',data = 'ER-O/L-Safari'))
            rec.add_ordered_field(Field(tag = '002',data = 'O/L-Safari'))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)

        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_OSO(self, x, name='ER-O/L-OSO'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-OSO'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-OSO'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'Oxford scholarship online.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)

        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_ACLS(self, x, name='ER-O/L-ACLS'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-ACLS'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-ACLS'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'History E-Book project']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'ACLS History E-Books.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)
        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_Wiley(self, x, name='ER-O/L-Wiley-InterSci'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-Wiley-InterSci'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-Wiley-InterSci'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'Wiley InterScience ebooks']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'Wiley online library.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)

        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_UPSO(self, x, name='ER-O/L-UPSO'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-UPSO'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-UPSO'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'University Press Scholarship Online.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)

        x = self.utilities.CreateMRC(recs)
        return x


    def ER_OL_APA_BOOKS(self, x, name='ER-O/L-APA Books'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
        ##### Keep everything above this comment ########
        ##### Make changes to each record below ########
            rec.add_ordered_field(Field(tag = '002', data = 'O/L-APA Books'))
            rec.add_ordered_field(Field(tag = '003', data = 'ER-O/L-APA Books'))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0', '\\'], subfields = ['a', 'APA Books.', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'], subfields = ['a', '*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'], subfields = ['l','olink', 'r', 's', 't', '99']))
            ###### Keep everything below this ########
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.AddEresourceGMD(rec)
        x = self.utilities.CreateMRC(recs)
        return x

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
            try:
                rec['530']['a'] = 'Print version available to institutional subscribers.'
            except:
                rec.add_ordered_field(Field(tag = '530', indicators =['\\','\\'],subfields = ['a','Print version available to institutional subscribers.']))
            # 490 and 830 fields lack ISBD punctuation, supply where lacking
            #x = re.sub('(?m)^(=490.*)[^ ;](\$v.*)', '\\1 ;\\2', x)
            try:
                four90a = rec['490']['a'] + ' ;'
                rec['490']['a'] = four90a
            except:
                rec.add_ordered_field(Field(tag = '490', indicators =['\\','\\'],subfields = ['a',' : ']))
            try:
                eight30a = rec['830']['a'] + ' ;'
                rec['830']['a'] = eight30a
            except:
                rec.add_ordered_field(Field(tag = '830', indicators =['\\','\\'],subfields = ['a',' : ']))
            # delete supplied 690 fields
            try:
                rec.remove_field(rec.get_fields('690')[0])
            except:
                pass
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec, 'NBER')
            rec = self.utilities.AddEresourceGMD(rec)
        x = self.utilities.CreateMRC(recs)
        return x


    def ER_OL_Safari(self, x, name='ER-O/L-Safari'):
        recs = self.utilities.BreakMARCFile(x)
        regexes = [
            re.compile(r'.*EBSCOhost.*\n'),
            re.compile(r'.*OhioLINK.*'),
            re.compile(r'.*SpringerLink.*\n'),
            re.compile(r'.*Wiley.*\n'),
        ]

        for rec in recs:
            for field in rec:
                if field.tag == '856':
                    #if any of the 856 fields match any of the above regex patterns, delete the whole field`
                    if any(regex.match(field.value()) for regex in regexes):
                        rec.remove_field(field)
                    #rename any 856$3 from Safari Books Online to Safari (ProQuest) :
                    if field['3'] == 'Safari Books Online':
                        field['3'] = 'Safari (ProQuest) :'
                    #edit proxy URLs
                    old_z = field['z']
                    old_z = re.sub('Connect to resource', 'Connect to resource online', old_z)
                    #old_z = re.sub('\(off-campus access\)', '(Off Campus Access)', old_z)
                    old_z = re.sub('\(off-campus\)', '(Off Campus Access)', old_z)
                    #old_z = re.sub('Connect to this resource online', 'Connect to resource online', old_z)
                    #old_z = re.sub('\(off-campus access\)', '(Off Campus Access)', old_z)
                    #old_z = re.sub('Connect to electronic resource', '$Connect to resource online', old_z)
                    field['z'] = old_z
                    #Change hyperlink tag from 856 to 956
                    #field.tag = '956'
            #Insert 002, 003, 730, 949 before supplied 008
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'],subfields = ['l','olink', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'],subfields = ['a','*b3=z;bn=bolin;']))
            rec.add_ordered_field(Field(tag = '730', indicators =['0','\\'],subfields = ['a','Safari books online.', '5', 'OCU']))
            #rec.remove_field(rec.get_fields('003')[0])
            rec.add_ordered_field(Field(tag = '003',data = 'ER-O/L-Safari'))
            rec.add_ordered_field(Field(tag = '002',data = 'O/L-Safari'))
            #rec = self.utilities.Standardize856_956(rec, )
            rec = self.utilities.AddEresourceGMD(rec)
            rec = self.utilities.DeleteLocGov(rec)
        x = self.utilities.CreateMRC(recs)
        return x

    def ER_OL_Sage_eRef(self, x, name='ER-O/L-Sage-eRef'):
        recs = self.utilities.BreakMARCFile(x)
        for rec in recs:
            #Insert 002, 003, 730, 949 before supplied 003
            rec.add_ordered_field(Field(tag = '002',data = 'O/L-Sage-eRef'))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '1'],subfields = ['l','olink', 'r', 's', 't', '99']))
            rec.add_ordered_field(Field(tag = '949', indicators = ['\\', '\\'],subfields = ['a','*bn=bolin;']))
            rec.add_ordered_field(Field(tag = '730', indicators = ['0','\\'],subfields = ['a','Sage eReference..', '5', 'OCU']))
            rec.add_ordered_field(Field(tag = '003',data = 'ER-O/L-Sage-eRef'))
            rec.add_ordered_field(Field(tag = '002',data = 'O/L-Sage-eRef'))
            rec = self.utilities.AddEresourceGMD(rec)
            rec = self.utilities.DeleteLocGov(rec)
            rec = self.utilities.Standardize856_956(rec, 'SAGE Reference Online')
        x = self.utilities.CreateMRC(recs)
        return x
