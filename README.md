viscount
========

Web / visual front end for community profiling analyses from [the Beck Lab @ UW](http://faculty.washington.edu/dacb):


After cloning, run setup and source activate:

    ./setup # creates virtual environment, installs python modules, creates database
    source activate # launches virtual environment

Run the server with the run script:

    usage: run [-h] [-d] [-i HOST] [-p PORT] [-r]
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Enable debug mode
      -i HOST, --host HOST  Specify the host interface for the server (default
                            all)
      -p PORT, --port PORT  Specify the port for the server (default 5000)
      -r, --root            Allow viscount to be run as root
