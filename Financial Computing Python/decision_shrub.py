
#
# File: decision_shrub_solution.py
# Author(s): Jingyi Guo
#

import math as m        # for log2

# return the entropy for a list of value counts, where the probability
# of counts[0] is counts[0] / sum(counts)
def entropy(counts):
    csum = sum(counts)
    if (not counts) or csum <= 0:
        return 0   # no counts: perfectly ordered
    e_ret = 0
    for c in counts:
        if c > 0:
            Pc = c / csum
            e_ret -= Pc * m.log2(Pc)
    return e_ret


data_file = 'stock_returns.csv'

label = 'Performance'   # attribute name of the classification label
rec_id = 'Ticker'       # attribute name of the record id field (not used for classification)

attr_names = {}         # set of attribute names from line 1
attr_name_to_col = dict()     # map from attribute name to column number
col_to_attr_name = dict()     # map from column number to attribute name
attr_name_to_values = dict()  # map from attribute name to set of attribute values
                              # for example: 'Performance' -> {'above', 'not_above'}
col_and_line_num_to_value = dict()  # map from (column number, line_num) to value
                                    # for example: (12, 2) -> 'not_above'

line_num = 0            # the current line number that we just read from the input
train_set_size = 200    # the number of records in the training set

# read in the data and build the data structures
fin = open(data_file, 'rt', encoding='utf-8')
for line in fin:
    line_num += 1
    line_no_nl = line[:len(line)-1] # line with no newline
    # print(str(line_num) + '\t' + line_no_nl)
    val_list = line_no_nl.split(',')

    if line_num == 1:   # attribute names
        attr_names = {v for v in val_list}
        attr_name_to_col = dict(zip(val_list,range(len(val_list))))
        col_to_attr_name = dict(zip(range(len(val_list)),val_list))
        attr_name_to_values = {an: set() for an in val_list}
        # print('attr_names:')
        # print(attr_names)
        # print('attr_name_to_col:')
        # print(attr_name_to_col,'\n')
        # print('col_to_attr_name:')
        # print(col_to_attr_name,'\n')
        # print('attr_name_to_values:')
        # print(attr_name_to_values,'\n')
    else:
        for c in range(len(val_list)):
            col_and_line_num_to_value[(c,line_num)] = val_list[c]
            an = col_to_attr_name[c]
            attr_name_to_values[an].add(val_list[c])
            # print(c, an, val_list[c], attr_name_to_values[an])

# now, analyze the training set, the first 200 records of data
# since the header is line 1, these will be lines 2 through 201, inclusive
col_list = [c for c in col_to_attr_name.keys()]
col_list.sort()
# print('col_list:')
# print(col_list,'\n')
print('Data file: ', data_file, '\n')
          
print('Record ID:    ', rec_id)
print('Label:        ', label, '\n')

print('{:15s}{:6s}   {:s}'.format('Attribute','Column','Values'))
for c in col_list:
    an = col_to_attr_name[c]
    antv = '' if an == rec_id else str(attr_name_to_values[an])
    print('{:15s}{:6d}   {:s}'.format(an, c, antv))
print('')

# compute and display the entropy for the label

label_col = attr_name_to_col[label]
label_vals = attr_name_to_values[label]
label_val_to_count = {v : 0 for v in label_vals}
for lnum in range(2, 202):
    v = col_and_line_num_to_value[(label_col,lnum)]
    label_val_to_count[v] += 1
# print('label_val_to_count:')
# print(label_val_to_count, '\n')
label_counts = [c for c in label_val_to_count.values()]
# print(label_counts)
H_label = entropy(label_counts)
# print(label_entropy)
print('H(',label,'):', H_label, '\n')

# compute and display the conditional entropies for other attributes:
# H(Performance | CEO_buy)   == sum over j of P(CEO_buy == yj) H(Performance | CEO_buy == yj),
#   where P(CEO_buy == yj) == (count of CEO_buy == yj in training set) / (size of training set),
#         H(Performance | CEO_buy == yj) == - sum over i of P(Performance = xi | CEO_buy == yj)
# H(Performance | CEO_sell)
# ...

