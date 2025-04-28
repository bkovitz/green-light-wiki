#!  /bin/bash
#echo "Content-type: text/plain"
#echo

export HOME=/home/bkovitz
export PATH=$HOME/software/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=$HOME/software/lib

#echo "yo"
#echo $PATH
#echo $PYTHONPATH
#which python
#python -V 2>&1

#env | sort

cd $HOME/wiki
date >> dates
TZ=PST8PDT python glwiki/Main.py 2>&1
#tee stdin.log | TZ=PST8PDT nohup python glwiki/WikiClient.py 2>&1 | tee output.log
#TZ=PST8PDT nohup python glwiki/WikiClient.py 2>&1

# rm -f /tmp/ben
# touch /tmp/ben
# ls -l /tmp/ben
# echo "uh huh"
