viscount
========

Web / visual front end for community profiling analyses from [the Beck Lab @ UW](http://faculty.washington.edu/dacb):


After cloning, run setup and source activate:

    ./setup # creates virtual environment, installs python modules, creates database
    source activate # launches virtual environment

The manage tool does a lot of the setup and day-to-date heavy lifting:

    ./manage
    usage: Manage viscount server installation

    Manage viscount server installation

    positional arguments:
      {database,shell,runserver}
        database            Perform database operations
        shell               Runs a Python shell inside Flask application context.
        runserver           Runs the Flask development server i.e. app.run()

    optional arguments:
      -?, --help            show this help message and exit

Individual command arguments provide their own help, e.g.

    ./manage database --help
    usage: Perform database operations
    
    Perform database operations
    
    positional arguments:
      {drop,populate,migrate,create,recreate,upgrade,downgrade}
        drop                Drops database tables
        populate            Populate database with default data
        migrate             Migrate data model
        create              Creates database tables from sqlalchemy models
        recreate            Recreates database tables (same as issuing 'drop' and
                            then 'create')
        upgrade             Upgrade data model
        downgrade           Downgrade data model
    
    optional arguments:
      -?, --help            show this help message and exit

Look at the runserver command for manage, e.g.

    usage: Manage viscount server installation runserver [-?] [-h HOST] [-p PORT]
                                                         [--threaded]
                                                         [--processes PROCESSES]
                                                         [--passthrough-errors]
                                                         [-d] [-D] [-r] [-R]
    
    Runs the Flask development server i.e. app.run()
    
    optional arguments:
      -?, --help            show this help message and exit
      -h HOST, --host HOST
      -p PORT, --port PORT
      --threaded
      --processes PROCESSES
      --passthrough-errors
      -d, --debug           enable the Werkzeug debugger (DO NOT use in production
                            code)
      -D, --no-debug        disable the Werkzeug debugger
      -r, --reload          monitor Python files for changes (not 100{'const':
                            True, 'help': 'monitor Python files for changes (not
                            100% safe for production use)', 'option_strings':
                            ['-r', '--reload'], 'dest': 'use_reloader',
                            'required': False, 'nargs': 0, 'choices': None,
                            'default': None, 'prog': 'Manage viscount server
                            installation runserver', 'container':
                            <argparse._ArgumentGroup object at 0x7ff747ace790>,
                            'type': None, 'metavar': None}afe for production use)
      -R, --no-reload       do not monitor Python files for changes


Testing / unit testing is performed with the test tool, e.g.


    usage: Test harness for viscount
    
    Test harness for viscount
    
    positional arguments:
      {run}
        run       Runs the test, required command
    
    optional arguments:
      -?, --help  show this help message and exit

And the flags for it:


    usage: Test harness for viscount run [-?] [-d] [-s] [-l] [-t] [-a] [-c]
    
    Runs the test, required command
    
    optional arguments:
      -?, --help            show this help message and exit
      -d, --db
      -s, --stub
      -l, --loginout
      -t, --tables
      -a, --all
      -c, --continueOnFail

