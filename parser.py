# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/21/16.
parser service conf or process conf
"""


import re


class parser:
    pass

gCommentRegular = r"^[ \t]*#"
gSectionRegular = r'^[ \t]*\[(.+)\][ \t]*'
gKeyValueRegular = r'^[ \t]*([^ \t=]+)[ \t=]([^\t=\n]+)'
gKeyRegular = r'^[ \t]*([^ \t=\n]+)'

gCommentRegex = re.compile(gCommentRegular)
gSectionRegex = re.compile(gSectionRegular)
gKeyValueregex = re.compile(gKeyValueRegular)
gKeyRegex = re.compile(gKeyRegular)

# base class


class Type:
    Comment, Section, KeyValue, Key = ("comment", "section", "keyvalue", "key")


class Parser:
    # parse the line, first comment parse then section parse return the result

    def parseLine(self, line):
        tType = Type.Comment
        if gCommentRegex.match(line):
            return Type.Comment

        tType = Type.Section
        result = gSectionRegex.match(line)
        if result is None:
            tType = Type.KeyValue
            result = gKeyValueregex.match(line)
            if result is None:
                tType = Type.Key
                result = gKeyRegex.match(line)

        return tType, result.groups()
    pass


class confParser:
    pass

"""
[service]
key=value1,value2
or just
key1=value1
key2=value2
"""


class confParser(confParser):
    def parse(self, path):
        parser = Parser()
        service = {}
        section = ""
        with open(path) as f:
            service[section] = {}
            # no section just key value
            for line in f:
                cType, group = parser.parseLine(line)
                if cType == Type.Section:
                    section = group[0]
                    service[section] = {}
                elif cType == Type.KeyValue:
                    service[section][group[0]] = group[1]
                elif cType == Type.Key:
                    service[section][group[0]] = ""
        return service
        pass
    pass
