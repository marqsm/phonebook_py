import os


class Phonebook():
    myvar = [1, 2, 3]

    def __init__(self):
        self.phonebook = {}

        @staticmethod
    def pb_parse_input_row(row):
        """parse one row from file input"""
        row = row.rstrip('\n')    # remove digits
        name = ''.join([c for c in row if not c.isdigit()]).strip()
        number = ''.join([c for c in row if c.isdigit()]).strip()
        return name, number

    @staticmethod
    def pb_parse_output_row(name, number):
        """parse output string from name & number"""
        return name + ' ' + number + '\n'

    def print_results(self, rows):
        """parse all results (accepts list of key-value pairs)"""
        if len(rows) > 0:
            for name, number in rows.iteritems():
                print name + ' ' + number
        else:
            print 'No results'

    def pb_load(self, filename):
        """load phonebook from file"""
        pb = {}
        with open(filename, 'r') as f:
            for line in f:
                name, number = self.pb_parse_input_row(line)
                pb[name] = number
        self.phonebook = pb
        return pb

    def pb_save(self, filename):
        """save phonebook to a file"""
        with open(filename, 'w') as f:
            for name, number in self.phonebook.iteritems():
                f.write(self.pb_parse_output_row(name, number))

    def pb_create(self, filename):
        if not os.path.isfile(filename):
            f = open(filename, 'w')
            f.close()
            return True
            print('Created phonebook %s in current directory' % (filename))
        else:
            print('Error: file %s already exists!' % (filename))
            return False

    def pb_lookup(self, name_lookup):
        """find by text partial match to name string"""
        results = {}
        search_name = name_lookup.lower()
        for name, num in self.phonebook.iteritems():
            if search_name in name.lower():
                results[name] = num
        return results

    def pb_reverse_lookup(self, number):
        """find by phone number (exact match)"""
        results = {}
        canonical_num = "".join([c for c in number if c.isdigit()])
        for name, num in self.phonebook.iteritems():
            if num.strip() == canonical_num:
                results[name] = num
        return results

    def pb_add(self, name, number):
        """check if row exists. Return false if already exists"""
        if name in self.phonebook:
            return False
        self.phonebook[name] = number
        return True

    def pb_change(self, name, number):
        print(name, number, self.phonebook)
        if name in self.phonebook:
            self.phonebook[name] = number
            return True
        else:
            return False

    def pb_remove(self, name):
        """phonebook remove 'John Michael' hsphonebook.pb"""
        if name in self.phonebook:
            self.phonebook.pop(name, None)
            return True
        else:
            return False
