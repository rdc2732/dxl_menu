# Import the os module, for the os.walk function
import os

# "C:\Program Files\IBM\Rational\DOORS\9.6\bin\doors.exe"
#   -d 36602@AZ18NT6012
#   -a \\az18nt6012\AERO\addins;\\az18nt6012\PhoenixAddins\Honeywell
#   -J \\az18nt6012\AERO\addins_project;\\az18nt6012\PhoenixAddins\Projects

# Use SQL table to hold menu_items
#    id, parent_id, name, type, display

# parseIndexFile: reads an input file and returns a list of sets menu item and description

# 1) Find the underscore searching from the right
# 2) String to the right is the MenuDescription
# 3) Backup to a single character
# 4) String to the left is the MenuItem


def parseIndexFile(indexFile):
    lines = []
    f = open(indexFile)
    for line in f:
        line = line.strip()
        if len(line) > 0:
            if line.find('-----') != -1:
                pass
            else:
                line = ' '.join(line.split('\t')) # replace tabs with spaces
                line = line.rsplit('_', 1) # split on rightmost underscore, may be one or two
                print("<<" + line[0] + ">>")
                menuDescription = line[1].strip() # grab text for description from right side of underscore
                menuItem = line[0].strip().split()[0] # grab text for item from first part of left side of underscore
                lines.append((menuItem, menuDescription))
    return(lines)

















# # Set the directory you want to start from
# rootDir = '\\\\az18nt6012\\PhoenixAddins\Honeywell'
# rootLevel = len(rootDir.rsplit('\\'))
# for dirName, subdirList, fileList in os.walk(rootDir):
#     dirLevel = len(dirName.rsplit('\\')) - rootLevel
#     baseFileName = dirName.rsplit('\\')[-1]
#     indexFile = dirName + '\\' + baseFileName + '.idx'
#     helpFile  = dirName + '\\' + baseFileName + '.hlp'
#     if os.path.isfile(indexFile) and os.path.isfile(helpFile) and dirLevel > 0:
#         print(dirLevel, '\t' * dirLevel, f'{baseFileName}')

# Set the directory you want to start from
rootDir = '\\\\az18nt6012\\PhoenixAddins\Projects'
rootLevel = len(rootDir.rsplit('\\'))
for dirName, subdirList, fileList in os.walk(rootDir):
    dirLevel = len(dirName.rsplit('\\')) - rootLevel
    baseFileName = dirName.rsplit('\\')[-1]
    indexFile = dirName + '\\' + baseFileName + '.idx'
    helpFile  = dirName + '\\' + baseFileName + '.hlp'
    if os.path.isfile(indexFile) and os.path.isfile(helpFile) and dirLevel > 0:
        for item in parseIndexFile(indexFile):
            pass
            # print(item[0], ': ', item[1])
    print("==============")

