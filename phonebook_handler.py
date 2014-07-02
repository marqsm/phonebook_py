#!/usr/bin/env python
import argparse
import phonebook

phonebook = phonebook.Phonebook()


# command line handler functions
def handle_rev_lookup(args):
    results = phonebook.pb_reverse_lookup(args.number)
    if results:
        phonebook.print_results(results)
    else:
        print('No search results for %s' % (args.number))


def handle_lookup(args):
    results = phonebook.pb_lookup(args.name)
    if results:
        phonebook.print_results(results)
    else:
        print('No search results for %s' % (args.name))


def handle_add(args):
    if phonebook.pb_add(args.name, args.number):
        print('Added "%s %s to phonebook %s' %
              (args.name, args.number, args.phone_file))
        phonebook.pb_save(args.phone_file, args.phonebook)
    else:
        print('A person called %s already in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_change(args):
    if phonebook.pb_change(args.name, args.number):
        print('Change number for "%s" to "%s" in phonebook %s' %
              (args.name, args.number, args.phone_file))
        phonebook.pb_save(args.phone_file, args.phonebook)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_remove(args):
    if phonebook.pb_remove(args.name):
        print('Removed "%s" from phonebook %s' % (args.name, args.phone_file))
        phonebook.pb_save(args.phone_file)
    else:
        print('No person called %s in phonebook %s. Changes ignored.' %
              (args.name, args.phone_file))


def handle_create(args):
    phonebook.pb_create(args.name)


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
        args.phonebook = phonebook.pb_load(args.phone_file)
    args.func(args)
