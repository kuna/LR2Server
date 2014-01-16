from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.template import Context, loader

import lr2db
import lr2bms2music
import os
import copy
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
lr2db.loadDB(BASE_DIR + "\\..\\LR2files\\Database\\song.db")

import glob
import StringIO
import zipfile
import unicodedata

def main(request):
    # all db
    tpl = loader.get_template('index.html')

    ctx = Context({
        'songcnt': lr2db.songCnt,
        'dblist': lr2db.dbList.items(),
        'gradelist': lr2db.gradeList.items(),
        'relpath': "./",
        '0page_display': 'inline',
        'pager_display': 'none',
        'pager_next': '',
        'pager_prev': ''
    })
    return HttpResponse(tpl.render(ctx))

def page(request, index=0):
    tpl = loader.get_template('index.html')

    prevind = int(index)-1
    if (prevind < 0):
        prevind =0

    ctx = Context({
        'songcnt': lr2db.songCnt,
        'dblist': lr2db.dbList.items()[int(index)*100:int(index)*100+100],
        'gradelist': lr2db.gradeList.items(),
        'relpath': "../",
        '0page_display': 'none',
        'pager_display': 'inline',
        'pager_next': '../' + str(int(index)+1) + '/',
        'pager_prev': '../' + str(prevind) + '/'
    })
    return HttpResponse(tpl.render(ctx))

def score(request, user=""):
    # all db with Player status
    DBFILE = BASE_DIR + "\\..\\LR2files\\Database\\Score\\" + user + ".db"
    if (os.path.isfile(DBFILE)):
        tpl = loader.get_template('index.html')

        # pre-create list
        lr2db.loadScoreDB(DBFILE)
        dblst = copy.copy(lr2db.dbList.items())
        ndblst = []
        for i in range(0, len(dblst)-1):
            farg = []
            for bmsdata in dblst[i][1]:
                if (lr2db.scoreList.has_key(bmsdata[0])):
                    farg.append(bmsdata + lr2db.scoreList[ bmsdata[0] ])
                else:
                    farg.append(bmsdata)
            ndblst.append([dblst[i][0], farg])

        ctx = Context({
            'songcnt': lr2db.songCnt,
            'dblist': ndblst,
            'gradelist': lr2db.gradeList.items(),
            'relpath': "../../",
            '0page_display': 'none',
            'pager_display': 'none',
            'pager_next': '',
            'pager_prev': ''
        })
        return HttpResponse(tpl.render(ctx))
    else:
        return HttpResponse("no user named %s exists" % user)


def downloadMusic(request, index=""):
    filepath = ""

    for row in lr2db.dbList.items():
        for bmsfile in row[1]:
            if (bmsfile[0] == index):
                filepath = bmsfile[7]

    if (filepath == ""):
        return HttpResponse("wrong request")
    else:
        filename = BASE_DIR + "\\..\\" + filepath
        ret_file = lr2bms2music.encodeFile(filename)
        if (ret_file == "none"):
            HttpResponse("file encoding is not supported by some reason.")
        else:
            if (os.path.isfile(ret_file)):
                f = open(ret_file,"rb") 
                response = HttpResponse()
                response.write(f.read())
                try:
                    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(ret_file).replace("\n", "_")
                except Exception, e:
                    # remove non-ascii character
                    rfn = os.path.basename(ret_file)
                    response['Content-Disposition'] = 'attachment; filename=%s' % unicodedata.normalize('NFKD', rfn).encode('ascii', 'ignore')
                response['Content-Type'] ='audio/wav'
                response['Content-Length'] =os.path.getsize(ret_file )
                return response
            else:
                HttpResponse("file encoding failed by some reason.")

def downloadBMS(request, index=-1):
    if (index < 1):
        return HttpResponse("wrong request")
    else:
    	return getBMSfile(BASE_DIR + "\\..\\" + lr2db.dbList.items()[int(index)-1][0])

def downloadSabun(request, index=""):
    filepath = ""

    for row in lr2db.dbList.items():
        for bmsfile in row[1]:
            if (bmsfile[0] == index):
                filepath = bmsfile[7]

    if (filepath == ""):
        return HttpResponse("wrong request")
    else:
        filename = BASE_DIR + "\\..\\" + filepath
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='text/plain')
        try:
            response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename).replace("\n", "_")
        except Exception, e:
            opfn = os.path.basename(filename)
            response['Content-Disposition'] = 'attachment; filename=%s' % unicodedata.normalize('NFKD', opfn).encode('ascii', 'ignore')
        response['Content-Length'] = os.path.getsize(filename)
        return response

# -------------------------------------------------------------------------------- #

def getBMSfile(path):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    print "start to scan %s ..." % path

    _filenames = os.listdir(path)
    filenames = []
    for fn in _filenames:
        filenames.append(path + "\\" + fn)
        
    print "%d files found" % len(filenames)

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = os.path.split(path)[1]
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    try:
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename.replace("\n", "_")
    except Exception, e:
        # remove non-ascii character
        resp['Content-Disposition'] = 'attachment; filename=%s' % unicodedata.normalize('NFKD', zip_filename).encode('ascii', 'ignore')

    return resp