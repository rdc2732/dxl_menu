# Import the os module, for the os.walk function
import os

# "C:\Program Files\IBM\Rational\DOORS\9.6\bin\doors.exe"
#   -d 36602@AZ18NT6012
#   -a \\az18nt6012\AERO\addins;\\az18nt6012\PhoenixAddins\Honeywell
#   -J \\az18nt6012\AERO\addins_project;\\az18nt6012\PhoenixAddins\Projects


def parseIndexFile(indexFile):
    lines = []
    f = open(indexFile)
    for line in f:
        line = line.strip()
        if len(line) > 0:
            if line.find('-----') != -1:
                lines.append(('', '---------------'))
            else:
                line = ' '.join(line.split('\t')) # replace tabs with spaces
                parts = line.rsplit('_', 1) # split on rightmost underscore, may be one or two
                menuDescription = parts[1].strip() # grab text for description from right side of underscore
                parts = parts[0].strip().rsplit(' ') # Get hotkey in last element of parts
                menuItem = ' '.join(parts[:-1]).strip() # grab text for item from first part of left side of underscore
                lines.append((menuItem, menuDescription))
    return(lines)


def processFolder(dirName, subDirList, fileList, dirLevel):
    baseFileName = dirName.rsplit('\\')[-1]
    indexFile = dirName + '\\' + baseFileName + '.idx'
    helpFile = dirName + '\\' + baseFileName + '.hlp'
    hasIndexFile = os.path.isfile(indexFile)
    hasHelpFile = os.path.isfile(helpFile)

    dxl_list = []  # Create initial list of dxls
    for fileName in fileList:
        if fileName.endswith('.dxl'):
            dxl_list.append(fileName)

    if hasIndexFile and hasHelpFile:
        print('\t' * dirLevel + baseFileName)
        items = parseIndexFile(indexFile)
        for item in items:  # returns a list of sets (menuItem, menuDescriptions)
            if item[0] in subdirList:
                # for dN, sdList, fL in os.walk(dirName + '\\' + item[0]):   <------------------ make this non-recursive.
                #     processFolder(dN, sdList, fL,  dirLevel + 1)
            else:
                print('\t' * (dirLevel + 1) + item[1])
            if item[1] in dxl_list:
                dxl_list.remove(item[1])
        for fileName in dxl_list:
            print('\t' * (dirLevel + 1) + fileName)
    return



# Starting with the current directory:
#   If there is a help and index file with the same name as the directory name,
#     Read the index file
#     For each valid line in the index file (contains format of a menu item)
#       If there is a dxl file in the current folder, or if there is a subfolder of the current
#         folder that matches the menuItem portion of the line, add to list of menu items to return.

# Set the directory you want to start from
#rootDirList = ['\\\\az18nt6012\\AERO\\addins_project','\\\\az18nt6012\\PhoenixAddins\Projects']
rootDirList = ['\\\\az18nt6012\\AERO\\addins_project']

for rootDir in rootDirList:
    for dirName, subdirList, fileList in os.walk(rootDir):
        processFolder(dirName, subdirList, fileList, 0)


