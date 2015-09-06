__author__ = 'stepan'
import struct

INT_LENGTH = 4

class serp:
    def __init__(self):
        self.type_of_record = 'Q'
        self.serp_id = 0
        self.query_id = 0
        self.time_passed = 0
        self.list_of_terms = []
        self.list_of_urls_and_domains = []


class session:
    def __init__(self, line=None):
        if line == None:
            self.user_id = ''
            self.day = ''
            self.serps = []
        else:
            position = 0
            self.serps = []
            self.user_id, self.day, num_serps = struct.unpack('iii', line[:3 * INT_LENGTH])
            position += 3 * INT_LENGTH
            for i in range(num_serps):
                self.serps.append(serp())

                self.serps[-1].type_of_record = line[position]
                position += 1

                self.serps[-1].serp_id, self.serps[-1].query_id, self.serps[-1].time_passed = struct.unpack(
                    'iii', line[position: position + 3 * INT_LENGTH])
                position += 3 * INT_LENGTH

                num_of_terms = struct.unpack('i', line[position: position + INT_LENGTH])[0]
                position += INT_LENGTH
                self.serps[-1].list_of_terms = list(struct.unpack('i' * num_of_terms,
                    line[position: position + num_of_terms * INT_LENGTH]))
                position += num_of_terms * INT_LENGTH

                num_urls = struct.unpack('i', line[position: position + INT_LENGTH])[0]
                position += INT_LENGTH
                for url_index in range(num_urls):
                    self.serps[-1].list_of_urls_and_domains.append(
                        struct.unpack('iiii', line[position:position + 4 * INT_LENGTH]))
                    position += 4 * INT_LENGTH

                pass