import re
import db
from pprint import pprint

regexes = {
    'AGPLv3': ["""GNU AFFERO GENERAL PUBLIC LICENSE.*Version 3""", """AGPL"""],
    'GPLv1': ["""GNU GENERAL PUBLIC LICENSE.*Version 1""", """GPL[ ]*v1"""],
    'GPLv2': ["""GNU GENERAL PUBLIC LICENSE.*Version 2""", """GPL[ ]*v2""", """GPL 2""", """Gnu Public license version 2"""],
    'GPLv3': ["""GNU GENERAL PUBLIC LICENSE.*Version 3""", """GPL[ ]*v3""", """GPL(,)? version 3""", """version 3 of the GNU General Public License""", """General Public License v3""", """GPL"""],
    'AcademicFreeLicense': ["""The Academic Free License""", """This Academic Free License (the "License") applies to any original work of authorship (the "Original Work") whose owner (the "Licensor") has placed the following notice immediately following the copyright notice for the Original Work:"""],
    'Apachev2': ["""Apache License.*(Version)? 2\.0""", """http://www\.apache\.org/licenses/LICENSE-2\.0""", """Apache 2\.0 Software License""", """Apache License"""],
    'BSD': ["""BSD License""", """Redistribution and use (of this software )?in source and binary forms, with or without modification, are permitted provided that the following conditions are met:""", """Redistribution and use in source and binary forms of the software as well as documentation, with or without modification, are permitted provided that the following conditions are met""", """BSD"""],
    'MIT': ["""MIT License""", """Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files \(.+\), to deal (in|with) the Software without restriction( except as noted below)?, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicen[sc]e, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:""", """Permission to use, copy, modify, and distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies\.""", """MIT"""],
    'FDL': ["""GNU Free Documentation License"""],
    'Ruby': ["""Ruby License""", """You may make and give away verbatim copies of the source form of (this|the) software without restriction, provided that you (retain|duplicate) ALL of the original copyright notices and associated disclaimers\.""", """same terms as Ruby""", """http://www\.ruby-lang\.org/en/LICENSE\.txt""", """same as Ruby"""],
    'ArtisticLicense': ["""The Artistic License""", """This license establishes the terms under which a given free software Package may be copied, modified, distributed, and/or redistributed\. The intent is that the Copyright Holder maintains some artistic control over the development of that Package while still keeping the Package available as open source and free software\."""],
    'ISC': ["""Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies\."""],
    'PHP': ["""The PHP License"""],
    'CCPL': ["""THE WORK \(AS DEFINED BELOW\) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE COMMONS PUBLIC LICENSE \("CCPL" OR "LICENSE"\)\. THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW\. ANY USE OF THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED\."""],
    'Unlicense': ["""This is free and unencumbered software released into the public domain"""],
    'MPL': ["""MOZILLA PUBLIC LICENSE""", """MPL"""],
    'EPL': ["""Eclipse Public License"""],
    'DontBeADick': ["""DON'T BE A DICK PUBLIC LICENSE""", """Do whatever you like with the original work, just don't be a dick\.""", """Everyone is permitted to copy and distribute verbatim or modified copies of this license document, and changing it is allowed as long as the name is changed"""],
    'OSL': ["""Open Software License"""],
    'CDDL': ["""COMMON DEVELOPMENT AND DISTRIBUTION LICENSE"""],
    'CCAttribution': ["""Creative Commons Attribution""", """http://creativecommons\.org/licenses/by/3\.0/"""],
    'CCAttributionNonCommercialShareAlike': ["""http://creativecommons\.org/licenses/by-nc-sa/3\.0"""],
    'CCAttributionShareAlike': ["""http://creativecommons\.org/licenses/by-sa/3\.0"""],
    'PublicDomain': ["""http://creativecommons\.org/licenses/publicdomain/""", """Public Domain""", """http://creativecommons\.org/publicdomain/"""],
    'LGPL': ["""LGPL""", """GNU Lesser General Public License"""],
    'Perl': ["""under the same terms as Perl itself"""],
    'CPL': ["""COMMON PUBLIC LICENSE"""],
    'ACM': ["""ACM Software License Agreement"""],
    'LiberalFreeware': ["""LIBERAL FREEWARE LICENSE"""],
    'Dojo': ["""Dojo License"""],
    'Erlang': ["""http://erlang\.org/EPLICENSE"""],
    'BeerWare': ["""THE BEER-WARE LICENSE"""],
    'Boost': ["""http://www\.boost\.org/LICENSE_1_0\.txt""", """Boost license"""]
}

patterns = {}

for key in regexes:
    patterns[key] = []
    for regex in regexes[key]:
        newregex = re.sub(' ', '[\s\*/#]+', regex)
        patterns[key].append(re.compile(newregex, re.IGNORECASE | re.DOTALL))


def getLicenseType(license):
    bestmatch = None
    for licenseType in patterns:
        for pattern in patterns[licenseType]:
            match = pattern.search(license)
            if match:
                if bestmatch == None or match.start(0) < bestmatch['start']:
                    bestmatch = {'type': licenseType, 'start': match.start(0)}
    if not bestmatch == None:
        return bestmatch['type']
    return None


def updateLicenseTypes():
    rows = db.getLicenses()
    for row in rows:

        rowid = row[0]
        license = row[1]
        print 'Updating id=%d' % rowid
        licenseType = getLicenseType(license)
        db.updateType(rowid, licenseType)
