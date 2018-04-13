import inspect, re, subprocess
from pymarc import Record, Field, MARCReader, MARCWriter, marcxml
from io import BytesIO

class utilityFunctions:

    def listChangeScripts(self, BatchEdits):
        num = 0
        ChangeScriptsDict = {}
        #pdb.set_trace()
        for i in dir(BatchEdits)[:-26]:
            num = num + 1
            ChangeScriptsDict[num] = [i,''.join(inspect.getargspec(getattr(BatchEdits, i))[3])]
        print(ChangeScriptsDict)
        for key in ChangeScriptsDict.keys():
            print(str(key) + ': ' + ChangeScriptsDict[key][0])
        return ChangeScriptsDict

    def ScriptSelect(self, ChangeScriptsDict):#options list
        NumberOfOptions = len(ChangeScriptsDict)
        def ScriptSelectValidate(low, high):
            prompt = '\nSelect number for desired process: '
            while True:
                try:
                    a = int(input(prompt))
                    if low <= a <= high:
                        return a
                    else:
                        print('\nPlease select a number between %d and %d!\a ' % (low, high))
                except ValueError:
                    print('\nPlease select a number between %d and %d!\a ' % (low, high))
            return
        x = ScriptSelectValidate(1, NumberOfOptions)
        verify = input('\nYou have selected:\n\n\t ' + ChangeScriptsDict[x][1] + '\n\nConfirm (y/n): ')
        while verify != 'y':
            while verify != 'y' and verify != 'n':
                verify = input('Please type \'y\' or \'n\'')
            if verify == 'y':
                pass
            else:
                x = ScriptSelectValidate(1, NumberOfOptions)
                verify = input('\nYou have selected:\n\n\t' + str(x) + '. ' + ChangeScriptsDict[x][1] + '\n\nConfirm (y/n): ')
        return x

    def MarcEditXmlToMarc(self, x):
        mrcFileName = re.sub('.xml', '.mrc', x)
        print('\n<Converting from XML to MARC>\n')
        #subprocess.call([MonoBin,MarcEditBin,"-s", x, "-d",mrcFileName,"-xmlmarc","-marc8", "-mxslt","/opt/marcedit/xslt/MARC21XML2Mnemonic_plugin.xsl"])
        marcStr = ''
        with open(x, 'rb') as fh:
            recs = marcxml.parse_xml_to_array(fh)
            for rec in recs:
                marcStr += str(rec)

        return marcStr

    def BreakMARCFileBACKUP(self, x):
        #break the file; output .mrk
        #mrkFileName = re.sub('.mrc', '.mrk', x)
        print("\n<Breaking MARC file>\n")
        #marcedit process
        #subprocess.call([MonoBin,MarcEditBin,"-s", x, "-d", mrkFileName,"-break"])
        with open(x, 'rb') as fh:
            reader = MARCReader(fh)
            x = ''
            for rec in reader:
                x += str(rec) + '\n'
        #marcedit process
        #x = open(mrkFileName).read()
        return x


    def BreakMARCFile(self, x):
        #break the file into a list of Record objects;
        #mrkFileName = re.sub('.mrc', '.mrk', x)
        print("\n<Breaking MARC file>\n")
        records = []
        with open(x, 'rb') as fh:
            reader = MARCReader(fh)
            for rec in reader:
                records.append(rec)
        return records

    def DeleteLocGov(self, rec):
        regexes = [
            re.compile(r'.*www.loc.gov.*\n'),
            re.compile(r'.*www.e-streams.com.*\n'),
            re.compile(r'.*Book review (E-STREAMS).*\n'),
            re.compile(r'.*catdir.loc.gov.*\n'),
            re.compile(r'.*books.google.com.*\n'),
            re.compile(r'.*cover image.*\n'),
            re.compile(r'.*http://d-nb.info.*\n'),
            re.compile(r'.*http://deposit.d-nb.de/cgi-bin.*\n'),
        ]
        #if an 856 field is present, check it against the above patterns.
        # if found, delete the field
        if rec['856'] is not None:
            url = rec['856']['u']
            if any(regex.match(url) for regex in regexes):
                rec.remove_field(rec.get_fields('856')[0])
        return rec

    def CleanURL(self,url):
        #delete all occurrences of $2
        url.delete_subfield('2')
        #delete all $z
        url.delete_subfield('z')
        #add standard $z
        url.add_subfield('z', 'Connect to resource online')
        #delete all $q
        url.delete_subfield('q')
        #delete all $y
        url.delete_subfield('y')
        #move leading $3 to EOF
        #
        return url

    def Standardize856_956(self, *args):
        rec = args[0]
        if rec['856'] is not None:
            field856 = rec['856']
            if rec['856'].indicator1 != '4':
                print('Found URL field with unexpected indicator')
            self.CleanURL(field856)
            if len(args) > 1 and type(args[1]) == str:
                rec['856'].add_subfield('3', args[1])

        if rec['956'] is not None:
            field956 = rec['956']
            if rec['956'].indicator1 != '4':
                print('Found URL field with unexpected indicator')
            self.CleanURL(field956)
            if len(args) > 1 and type(args[1]) == str:
                rec['956'].add_subfield('3', args[1])

        return rec

    def Standardize856_956_BAK(self, *args):
        rec = args[0]
        output = []
        #Check 8/956 indicator 1 code for non http URL
        if rec['856'] is not None:
            field856 = rec['856'].value()
            print(field856)
        if rec['956'] is not None:
            field956 = rec['956'].value()
            print(field956)
        URLFieldInd1 = re.findall('=[8|9]56  [^4]..*', args[0])
        #if found, interrupt script with alert
        if URLFieldInd1:
            print('\a\a\nFound URL fields(s) with unexpected indicator:\n')
            for URLField in URLFieldInd1:
                print('\t' + URLField)
            raw_input('\nPress <ENTER> to continue\n')
        #split file into list of lines
        x = args[0].split('\n')
        for line in x:
            match = re.search('=[8|9]56  ..', line)
            if match:
                #delete all occurance of $2
                line = re.sub('\$2http[^\$]*', '', line)
                #delete all $z
                line = re.sub('\$z[^\$]*', '', line)
                #delete all occurance of $q
                line = re.sub('\$q[^\$]*', '', line)
                #delete all occurance of $y
                line = re.sub('\$y[^\$]*', '', line)
                #move leading $3 to EOF
                line = re.sub('(=[8|9]56  ..)(\$3.*?)(\$u.*)', '\\1\\3\\2', line)
                if len(args) > 1 and type(args[1]) == str:
                    if re.search('\$3', line):
                        line = re.sub('(\$3)(.*)', '\\1{0} (\\2)'.format(args[1]), line)
                    else:
                        line = line + '$3{0} :'.format(args[1])
                #add standard $z
                line = line + '$zConnect to resource online'
                output.append(line)
            else:
                output.append(line)
        x = '\n'.join(output)
        return x

    def CharRefTrans(self, rec):#Character reference translation table
        CharRefTransTable = {
            #Hex char refs
            '&#039;' : ['&#039;', '\"'],
            '&#146;' : ['&#146;', '\''],
            '&#160;' : ['&#160;', '  '],
            '&#160;' : ['&#160;', '{A0}'],
            '&#161;' : ['&#161;', '{iexcl}'],
            '&#163;' : ['&#163;', '{pound}'],
            '&#168;' : ['&#168;', '{uml}'],
            '&#169;' : ['&#169;', '{copy}'],
            '&#174;' : ['&#174;', '{reg}'],
            '&#176;' : ['&#176;', '{deg}'],
            '&#177;' : ['&#177;', '{plusmin}'],
            '&#181;' : ['&#181;', '[micro]'],
            '&#192;' : ['&#192;', '{grave}A'],
            '&#193;' : ['&#193;', '{acute}A'],
            '&#194;' : ['&#194;', '{circ}A'],
            '&#195;' : ['&#195;', '{tilde}A'],
            '&#196;' : ['&#196;', '{uml}A'],
            '&#197;' : ['&#197;', '{ring}A'],
            '&#198;' : ['&#198;', '{AElig}'],
            '&#199;' : ['&#199;', '{cedil}C'],
            '&#200;' : ['&#200;', '{grave}E'],
            '&#201;' : ['&#201;', '{acute}E'],
            '&#202;' : ['&#202;', '{circ}E'],
            '&#203;' : ['&#203;', '{uml}E'],
            '&#204;' : ['&#204;', '{grave}I'],
            '&#205;' : ['&#205;', '{acute}I'],
            '&#206;' : ['&#206;', '{circ}I'],
            '&#207;' : ['&#207;', '{uml}I'],
            '&#209;' : ['&#209;', '{tilde}N'],
            '&#210;' : ['&#210;', '{grave}O'],
            '&#211;' : ['&#211;', '{acute}O'],
            '&#212;' : ['&#212;', '{circ}O'],
            '&#213;' : ['&#213;', '{tilde}O'],
            '&#214;' : ['&#214;', '{uml}O'],
            '&#217;' : ['&#217;', '{grave}U'],
            '&#218;' : ['&#218;', '{acute}U'],
            '&#219;' : ['&#219;', '{circ}U'],
            '&#220;' : ['&#220;', '{uml}U'],
            '&#221;' : ['&#221;', '{acute}Y'],
            '&#222;' : ['&#222;', '{THORN}'],
            '&#224;' : ['&#224;', '{grave}a'],
            '&#225;' : ['&#225;', '{acute}a'],
            '&#226;' : ['&#226;', '{circ}a'],
            '&#227;' : ['&#227;', '{tilde}a'],
            '&#228;' : ['&#228;', '{uml}a'],
            '&#229;' : ['&#229;', '{ring}a'],
            '&#230;' : ['&#230;', '{aelig}'],
            '&#231;' : ['&#231;', '{cedil}c'],
            '&#232;' : ['&#232;', '{grave}e'],
            '&#233;' : ['&#233;', '{acute}e'],
            '&#234;' : ['&#234;', '{circ}e'],
            '&#235;' : ['&#235;', '{uml}e'],
            '&#236;' : ['&#236;', '{grave}i'],
            '&#237;' : ['&#237;', '{acute}i'],
            '&#238;' : ['&#238;', '{circ}i'],
            '&#239;' : ['&#239;', '{uml}i'],
            '&#240;' : ['&#240;', '{eth}'],
            '&#241;' : ['&#241;', '{tilde}n'],
            '&#242;' : ['&#242;', '{grave}o'],
            '&#243;' : ['&#243;', '{acute}o'],
            '&#244;' : ['&#244;', '{circ}o'],
            '&#245;' : ['&#245;', '{tilde}o'],
            '&#246;' : ['&#246;', '{uml}o'],
            '&#247;' : ['&#247;', '/'],
            '&#xf7;' : ['&#xF7;', '/'],
            '&#249;' : ['&#249;', '{grave}u'],
            '&#250;' : ['&#250;', '{acute}u'],
            '&#251;' : ['&#251;', '{circ}u'],
            '&#252;' : ['&#252;', '{uml}u'],
            '&#253;' : ['&#253;', '{acute}y'],
            '&#254;' : ['&#254;', '{thorn}'],
            '&#255;' : ['&#255;', '{uml}y'],
            '&#268;' : ['&#268;', '{caron}C'],
            '&#269;' : ['&#269;', '{caron}c'],
            '&#x2BC;' : ['&#x2BC;', '\''],
            '&#345;' : ['&#345;', '{caron}r'],
            '&#34;' : ['&#34;', '\"'],
            '&#38;' : ['&#38;', '&'],
            '&#39;' : ['&#39;', '\''],
            '&#60;' : ['&#60;', '<'],
            '&#62;' : ['&#62;', '>'],
            '&#64257;' : ['&#64257;', 'fi'],
            '&#8194;' : ['&#8194;', ''],#em space
            '&#8195;' : ['&#8195;', '  '],
            '&#8203;' : ['&#8203;', ''],#zero width letter spacing
            '&#8209;' : ['&#8209;', '-', '-'],
            '&#8211;' : ['&#8211;', '-'],
            '&#8212;' : ['&#8212;', '--'],
            '&#8213;' : ['&#8213;', '--'],
            '&#8216;' : ['&#8216;', '\''],
            '&#8217;' : ['&#8217;', '\''],
            '&#8220;' : ['&#8220;', '\"'],
            '&#8221;' : ['&#8221;', '\"'],
            '&#8223;' : ['&#8223;', '\"', '\"'],
            '&#8226;' : ['&#8226;', '{middot}'],
            '&#8234;' : ['&#8234;', ''],#unicode control character
            '&#8242;' : ['&#8242;', '\''],#prime
            '&#8482;' : ['&#8482;', '[TM]'],
            '&#8486;' : ['&#8486;', '[Ohm]'],
            '&#8722;' : ['&#8722;', '-'],
            '&#8804;' : ['&#8804;', '<=', '<='],
            '&#8805;' : ['&#8805;', '>=', '>='],
            '&#913;' : ['&#913;', '[Alpha]'],
            '&#914;' : ['&#914;', '[Beta]'],
            '&#915;' : ['&#915;', '[Gamma]'],
            '&#916;' : ['&#916;', '[Delta]'],
            '&#917;' : ['&#917;', '[Epsilon]'],
            '&#918;' : ['&#918;', '[Zeta]'],
            '&#919;' : ['&#919;', '[Eta]'],
            '&#920;' : ['&#920;', '[Theta]'],
            '&#921;' : ['&#921;', '[Iota]'],
            '&#922;' : ['&#922;', '[Kappa]'],
            '&#923;' : ['&#923;', '[Lambda]'],
            '&#924;' : ['&#924;', '[Mu]'],
            '&#925;' : ['&#925;', '[Nu]'],
            '&#926;' : ['&#926;', '[Xi]'],
            '&#927;' : ['&#927;', '[Omicron]'],
            '&#928;' : ['&#928;', '[Pi]'],
            '&#929;' : ['&#929;', '[Rho]'],
            '&#931;' : ['&#931;', '[Sigma]'],
            '&#932;' : ['&#932;', '[Tau]'],
            '&#933;' : ['&#933;', '[Upsilon]'],
            '&#934;' : ['&#934;', '[Phi]'],
            '&#935;' : ['&#935;', '[Chi]'],
            '&#936;' : ['&#936;', '[Psi]'],
            '&#937;' : ['&#937;', '[Omega]'],
            '&#945;' : ['&#945;', '[alpha]'],
            '&#946;' : ['&#946;', '[beta]'],
            '&#947;' : ['&#947;', '[gamma]'],
            '&#948;' : ['&#948;', '[delta]'],
            '&#949;' : ['&#949;', '[epsilon]'],
            '&#950;' : ['&#950;', '[zeta]'],
            '&#951;' : ['&#951;', '[eta]'],
            '&#952;' : ['&#952;', '[theta]'],
            '&#953;' : ['&#953;', '[iota]'],
            '&#954;' : ['&#954;', '[kappa]'],
            '&#955;' : ['&#955;', '[lambda]'],
            '&#956;' : ['&#956;', '[mu]'],
            '&#957;' : ['&#957;', '[nu]'],
            '&#958;' : ['&#958;', '[xi]'],
            '&#959;' : ['&#959;', '[omicron]'],
            '&#960;' : ['&#960;', '[pi]'],
            '&#964;' : ['&#964;', '[tau]'],
            '&#965;' : ['&#965;', '[upsilon]'],
            '&#966;' : ['&#966;', '[phi]'],
            '&#967;' : ['&#967;', '[chi]'],
            '&#968;' : ['&#968;', '[psi]'],
            '&#969;' : ['&#969;', '[omega]'],
            '&#xAD;' : ['&#xAD;', '-'],
            '&#x0027;' : ['&#x0027;', '\''],
            '&#x0101;' : ['&#x0101;', '{macr}a', '{229}a'],
            '&#x142;' : ['&#x142;', '{lstrok}', '{177}'],
            '&#x153;' : ['&#x153;', '{oelig}', '{182}'],
            '&#x201A;' : ['&#x201A;', ','],
            '&#x2013;' : ['&#x2013;', '-'],
            '&#x2014;' : ['&#x2014;', '--'],
            '&#x2018;' : ['&#x2018;', '\''],
            '&#x2019;' : ['&#x2019;', '\''],
            '&#x2020;' : ['&#x2020;', ''],
            '&#x201E;' : ['&#x201E;', '\"', '\"'],
            '&#x2022;' : ['&#x2022;', '{middot}', '{168}'],
            '&#x2044;' : ['&#x2044;', '/', '{168}'],
            '&#x2039;' : ['&#x2039;', '\'', '\''],
            '&#x203A;' : ['&#x203A;', '\'', '\''],
            '&#x2b9;' : ['&#x2b9;', '\'', '\''],
            '&#x2bb;' : ['&#x2bb;', '\'', '\''],
            '&#x2bb;' : ['&#x2bc;', '\'', '\''],
            '&#x300;' : ['&#x300;', '{grave}', '{225}'],
            '&#x301;' : ['&#x301;', '{acute}', '{226}'],
            '&#x302;' : ['&#x302;', '{circ}', '{227}'],
            '&#x303;' : ['&#x303;', '{tilde}', '{228}'],
            '&#x304;' : ['&#x304;', '{macr}', '{229}'],
            '&#x306;' : ['&#x306;', '{breve}', '{230}'],
            '&#x307;' : ['&#x307;', '{dot}', '{231}'],
            '&#x308;' : ['&#x308;', '{uml}', '{232}'],
            '&#x30c;' : ['&#x30c;', '{caron}', '{233}'],
            '&#x323;' : ['&#x323;', '{dotb}', '{242}'],
            '&#x326;' : ['&#x326;', '{commab}', ','],
            '&#x327;' : ['&#x327;', '{cedil}', '{240}'],
            '&#x328;' : ['&#x328;', '{ogon}', '{241}'],
            '&#x81;' : ['&#x81;', '', ''],#control char
            '&#xA6;' : ['&#xA6;', '[broken bar]', '[broken bar]'],
            '&#xe6;' : ['&#xe6;', '{aelig}', '{181}'],
            '&#xfe20;' : ['&#xfe20;', '{llig}', '{235}'],
            '&#xfe21;' : ['&#xfe21;', '{rlig}', '{236}'],
            '&Delta;' : ['&Delta;', '[Delta]', '[Delta]'],
            '&Lambda;' : ['&Lambda;', '[Lambda]', '[Lambda]'],
            '&Prime;' : ['&Prime;', '\'', '\''],
            '&aacute;' : ['&aacute;', '{acute}a', '{226}a'],
            '&acirc;' : ['&acirc;', '{circ}a', '{227}a'],
            '&acute;' : ['&acute;', '{acute}', '{226}'],
            '&aelig;' : ['&aelig;', '{aelig}', '{181}'],
            '&agr;' : ['&agr;', '[alpha]', '[alpha]'],
            '&alpha;' : ['&alpha;', '[alpha]', '[alpha]'],
            '&amp;' : ['&amp;', '&', '&'],
            '&ap;' : ['&ap;', '[almost equal to]', '[almost equal to]'],
            '&aring;' : ['&aring;', '{ring}a', '{234}a'],
            '&Aring;' : ['&Aring;', '{ring}A', '{234}A'],
            '&ast;' : ['&ast;', '*', '*'],
            '&auml;' : ['&auml;', '{uml}', '{232}'],
            '&bull;' : ['&bull;', '{middot}', '{168}'],
            '&cacute;' : ['&cacute;', '{acute}c', '{226}c'],
            '&ccaron;' : ['&ccaron;', '{caron}', '{233}'],
            '&ccedil;' : ['&ccedil;', '{cedil}c', '{240}c'],
            '&circ;' : ['&circ;', '{circ}', '{227}'],
            '&dashv;' : ['&dashv;', '[left tack]', '[left tack]'],
            '&dollar;' : ['&dollar;', '{dollar}', '$'],
            '&deg;' : ['&deg;', '{deg)', '{234}'],
            '&delta;' : ['&delta;', '[delta]', '[delta]'],
            '&eacute;' : ['&eacute;', '{acute}e', '{226}e'],
            '&egr;' : ['&egr;', '[epsilon]', '[epsilon]'],
            '&Egr;' : ['&Egr;', '[Epsilon]', '[Epsilon]'],
            '&esc;' : ['&esc;', '', ''],
            '&ge;' : ['&ge;', '>=', '>='],
            '&grave;' : ['&grave;', '{grave}', '{225}'],
            '&gt;' : ['&gt;', '>', '>'],
            '&hacek;' : ['&hacek;', '{caron}', '{233}'],
            '&hardsign;' : ['&hardsign;', '{hardsign}', '{183}'],
            '&iacute;' : ['&iacute;', '{acute}i', '{226}'],
            '&iexcl;' : ['&iexcl;', '{iexcl}', '{160}'],
            '&inches;' : ['&inches;', '\"', '\"'],
            '&kappa;' : ['&kappa;', '[kappa]', '[kappa]'],
            '&Lambda;' : ['&Lambda', '[Lambda]', '[Lambda]'],
            '&le;' : ['&le;', '<=', '<='],
            '&lt;' : ['&lt;', '<', '<'],
            '&macr;' : ['&macr;', '{macr}', '{macr}'],
            '&mdash;' : ['&mdash;', '--', '--'],
            '&mgr;' : ['&mgr;', '[Mu]', '[Mu]'],
            '&middot;' : ['&middot;', '{middot}', '{168}'],
            '&mllhring;' : ['&mllhring;', '{mlrhring}', '{174}'],
            '&mlrfring;' : ['&mlrfring;', '{mlrfring}', '{176}'],
            '&mu;' : ['&mu;', '[mu]', '[mu]'],
            '&nacute;' : ['&nacute;', '{acute}n', '{226}n'],
            '&nbsp;' : ['&nbsp;', ' ', ' '],
            '&ndash;' : ['&ndash;', '-', '-'],
            '&ne;' : ['&ne;', '[not equal]', '[not equal]'],
            '&ntilde;' : ['&ntilde;', '{tilde}n', '{228}n'],
            '&Ntilde;' : ['&Ntilde;', '{tilde}N', '{228}N'],
            '&oacute;' : ['&oacute;', '{acute}o', '{226}o'],
            '&ocirc;' : ['&ocirc;', '{circ}o', '{227}o'],
            '&oslash;' : ['&oslash;', '{Ostrok}', '{162}'],
            '&ouml;' : ['&ouml;', '{uml}o', '{232}o'],
            '&Ouml;' : ['&Ouml;', '{uml}O', '{232}O'],
            '&perp;' : ['&perp;', '[up tack]', '[up tack]'],
            '&phis;' : ['&phis;', '[phi]', '[phi]'],
            '&phiv;' : ['&phiv;', '[Phi]', '[Phi]'],
            '&pi;' : ['&pi;', '[pi]', '[pi]'],
            '&quot;' : ['&quot;', '\"', '\"'],
            '&radic;' : ['&radic;', '[check mark]', '[check mark]'],
            '&reg;' : ['&reg;', ' {reg}', '{170}'],
            '&ring;' : ['&ring;', '{ring}', '{234}'],
            '&scedil;' : ['&scedil;', '{cedil}s', '{240}s'],
            '&sect;' : ['&sect;', '[section]', '[section]'],
            '&shy' : ['&shy', '-', '-'],
            '&shy;' : ['&shy;', '-', '-'],
            '&sigma;' : ['&sigma;', '[sigma]', '[sigma]'],
            '&sim;' : ['&sim;', '[equivalent]', '[equivalent]'],
            '&softsign;' : ['&softsign;', '{softsign}', '{167}'],
            '&sol;' : ['&sol;', '/', '/'],
            '&square;' : ['&square;', '[square]', '{175}'],
            '&szlig;' : ['&szlig;', 'ss', 'ss'],
            '&thgr;' : ['&thgr;', '[theta]', '[theta]'],
            '&thinsp;' : ['&thinsp;', ' ', ' '],
            '&trade;' : ['&trade;', '[TM]', '[TM]'],
            '&uuml;' : ['&uuml;', '{uml}u', '{232}u'],
            '&zcaron;' : ['&zcaron;', '{caron}z', '{233}z'],
            }

        keys = list(dict.keys(CharRefTransTable))
        for key in range(len(keys)):
            for x in rec:
                x = re.sub(CharRefTransTable[keys[key]][0],CharRefTransTable[keys[key]][1], x.value())
            #Flag unknown Char Refs
            UnrecognizedCharRef = list(set(re.findall('&[\d|\w|#]*;', x)))
            if UnrecognizedCharRef:
                #sound bell
                print('\a\a\a\a\a\n<Found unrecognized characters>\n\n\t...generating error file\n')
                BoolUnrecognizedCharRef = 1
                CharRefIf = open(filename + '_UnrecognizedCharRef.txt', 'w')
                CharRefIf.write('Unrecognized character references\n')
                CharRefIf.write('\n'.join(UnrecognizedCharRef))
                CharRefIf.close()
        return rec


    def AddEresourceGMD(self, rec):
        if rec['245']['h'] is None:
            if rec['245']['b'] is not None:
                rec['245'].delete_subfield('b')
                rec['245'].add_subfield('h', '[electronic resource]')
            elif rec['245']['c'] is not None:
                rec['245'].delete_subfield('c')
                rec['245'].add_subfield('h', '[electronic resource]')
            else:
                rec['245'].add_subfield('h', '[electronic resource]')
        return rec

    # re-order 007 fields in a MARC record
    def order_007(self, rec):
        james_bond = []
        for field in rec:
            if field.tag == '007':
                james_bond.append(field.data)
                if len(james_bond) > 1:
                    rec.remove_fields('007')
                    james_bond.sort()
                    for f in james_bond:
                        rec.add_ordered_field(Field(tag = '007',data = f))
        return rec

    def SaveToMRK(self, recs, filename):
        filenameNoExt = re.sub('.\w*$', '', filename)
        outfile = open(filenameNoExt + '_OUT.mrk', 'w')
        for r in recs:
            outfile.write(str(r) + '\n')
        outfile.close()
        return recs

    def CreateMRK(self, recs):
        out_file = recs
        return out_file

    def MakeMARCFile(self, recs, filename):
        filenameNoExt = re.sub('.\w*$', '', filename)
        mrcFileName = filenameNoExt + '_OUT.mrc'
        print('\n<Compiling file to MARC>\n')
        writer = MARCWriter(open(mrcFileName, "wb"))
        for r in recs:
            try:
                writer.write(r.as_marc())
            except Exception as e:
                print(str(e) + ' error. Encoding: ' + str(r))
        writer.close()
        return recs

    def CreateMRC(self, recs):
        ### writing to memory (Python 3 only)
        memory = BytesIO()
        writer = MARCWriter(memory)
        for record in recs:
            writer.write(record)
        writer.close(close_fh=False)
        return memory