# laying out one example in hideous detail:
# H(Performance | CEO_buy = 'true') = - P(Performance = 'above' | CEO_buy = 'true') * log2(...)
#                                     - P(Performance = 'not_above' | CEO_buy = 'true') * log2(...)
# H(Performance | CEO_buy = 'false') = - P(Performance = 'above' | CEO_buy = 'false') * log2(...)
#                                      - P(Performance = 'not_above' | CEO_buy = 'false') * log2(...)
# H(Performance | CEO_buy) =   P(CEO_buy = 'true') * H(Performance | CEO_buy = 'true')
#                            + P(CEO_buy = 'false') * H(Perfromance | CEO_buy = 'false)
# P(a=b) = count of recs where a = b / count of recs
# P(a=b | c=d) = count of recs where a = b and c = d / count of recs where c = d

# cb: CEO_buy
cb_col = attr_name_to_col['CEO_buy']
cb_vals = attr_name_to_values['CEO_buy']
cb_val_counts = {v: 0 for v in cb_vals}    # initial count of each value is 0
cb_val_counts_given_label = {(v1, v2): 0 for v1 in cb_vals for v2 in label_vals}
# print('cb_col:')
# print(cb_col, '\n')
# print('cb_vals:')
# print(cb_vals, '\n')
# print('cb_val_counts:')
# print(cb_val_counts, '\n')
# print('cb_val_counts_given_label:')
# print(cb_val_counts_given_label, '\n')

for lnum in range(2, 202):
    cb_line_val = col_and_line_num_to_value[(cb_col,lnum)]
    lab_line_val = col_and_line_num_to_value[(label_col,lnum)]
    cb_val_counts[cb_line_val] += 1
    cb_val_counts_given_label[(cb_line_val,lab_line_val)] += 1
# print('cb_val_counts:')
# print(cb_val_counts, '\n')
# print('cb_val_counts_given_label:')
# print(cb_val_counts_given_label, '\n')

count_cb_true = cb_val_counts['true']
count_cb_false = cb_val_counts['false']
count_lab_above_cb_true = cb_val_counts_given_label[('true','above')]
count_lab_above_cb_false = cb_val_counts_given_label[('false','above')]
count_lab_not_above_cb_true = cb_val_counts_given_label[('true','not_above')]
count_lab_not_above_cb_false = cb_val_counts_given_label[('false','not_above')]

# print('count_cb_true:               ', count_cb_true)
# print('count_cb_false:              ', count_cb_false)
# print('count_lab_above:             ', label_val_to_count['above'])
# print('count_lab_not_above:         ', label_val_to_count['not_above'])
# print('count_lab_above_cb_true:     ', count_lab_above_cb_true)
# print('count_lab_above_cb_false:    ', count_lab_above_cb_false)
# print('count_lab_not_above_cb_true: ', count_lab_not_above_cb_true)
# print('count_lab_not_above_cb_false:', count_lab_not_above_cb_false)

P_cb_true = count_cb_true / (count_cb_true + count_cb_false)
P_cb_false = count_cb_false / (count_cb_true + count_cb_false)
H_lab_cb_true = entropy([count_lab_above_cb_true, count_lab_not_above_cb_true])
H_lab_cb_false = entropy([count_lab_above_cb_false, count_lab_not_above_cb_false])
H_lab_cb = P_cb_true * H_lab_cb_true + P_cb_false * H_lab_cb_false
IG_lab_cb = H_label - H_lab_cb

print('P(CEO_buy = \'true\'):               ', P_cb_true)
print('P(CEO_buy = \'false\'):              ', P_cb_false)
print('H(Performance | CEO_buy = \'true\'): ', H_lab_cb_true)
print('H(Performance | CEO_buy = \'false\'):', H_lab_cb_false)
print('H(Performance | CEO_buy):    ', H_lab_cb)
print('IG(Performance | CEO_buy):   ', IG_lab_cb)
print('')

# do all the attributes in a loop

