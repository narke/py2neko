This will be a trans-compiler which converts Python to neko in order
to run Python on NekoVM.


## Code status

The translation logic is yet incomplete.  
Work in progress.


## Requirements

  + Python 3
  + NekoVM
  + Unix-like OS


## Usage:

    narke@darkstar:~$ git clone https://narke@github.com/narke/py2neko.git
    narke@darkstar:~$ export NEKOPATH="/usr/lib/neko;/opt/py2neko/lib"
    narke@darkstar:~$ cd py2neko.git
    narke@darkstar:~/py2neko.git$ ./install.py  (root privileges needed)
    narke@darkstar:~/py2neko.git$ ./py2neko.py <python file>
    narke@darkstar:~/py2neko.git$ nekoc out.neko
    narke@darkstar:~/py2neko.git$ neko out.n
