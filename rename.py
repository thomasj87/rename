#!/usr/bin/env python -tt

__author__ = 'tjongeri'

import logging
import glob
import os
import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():

    if len(sys.argv) < 4:
        logging.error("Not enough arguments!")
        print 'Help: ' \
              '<directory> <pattern> <rename_prefix> (index start number)'
        sys.exit(10)


    directory = sys.argv[1]
    to_find = sys.argv[2]
    rename_prefix = sys.argv[3]

    list_files = glob.glob1(directory, to_find)

    if len(sys.argv) >= 5:
        index = int(sys.argv[4])
    else:
        index = 0001

    execute_list = []

    for filename in list_files:
        existing_path = os.path.join(directory, filename)
        title, ext = os.path.splitext(os.path.basename(existing_path))
        new = directory + rename_prefix + str(index) + ext
        execute_list.append([existing_path, new])
        index += 1

    for item in execute_list:
        print "Rename {0} to {1}?".format(item[0], item[1])
        if os.path.isfile(item[1]):
            logging.warn("{0} already exists!".format(item[1]))

    confirm = query_yes_no("You want to rename these files?", default="no")

    if confirm:
        for item in execute_list:
            if os.path.isfile(item[1]):
                logging.warn("{0} already exists!".format(item[1]))
                logging.warn("File will not be overwritten!".format(item[1]))
            else:
                os.rename(item[0], item[1])
                print "Renamed {0} to {1}!".format(item[0], item[1])
    else:
        print "No changes made!"
        print "Exiting..."

if __name__ == '__main__':

    # Production syntax for logging
    logging.basicConfig(stream=sys.stderr,
                level=logging.INFO,
                format="[%(levelname)8s]:%(name)s:  %(message)s")
    # Dev syntax for logging
    logging.debug("Starting script!")

    main()
