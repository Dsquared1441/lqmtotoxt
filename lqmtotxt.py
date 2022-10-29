import os
import sys
import zipfile
import json


'''
    lqm_to_txt.py -- given a absolute path of a folder/file, it will convert .lqm to .txt file by extracting data
    python lqmtotxt <absolute path for folder containing .lqm files>
'''

good = 0

# converts a DirEntry object with filename ending in .lqm to a .txt file in a folder called conversions in the parent folder
def convertLQMToTXT(lqmfile, homefolder):
    global good
    print('Converting {}...'.format(lqmfile.name))
    print(homefolder)
    
    
    # get conversion folders ready
    destfolder = homefolder + '\\conversion'
    print(destfolder)    

    #parse file
    try:
        z = zipfile.ZipFile(lqmfile);
        z.extract('memoinfo.jlqm');
        memodata = open('memoinfo.jlqm')
        contents = memodata.read();
        memodata.close()
        os.remove(homefolder + '\\memoinfo.jlqm');
        del z
    
        # main data
        memoinfo = json.loads(contents)
        maindata = memoinfo['MemoObjectList'][0]['DescRaw'];
        name = destfolder + '\\' + lqmfile.name[:-3] + '.txt';
        text = open(name, 'w');
        text.write(maindata);
        text.close()
        good = good + 1;
    except:
        print('uh oh. Something happended during conversion, skipping and adding to error log')
        err = open('errors.txt', 'a+')
        print(lqmfile.name, file=err)
        err.close()
    

# parse command line arguments

arg = sys.argv[1];

if len(sys.argv) > 2:
    print('This only works on singular files with .lqm or folders with .lqm files in themselves.');


# if arg is folder, preform conversion on each file
if os.path.isdir(arg):
    print('Argument is a folder.')
    # make a conversion folder
    (folder, rest) = os.path.split(arg)
    os.chdir(folder);
    if not os.path.exists(folder+'\\conversion'):
        os.mkdir('conversion')
    
    # for each file in the target folder, convert it to a txt file
    allfiles = os.scandir(arg);
    allfiles = [f for f in allfiles]
    length = len(allfiles)
    for (i, file) in enumerate(allfiles):
        name = file.name;
        print('{} of {} in {}'.format(i, length, arg));
        if name[-4:] != '.lqm':
            continue
        else:
            convertLQMToTXT(file, folder)

    print('{} out of {} printed.'.format(good, length))
    
    
# else, if arg is file, convert file
elif os.path.isfile(arg):
    print('Argument is a file.')
    (folder, rests) = os.path.split(arg)
    os.chdir(folder);
    if not os.path.exists(folder+'\\conversion'):
        os.mkdir('conversion')
    
    # make a DirEntry out of the filename
    (home, name) = os.path.split(arg)
    file = None
    for f in os.scandir(home):
        if f.name == name:
            file = f
    
    convertLQMToTXT(f, folder)
    
# else, return 'Not valid file'
else:
    print('Invalid filename. Please enter an absolute pathname (C:/Users/user/...')
    
print('done. thank you for using me!')
