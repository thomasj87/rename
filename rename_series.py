#!/usr/bin/env python -tt

__author__ = 'tjongeri'

import logging
import glob
import os
import sys
import datetime
import time
import re

try:
    import exifread
except:
    print "No exifread module"

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

def get_creat_date(file):
    try:
        f = open(file, 'rb')
        tags = exifread.process_file(f)

        if 'Image DateTime' in tags:
            file_date_time = datetime.datetime.strptime(str(tags['Image DateTime']), "%Y:%m:%d %H:%M:%S")
        else:
            system_time = time.ctime(os.path.getctime(file))
            file_date_time = datetime.datetime.strptime(system_time, "%c")

        if file_date_time.minute < 10:
            minute = '0' + str(file_date_time.minute)
        else:
            minute = str(file_date_time.minute)

        if file_date_time.hour < 10:
            hour = '0' + str(file_date_time.hour)
        else:
            hour = str(file_date_time.hour)

        if file_date_time.second < 10:
            second = '0' + str(file_date_time.second)
        else:
            second = str(file_date_time.second)

        if file_date_time.month < 10:
            month = '0' + str(file_date_time.month)
        else:
            month = str(file_date_time.month)

        if file_date_time.day < 10:
            day = '0' + str(file_date_time.day)
        else:
            day = str(file_date_time.day)

        return_value = str(file_date_time.year) + month + day + '_' + hour + minute + second
    except:
        return_value = None

    return return_value

def main():


    if len(sys.argv) < 5:
        logging.error("Not enough arguments! (%s)" % len(sys.argv))
        print 'Help: ' \
              '<directory> <match pattern> <change> <pre-pattern> [post-pattern]'
        sys.exit(10)

    directory = sys.argv[1]
    to_find = sys.argv[2]
    change = sys.argv[3]
    pre_pat = sys.argv[4]
    post_pat = None


    list_files = glob.glob1(directory, to_find)

    if len(sys.argv) == 6:
        post_pat = sys.argv[5]

    print "Script Settings:\n"
    print "Len: %s" % len(sys.argv)
    print "Dir: %s" % directory
    print "Find: %s" % to_find
    print "Change To: %s" % change
    print "Pre: %s" % pre_pat
    print "Post: %s" % post_pat

    print "\n"
    print "Changes:\n"

    execute_list = []

    for filename in list_files:
        existing_path = os.path.join(directory, filename)


        title, ext = os.path.splitext(os.path.basename(existing_path))

        if post_pat:
            re_search = r"(" + re.escape(pre_pat) + r")(\d+)(" + re.escape(post_pat) + r")"
        else:
            re_search = r"(" + re.escape(pre_pat) + r")(\d+)"

        try:
            match = re.search(re_search, title)

            serie_id = match.group(2)
            new = directory + "/" + change + serie_id + ext

            execute_list.append([existing_path, new])

        except:
            print "Could not match file: %s" % existing_path

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
