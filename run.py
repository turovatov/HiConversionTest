#! /usr/bin/python3.5

from optparse import OptionParser

from db.connection import db_mgr
from tool.config import config_mgr
from web.app import create_web_app

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('--debug', default=0)
    parser.add_option('--init', default=0)
    options, list_args = parser.parse_args()

    config_file = 'debug-config.yaml' if options.debug else 'config.yaml'
    config_mgr.init_values(filename=config_file)
    config_mgr.add_value(key='debug', value=options.debug)

    db_mgr.init_engine()
    if options.init:
        db_mgr.create_db()
        db_mgr.init_values()

    run_params = dict(
        host='0.0.0.0',
        port=8000,
        debug=False
    )
    app = create_web_app()
    app.run(**run_params)
