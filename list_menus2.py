# Import the os module, for the os.walk function
import os

# "C:\Program Files\IBM\Rational\DOORS\9.6\bin\doors.exe"
#   -d 36602@AZ18NT6012
#   -a \\az18nt6012\AERO\addins;\\az18nt6012\PhoenixAddins\Honeywell
#   -J \\az18nt6012\AERO\addins_project;\\az18nt6012\PhoenixAddins\Projects


# Function definitions
def test_menu_folder(folder_path):
    base_folder_name = folder_path.rsplit('\\')[-1]
    indexFile = folder_path + '\\' + base_folder_name + '.idx'
    helpFile = folder_path + '\\' + base_folder_name + '.hlp'
    hasIndexFile = os.path.isfile(indexFile)
    hasHelpFile = os.path.isfile(helpFile)

    return(hasIndexFile and hasHelpFile, indexFile)


def read_index_file(indexFile):
    print('index_file: ' + indexFile)
    menu_items = [] # will contain sets (menu_item, menu_description)
    f = open(indexFile)
    for line in f:
        line = line.strip()
        if len(line) > 0:
            if line.find('-----') != -1:
                menuItem = 'SEP'
                menuDescription = '---------------'
            else:
                line = ' '.join(line.split('\t'))  # replace tabs with spaces
                line = ' '.join(line.split()) # remove multiple spaces with one space
                parts = line.rsplit(' ')  # split on the single spaces
                if '_' in parts: # Normally there will be one or two.  We need to find it if one, the second if two
                    part_index = 0
                    counter = 0
                    for part in parts:
                        counter += 1
                        if part == '_':
                            part_index = counter
                    if part_index not in [1,2]:
                        menuItem = 'Error'
                        menuDescription = 'Error'
                    else:
                        menuItem = ' '.join(parts[:part_index])  # grab text from left side of underscore
                        menuDescription = ' '.join(parts[part_index:])  # grab text from right side of underscore
                else:
                    menuItem = 'Error'
                    menuDescription = 'Error'
            print('\t', menuItem, menuDescription)
            menu_items.append((menuItem, menuDescription))

    return(menu_items)


def menu_maker(folder_name, menu_data, menu_level):
    dxl_list = []  # Create initial list of dxls
    fileTest, indexFile = test_menu_folder(folder_name) # Check folder and get index file name
    if not fileTest: # process folder if it is a menu element
        return(menu_data)

    for dirName, subdirList, fileList in os.walk(folder_name): # use os.walk to get directory info
        break

    for fname in fileList:  # Build list of dxl files in current directory
        if fname.endswith('.dxl'):
            dxl_list.append(fname)

    for item in read_index_file(indexFile): # Build menu from .idx file
        if item[0] == 'SEP':
            menu_data.append((menu_level, '-----'))
        elif item[0] in subdirList:
            subdirPath = dirName + '\\' + item[0]
            menu_info = (menu_level, item[0])
            menu_data.append(menu_info)
            menu_maker(subdirPath, menu_data, menu_level + 1) # Recurse this function for next level menu
            subdirList.remove(item[0])
        elif item[0] in dxl_list:
            menu_info = (menu_level, item[1])
            menu_data.append(menu_info)
            dxl_list.remove(item[0] + '.dxl')

    for subdirName in subdirList: # Add any other dxl files in folder to menu
        subdirPath = folder_name + '\\' + subdirName
        menu_maker(subdirPath, menu_data, menu_level + 1)  # Recurse this function for next level menu

    for dxl_file in dxl_list: # Add any other dxl files in folder to menu
        menu_info = (menu_level, dxl_file)
        menu_data.append(menu_info)

    return(menu_data)


# Main program
# rootDirList = ['\\\\az18nt6012\\AERO\\addins_project','\\\\az18nt6012\\PhoenixAddins\Projects']
rootDirList = ['\\\\az18nt6012\\AERO\\addins_project']
menu = []
menu_level = 0

for rootDir in rootDirList:
    menu_maker(rootDir, menu, menu_level)
    for tabs, description in menu:
        continue
        print('\t'*tabs + description)
