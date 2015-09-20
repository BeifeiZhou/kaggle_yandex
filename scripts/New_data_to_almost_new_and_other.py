import sys

def Get_new_data(old_file, really_new_file, new_file):
    with open(old_file) as data,\
        open(really_new_file, 'w') as r_new,\
        open(new_file, 'w') as new_small:
        for line_n, line in enumerate(data):
            line1 =  line.strip().split('\t')
            if (float(line1[13]) > 1e-5 or abs(sum(float(i) for i in line1[:10])) > 1e-5):
                new_small.write(line)
            else:
                r_new.write(line)

directory = "../../my_data/"
validation_file_new =  directory + "validation_new"
validation_with_some_statistic = directory + "validation_new_small"
validation_with_stat = directory + "validation_r_new"
test_file_new = directory + "test_new"
test_with_some_statistic = directory + "test_new_small"
test_with_stat = directory + "test_r_new"

Get_new_data(validation_file_new, validation_with_stat, validation_with_some_statistic)
Get_new_data(test_file_new, test_with_stat, test_with_some_statistic)