IG_and_attr_name = []   # a list of (IG,attr_name) tuples, to make sorting easy
for c in col_list:      # for each attribute, except label and rec_id ...
    if c == attr_name_to_col[label] or c == attr_name_to_col[rec_id]:
        continue
    atn = col_to_attr_name[c]
    atn_vals = attr_name_to_values[atn]
    atn_val_counts = {v: 0 for v in atn_vals}
    atn_val_counts_given_label = {(v1, v2): 0 for v1 in atn_vals for v2 in label_vals}
    for lnum in range(2, 202):
        at_line_val = col_and_line_num_to_value[(c,lnum)]
        lab_line_val = col_and_line_num_to_value[(label_col,lnum)]
        atn_val_counts[at_line_val] += 1
        atn_val_counts_given_label[(at_line_val,lab_line_val)] += 1
    count_atn_val = {v: atn_val_counts[v] for v in atn_vals}
    count_lab_val_atn_val = {k: atn_val_counts_given_label[k] for k in atn_val_counts_given_label.keys()}
    sum_atn_counts = sum(count_atn_val.values())
    P_atn_val = {v: 0 if sum_atn_counts == 0 else count_atn_val[v] / sum_atn_counts for v in atn_vals}
    H_lab_atn_val = {aval: entropy([atn_val_counts_given_label[(aval,lval)] for lval in label_vals]) for aval in atn_vals}
    H_atn_val = sum([P_atn_val[aval] * H_lab_atn_val[aval] for aval in atn_vals])
    print('{:30s} {}'.format('H(Performance | ' + atn + '):', H_atn_val))
    IG_and_attr_name.append((H_label - H_atn_val,atn))
print('')
IG_and_attr_name.sort()    
IG_and_attr_name.reverse()    
for t in IG_and_attr_name:
    print('{:30s} {:.8f}'.format('IG(Performance | ' + t[1] + '):', t[0]))
print('')

# we discover that ROE (return on equity) has the highest information gain in our training set,
# so the "stump" of our decision tree splits on ROE

# Compute information gains for the other attributes, for each value of ROE to find the second
# level attributes of our "shrub"

# really should have written this as a function ...
ROE_col = attr_name_to_col['ROE']
for ROE_val in attr_name_to_values['ROE']:
    IG_and_attr_name = []   # a list of (IG,attr_name) tuples, to make sorting easy
    for c in col_list:      # for each attribute, except label, rec_id, and ROE ...
        if c == attr_name_to_col[label] or c == attr_name_to_col[rec_id] or c == ROE_col:
            continue
        atn = col_to_attr_name[c]
        atn_vals = attr_name_to_values[atn]
        atn_val_counts = {v: 0 for v in atn_vals}
        atn_val_counts_given_label = {(v1, v2): 0 for v1 in atn_vals for v2 in label_vals}
        # we need the label_counts for this subset of data
        label_to_count = {v: 0 for v in label_vals}
        for lnum in range(2, 202):
            # here is where we split the data set by ROE value
            if col_and_line_num_to_value[(ROE_col,lnum)] == ROE_val:
                at_line_val = col_and_line_num_to_value[(c,lnum)]
                lab_line_val = col_and_line_num_to_value[(label_col,lnum)]
                label_to_count[lab_line_val] += 1
                atn_val_counts[at_line_val] += 1
                atn_val_counts_given_label[(at_line_val,lab_line_val)] += 1
        count_atn_val = {v: atn_val_counts[v] for v in atn_vals}
        count_lab_val_atn_val = {k: atn_val_counts_given_label[k] for k in atn_val_counts_given_label.keys()}
        sum_atn_counts = sum(count_atn_val.values())
        P_atn_val = {v: 0 if sum_atn_counts == 0 else count_atn_val[v] / sum_atn_counts for v in atn_vals}
        H_lab_atn_val = {aval: entropy([atn_val_counts_given_label[(aval,lval)] for lval in label_vals]) for aval in atn_vals}
        H_atn_val = sum([P_atn_val[aval] * H_lab_atn_val[aval] for aval in atn_vals])
        # print('{:45s} {}'.format('H(Performance | ' + atn + ', ROE = ' + ROE_val + '):', H_atn_val))
        H_label_given_ROE_val = entropy([v for v in label_to_count.values()])
        IG_and_attr_name.append((H_label_given_ROE_val - H_atn_val,atn))
    # print('')
    IG_and_attr_name.sort()    
    IG_and_attr_name.reverse()
    highest = IG_and_attr_name[0]
    print('Highest IG(Performance | ROE = ' + ROE_val + ', ' + highest[1] + '):', round(highest[0],8))

