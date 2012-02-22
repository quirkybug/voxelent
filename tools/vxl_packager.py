import sys,string,traceback, os.path, subprocess, shutil



def pack(VOX_VERSION_NUMBER):

    print len(str(VOX_VERSION_NUMBER))
    
    print '-- START --'
    VERSION_TAG = "_v"+str(VOX_VERSION_NUMBER)
    SLUG = "c4n3l4"
    
    minify = False
    #Here is one of the beauties of this script: It does not matter how the files are organized into folders. This will always be the order. regardless.
    core = [
             'VXL',
             'Notifier', 
             'Math3D',
             'CameraState',   
             'Camera',
             'CameraManager',
             'CameraInteractor', 
             'ViewInteractor', 
             'TrackerInteractor', 
             'PickerInteractor',
             'Transforms',
             'DiffusiveProgram',
             'PhongProgram',
             'Program',
             'Renderer',
             'Model',  
             'Actor', 
             'Scene', 
             'Toys',
             'LookupTable', 
             'LookupTableManager', 
             'BoundingBox', 
             'Axis', 
             'Floor',
             'View', 
             'ModelManager', 
             'API', 
             'FrameAnimation'
    
    ]
    
    
    vox_files = [os.path.join(root,name)
                 for root, dirs, files in os.walk("..\\source")
                 for name in files
                 if name.endswith(".js")]
    
    for f in vox_files:
        head, tail =  os.path.split(f)
        tail = str.replace(tail,'.js','');
        head = str.replace(head,'\\','/')
        tdir = SLUG + '/' + head
        tdir = str.replace(tdir,'../','')
        
        if not os.path.exists(tdir):
                print "creating "+tdir
                os.makedirs(tdir)
        
        origin =  head + '/' + tail + '.js'
        target =  tdir + '/' + tail + VERSION_TAG + '.js'
        print "Packing " + origin + ' into ' + target
        if (minify):
            subprocess.call("java -jar yui.jar --type js --line-break 500  "+ origin + " -o "+target)
        else:
            shutil.copy(origin, target); #test
    
    print "Adding parts to lib"
    hashmap = {}
    for root, dirs, files in os.walk(SLUG+"/source"):
        for name in files:
    
            n = os.path.join(root,name)
            print 'opening '+ name
            try:
                f = open(n,'r')
                hashmap[name]= f.read()
            except IOError:
                    print 'error'
            finally:
                f.close()
    buffer = ''
    for lkp in core:
        key = lkp + VERSION_TAG + '.js'
        if key in hashmap:
            buffer += hashmap[key]
            print "Adding " + key + " to file"
            
    
    
    w3 = open('..\\demos\\lib\\voxelent'+VERSION_TAG+'.js','w');
    w4 = open('..\\library\\voxelent'+VERSION_TAG+'.js','w');
    
    w3.write(buffer);
    w4.write(buffer);
    
    
    w3.close();
    w4.close();
    print ' -- END --'
    
if __name__ == '__main__':
    pack(sys.argv[1])