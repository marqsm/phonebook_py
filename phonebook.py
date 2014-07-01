#!/usr/bin/env python
import os
import argparse


def pb_parse_input_row(row):
    """parse one row from file input"""
    row = row.rstrip('\n')    # remove digits
    name = ''.join([c for c in row if not c.isdigit()]).strip()
    number = ''.join([c for c in row if c.isdigit()]).strip()
    return name, number


def pb_parse_output_row(name, number):
    """parse output string from name & number"""
    return name + ' ' + number + '\n'


def print_results(rows):
    """parse all results (accepts list of key-value pairs)"""
    if len(rows) > 0:
        for name, number in rows.iteritems():
            print name + ' ' + number
    else:
        print 'No results'


def pb_load(filename):
    """load phonebook from file"""
    pb = {}
    with open(filename, 'r') as f:
        for line in f:
            name, number = pb_parse_input_row(line)
            pb[name] = number
    return pb


def pb_save(filename, pb):
    """save phonebook to a file"""
    with open(filename, 'w') as f:
        for name, number in pb.iteritems():
            f.write(pb_parse_output_row(name, number))


def pb_create(filename):
    if not os.path.isfile(filename):
        f = open(filename, 'w')
        f.close()
        return True
        print('Created phonebook %s in current directory' % (filename))
    else:
        print('Error: file %s already exists!' % (filename))
        return False


def pb_lookup(name_lookup, pb):
    """find by text partial match to name string"""
    results = {}
    search_name = name_lookup.lower()
    for name, num in pb.iteritems():
        if search_name in name.lower():
            results[name] = num
    return results


def pb_reverse_lookup(number, pb):
    """find by phone number (exact match)"""
    results = {}
    canonical_num = "".join([c for c in number if c.isdigit()])
    for name, num in pb.iteritems():
        if num.strip() == canonical_num:
            results[name] = num
    return results


def pb_add(name, number, pb):
    """check if row exists. Return false if already exists"""
    if name in pb:
        return False
    pb[name] = number
    return True


def pb_change(name, number, pb):
    print(name, number, pb)
    if name in pb:
        pb[name] = number
        return True
    else:
        return False


def pb_remove(name, pb):
    """phonebook remove 'John Michael' hsphonebook.pb"""
    if name in pb:
        pb.pop(name, None)
        return True
    else:
        return False


# command line handler functions
def parse_arguments(args):
    accepted_commands = ['create', 'add', 'change',
                         'remove', 'lookup', 'reverse-lookup']
    filename = None
    name = None
    number = None
    search_term = None

    command = args[0]
    if command not in accepted_commands:
        print 'Command not recognized'
        return False

    filename = args.pop()
    if command in ['lookup', 'reverse-lookup']:
        search_term = args[1]
    elif command in ['add', 'change']:
        name = args[1]
        number = args[2]
    elif command == 'remove':
        name = args[1]
    return filename, name, number, search_term


def handle_rev_lookup(args):
    results = pb_reverse_lookup(args.number, args.phonebook)
    if results:
        print_results(results)
    else:
        print('No search results for %s' % (args.number))


def handle_lookup(args):
    results = pb_lookup(args.name, args.phonebook)
    if results:
        print_results(results)
    else:
        print('No search results for %s' % (args.name))


def handle_add(args):
    if pb_add(args.name, args.number, args.phonebook):
        print('Added "%s %s to phonebook %s' %
              (args.name, args.number, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('A person called %s already in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_change(args):
    if pb_change(args.name, args.number, args.phonebook):
        print('Change number for "%s" to "%s" in phonebook %s' %
              (args.name, args.number, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_remove(args):
    if pb_remove(args.name, args.phonebook):
        print('Removed "%s" from phonebook %s' % (args.name, args.phone_file))
        pb_save(args.phone_file, args.phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_create(args):
    pb_create(args.name)


"""get argumets, make sure the py file is not the first one."""
parser = argparse.ArgumentParser(description="Manage those phonebooks.")
subparsers = parser.add_subparsers(dest="command")

create_parser = subparsers.add_parser("create", help="Create a new phonebook.")
create_parser.add_argument("phone_file",
                           help="Name of the phonebook file to create.")
create_parser.set_defaults(func=handle_create)

lookup_parser = subparsers.add_parser("lookup",
                                      help="Lookup a person in a phonebook.")
lookup_parser.add_argument("name", help="name of person to lookup.")
lookup_parser.add_argument("phone_file", help="phonebook to look up in.")
lookup_parser.set_defaults(func=handle_lookup)

add_parser = subparsers.add_parser("add",
                                   help="Add a new person to phonebook.")
add_parser.add_argument("name", help="name of person to add")
add_parser.add_argument("number", help="their number")
add_parser.add_argument("phone_file", help="phonebook to look up in.")
add_parser.set_defaults(func=handle_add)

change_parser = subparsers.add_parser("change",
                                      help="Change someone's phone number.")
change_parser.add_argument("name",
                           help="name of person whose number to change.")
change_parser.add_argument("number", help="new number")
change_parser.add_argument("phone_file", help="phonebook to change in.")
change_parser.set_defaults(func=handle_change)

remove_parser = subparsers.add_parser("remove",
                                      help="Remove someone.")
remove_parser.add_argument("name", help="name of person to remove.")
remove_parser.add_argument("phone_file", help="phonebook to remove them from.")
remove_parser.set_defaults(func=handle_remove)

rev_lookup_parser = subparsers.add_parser("reverse-lookup",
                                          help="Look someone up by number.")
rev_lookup_parser.add_argument("number", help="number of person to look up.")
rev_lookup_parser.add_argument("phone_file", help="phonebook to lookup in.")
rev_lookup_parser.set_defaults(func=handle_rev_lookup)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.command != "create":
        args.phonebook = pb_load(args.phone_file)
    args.func(args)