# so if ROE is well_above, split on Mkt_Cap,
# if ROE is above, split on DtoE,
# if ROE is below, split on CFO_buy
# if ROE is average, split on PEG_ratio
# if ROE is well_below: predict not_above (no examples in the training set)

# The Decision "Shrub"
# We don't need to compute actual counts, we can increment a counter for 'above'
# and decrement for 'not_above', then check counter for > 0

dt_level_one_on_ROE = {'well_above': 'Mkt_Cap',
                       'above':      'DtoE',
                       'below':      'CFO_buy',
                       'average':    'PEG_ratio',
                       'well_below': 'NONE'}
level_two_attrs = ['Mkt_Cap', 'DtoE', 'CFO_buy', 'PEG_ratio']
dt_level_two_on_attr_vals = {(a,v): 0 for a in level_two_attrs for v in attr_name_to_values[a]}
ROE_col = attr_name_to_col['ROE']
                        
for lnum in range(2,202):
    line_ROE_val = col_and_line_num_to_value[(ROE_col,lnum)]
    line_level_two_attr_name = dt_level_one_on_ROE[line_ROE_val]
    if line_level_two_attr_name != 'NONE':
        attr_col = attr_name_to_col[line_level_two_attr_name]
        line_attr_val = col_and_line_num_to_value[(attr_col,lnum)]
        line_label_val = col_and_line_num_to_value[(label_col,lnum)]
        if line_label_val == 'above':
            dt_level_two_on_attr_vals[(line_level_two_attr_name,line_attr_val)] += 1
        else:
            dt_level_two_on_attr_vals[(line_level_two_attr_name,line_attr_val)] -= 1

print('\nDecision Shrub:')
for roek in dt_level_one_on_ROE.keys():
    if roek == 'well_below':
        print("ROE == 'well_below' -> 'not_above'")
    else:
        lv2_atn = dt_level_one_on_ROE[roek]
        for atv in attr_name_to_values[lv2_atn]:
            count = dt_level_two_on_attr_vals[(lv2_atn,atv)]
            if count > 0:
                print("ROE == '" + roek + "', " + lv2_atn + " == '" + atv + "' -> 'above'")
            else:
                print("ROE == '" + roek + "', " + lv2_atn + " == '" + atv + "' -> 'not_above'")
print('')
                
# training set error: the fraction of incorrect predictions in the training set
train_errors = 0
for lnum in range(2,202):
    line_ROE_val = col_and_line_num_to_value[(ROE_col,lnum)]
    line_level_two_attr_name = dt_level_one_on_ROE[line_ROE_val]
    line_label_val = col_and_line_num_to_value[(label_col,lnum)]
    if line_level_two_attr_name == 'NONE':
        if line_label_val != 'not_above':
            train_errors += 1
    else:
        attr_col = attr_name_to_col[line_level_two_attr_name]
        line_attr_val = col_and_line_num_to_value[(attr_col,lnum)]
        count = dt_level_two_on_attr_vals[(line_level_two_attr_name,line_attr_val)]
        if count > 0 and line_label_val == 'not_above' or count <= 0 and line_label_val == 'above':
            train_errors += 1
print('training set error:', round(train_errors / 200, 4))

# test set error: the fraction of incorrect predictions in the training set
test_errors = 0
for lnum in range(202,2002):
    line_ROE_val = col_and_line_num_to_value[(ROE_col,lnum)]
    line_level_two_attr_name = dt_level_one_on_ROE[line_ROE_val]
    line_label_val = col_and_line_num_to_value[(label_col,lnum)]
    if line_level_two_attr_name == 'NONE':
        if line_label_val != 'not_above':
            test_errors += 1
    else:
        attr_col = attr_name_to_col[line_level_two_attr_name]
        line_attr_val = col_and_line_num_to_value[(attr_col,lnum)]
        count = dt_level_two_on_attr_vals[(line_level_two_attr_name,line_attr_val)]
        if count > 0 and line_label_val == 'not_above' or count <= 0 and line_label_val == 'above':
            test_errors += 1
print('test set error:', round(test_errors / 1800, 4))

                
