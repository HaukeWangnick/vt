import os
import sys
import argparse
import subprocess
import select
import shutil

def existing(path,exist,fmt,join):
    orig = path
    if join: path = os.path.join(path,join)
    if os.path.exists(path)!=exist:
        if fmt is None: fmt = '%s doesn\'t exist' if exist else '%s already exists'
        raise argparse.ArgumentTypeError(fmt%path)
    return orig
             
def existingtype(exist,fmt=None,join=None):
    return lambda path: existing(path,exist,fmt,join)

def communicate(proc,timeout=None,progress=None):
    out = []
    err = []
    read_set = []
    if proc.stdout: read_set.append(proc.stdout)
    if proc.stderr: read_set.append(proc.stderr)
    while (read_set):
        try:
            (rlist,wlist,xlist) = select.select(read_set, [], [], timeout)
        except select.error as e:
            if e.args[0]==errno.EINTR: continue
            raise
        if not (rlist or wlist or xlist):
            proc.kill()
            raise subprocess.TimeoutExpired(proc.args,timeout)
        if proc.stdout in rlist:
            data = os.read(proc.stdout.fileno(),1024)
            if data:
                out.append(data)
                if progress: progress(data,False)
            else:
                proc.stdout.close()
                read_set.remove(proc.stdout)
        if proc.stderr in rlist:
            data = os.read(proc.stderr.fileno(),1024)
            if data:
                err.append(data)
                if progress: progress(data,True)
            else:
                proc.stderr.close()
                read_set.remove(proc.stderr)
    out = b''.join(out)
    err = b''.join(err)
    proc.wait(timeout=timeout)
    if proc.universal_newlines:
        if out: out = out.decode(proc.stdout.encoding).replace('\r\n','\n').replace('\r', '\n')
        if err: err = err.decode(proc.stderr.encoding).replace('\r\n','\n').replace('\r', '\n')
    return (out,err)

class callError(subprocess.CalledProcessError): pass

def call(cmd,timeout=None,progress=None):
     if type(cmd) is str: cmd = cmd.split()
     proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
     out,err = communicate(proc,timeout,progress)
     if proc.returncode:
         #print("cmd: "+str(cmd))
         #print("returncode: "+str(proc.returncode))
         #print("out: "+str(out))
         #print("err: "+str(err))
         #exc = subprocess.CalledProcessError(proc.returncode,cmd,out)
         #exc.error = err
         raise callError(proc.returncode,cmd,out)
     return out

def projectinit(name,vtdir,template,gitinit=True):
    try:
        shutil.copytree(os.path.join(vtdir,'resources',template),name,symlinks=True)
    except OSError as exc:
        sys.exit('%s when initialising project directory from template'%exc)

    if gitinit:
        try:
            os.chdir(name)
            call('git init',5)
        except callError as exc:
            sys.exit('Project directory created, but git init failed (%s)'%exc)

