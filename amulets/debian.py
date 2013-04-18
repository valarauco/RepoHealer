'''
Created on 12/04/2013

@author: Manuel Delgado
'''
import gzip, subprocess, time, os, amulet

class Debian(amulet.Amulet):
    '''
    classdocs
    '''
    
    def is_checksum_file(self, filename):
        return "Packages.gz" in filename
        
    def check_with(self, filepath):
        packages = self._uncompress(filepath)
        self._checkfiles(packages)
        os.remove(packages)
     
    def _uncompress(self, uri):
        files = gzip.open(uri, 'rb')
        tmpfile = "/tmp/Packages" + str(int(time.time()))
        outfile = open(tmpfile, 'w') #aca hay que cambiarlo para truncar el archivo
        outfile.write(files.read())
        outfile.close()
        files.close()
        return tmpfile
    
    def _checkfiles(self, packages):      
        checked = set()
        filename = ""
        md5 = ""
        f = open(packages, "r")
        for i in f: 
            if "Filename:" in i:
                filename = i.split("Filename: ")
                filename = (filename[1])[0:-1]
            if "MD5sum:" in i:
                if filename not in checked:
                    #TODO find a better way
                    checked.add(filename)
                    md5 = i.split("MD5sum: ")
                    self._compare(filename, (md5[1])[0:-1])
        f.close()

    def _compare(self, filename, md5sum):
        localmd5 = self._calculate_md5(filename)
        if not (localmd5 == md5sum):
            self._download(filename)

        

    def _calculate_md5 (self, filename):
        filepath = os.path.join(self._healer.repobase, filename)
        if os.path.isfile(filepath):
            salida = subprocess.PIPE
            args = ['md5sum', filepath]
            p = subprocess.Popen(args, stdout=salida).communicate()[0]
            return p.split(' ')[0]
        else:
            return -1

    def _download (self, filename):
        self._healer.logging.info("MD5 checksum error in "+ filename)
        filepath = os.path.join(self._healer.repobase, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        salida = subprocess.PIPE
        args = ['wget','-O', filepath, self._healer.mirror + filename]
        p = subprocess.Popen(args, stdout=salida, stderr=subprocess.STDOUT).communicate()[0]
        self._healer.logging.debug(p)
        