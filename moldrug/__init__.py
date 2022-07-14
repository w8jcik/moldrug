#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""For information of MolDrug:
    Docs: https://moldrug.readthedocs.io/en/latest/
    Source Code: https://github.com/ale94mleon/moldrug
"""
__version__ = "0.0.1.beta8"

import yaml, argparse, os, inspect

def run():
    from moldrug import utils

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        help='The configuration yaml file',
        dest='yaml_file',
        type=str
    )
    args = parser.parse_args()
    with open(args.yaml_file, 'r') as c:
        Config = yaml.safe_load(c)
    try:
        from moldrug import fitness
        Cost = dict(inspect.getmembers(fitness))[Config['costfunc']]
    except:
        from . import fitness
        Cost = dict(inspect.getmembers(fitness))[Config['costfunc']]
    
    if Config['type'].lower() == 'ga':
        TypeOfRun = utils.GA
    elif Config['type'].lower() == 'local':
        TypeOfRun = utils.Local
    else:
        raise RuntimeError(f"\"{Config['type']}\" it is not a possible type. Select from: GA or Local")
    InitArgs = Config.copy()

    # Modifying InitArgs
    [InitArgs.pop(key, None) for key in ['type', 'njobs']]
    InitArgs['costfunc'] = Cost
    
    # Initialize the class
    Results = TypeOfRun(**InitArgs)
    # Call the class
    Results(Config['njobs'])
    # Save final data
    Results.pickle(f"{InitArgs['deffnm']}_result", compress=True)
    print(Results.to_dataframe())
 