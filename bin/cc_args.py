#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

CONFIG_NAME = ".clang_complete"

def readConfiguration():
  try:
    f = open(CONFIG_NAME, "r")
  except IOError:
    return []

  result = []
  for line in f:
    if strippedLine := line.strip():
      result.append(strippedLine)
  f.close()
  return result

def writeConfiguration(lines):
  with open(CONFIG_NAME, "w") as f:
    f.writelines(lines)

def parseArguments(arguments):
  nextIsInclude = False
  nextIsDefine = False
  nextIsIncludeFile = False
  nextIsIsystem = False

  includes = []
  defines = []
  include_file = []
  options = []
  isystem = []

  for arg in arguments:
    if nextIsInclude:
      includes += [arg]
      nextIsInclude = False
    elif nextIsDefine:
      defines += [arg]
      nextIsDefine = False
    elif nextIsIncludeFile:
      include_file += [arg]
      nextIsIncludeFile = False
    elif nextIsIsystem:
      isystem += [arg]
      nextIsIsystem = False
    elif arg == "-I":
      nextIsInclude = True
    elif arg == "-D":
      nextIsDefine = True
    elif arg[:2] == "-I":
      includes += [arg[2:]]
    elif arg[:2] == "-D":
      defines += [arg[2:]]
    elif arg == "-include":
      nextIsIncludeFile = True
    elif arg == "-isystem":
      nextIsIsystem = True
    elif arg.startswith('-std='):
      options.append(arg)
    elif arg == '-ansi':
      options.append(arg)
    elif arg.startswith('-pedantic'):
      options.append(arg)
    elif arg.startswith('-W'):
      options.append(arg)

  result = list(map(lambda x: f"-I{x}", includes))
  result.extend(map(lambda x: f"-D{x}", defines))
  result.extend(map(lambda x: f"-include {x}", include_file))
  result.extend(map(lambda x: f"-isystem{x}", isystem))
  result.extend(options)

  return result

def mergeLists(base, new):
  result = list(base)
  for newLine in new:
    if newLine not in result:
      result.append(newLine)
  return result

configuration = readConfiguration()
args = parseArguments(sys.argv)
result = mergeLists(configuration, args)
writeConfiguration(map(lambda x: x + "\n", result))


import subprocess
proc = subprocess.Popen(sys.argv[1:])
ret = proc.wait()

if ret is None:
  sys.exit(1)
sys.exit(ret)

# vim: set ts=2 sts=2 sw=2 expandtab :
