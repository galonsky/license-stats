import re
import db
from pprint import pprint

regexes = {
    'AGPLv3': ["""GNU AFFERO GENERAL PUBLIC LICENSE.*Version 3"""],
    'GPLv1': ["""GNU GENERAL PUBLIC LICENSE.*Version 1"""],
    'GPLv2': ["""GNU GENERAL PUBLIC LICENSE.*Version 2"""],
    'GPLv3': ["""GNU GENERAL PUBLIC LICENSE.*Version 3"""],
    'AcademicFreeLicense': ["""The Academic Free License""", """This Academic Free License (the "License") applies to any original work of
authorship (the "Original Work") whose owner (the "Licensor") has placed the
following notice immediately following the copyright notice for the Original
Work:"""],
    'Apachev2': ["""Apache License.*Version 2\.0"""],
    'BSD': ["""BSD License""","""Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:.*"""],
    'MIT': ["""MIT License""","""Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files \(the "Software"\), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:"""],
    'FDL': ["""GNU Free Documentation License"""],
    'Ruby': ["""Ruby License""", """You may make and give away verbatim copies of the source form of this
    software without restriction, provided that you retain ALL of the
    original copyright notices and associated disclaimers."""],
    'ArtisticLicense': ["""The Artistic License""", """This license establishes the terms under which a given free software
Package may be copied, modified, distributed, and/or redistributed\.
The intent is that the Copyright Holder maintains some artistic
control over the development of that Package while still keeping the
Package available as open source and free software\."""]
}

patterns = {}

for key in regexes:
    patterns[key] = []
    for regex in regexes[key]:
        patterns[key].append(re.compile(regex, re.IGNORECASE))


def getLicenseType(license):
    for licenseType in patterns:
        for pattern in patterns[licenseType]:
            if pattern.search(license):
                return licenseType
    return None


def updateLicenseTypes():
    rows = db.getLicenses()
    for row in rows:

        rowid = row[0]
        license = row[1]
        print 'Updating id=%d' % rowid
        licenseType = getLicenseType(license)
        db.updateType(rowid, licenseType)
