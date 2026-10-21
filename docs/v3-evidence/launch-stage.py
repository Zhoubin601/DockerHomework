from pathlib import Path
import os,subprocess,sys,json
p=Path(__file__).resolve().parent
name=sys.argv[1]
env=os.environ.copy();env['DISPLAY']=':99';env['GDK_BACKEND']='x11'
command='script -q -e -c '+__import__('shlex').quote('bash '+str(p/(name+'.sh')))+' '+__import__('shlex').quote(str(p/(name+'.txt')))+'; printf "\\n[Live stage finished; press Enter to close]\\n"; read -r'
args=['dbus-run-session','xfce4-terminal','--disable-server','--geometry=140x50+0+0','--font=DejaVu Sans Mono 10','--hide-menubar','--hide-borders','--hide-scrollbar','--color-bg=#ffffff','--color-text=#111827','--title=memory-game6085 v3 | '+name,'--execute','bash','--noprofile','--norc','-c',command]
f=(p/('terminal-'+name+'-launch.log')).open('w')
proc=subprocess.Popen(args,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(p/('terminal-'+name+'-pid.txt')).write_text(str(proc.pid));print(proc.pid)
