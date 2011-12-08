우분투 리눅스에서 편지봉투 인쇄를 자동화하기 위한 도구들.

# You need to...

Install BeautifulSoup:

    $ sudo apt-get install python-beautifulsoup

Install gdata:

    $ cp ~/apps/
    $ tar -xvzf gdata-x.x.x.tar.gz
    $ cd gdata-x.x.x
    $ ./setup.py install --home=$HOME

Append following line in your `.bashrc`:

    PYTHONPATH=$PYTHONPATH:$HOME/lib/python/
