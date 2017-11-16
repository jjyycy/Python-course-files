
# File: sort_test_solution_v2.py
# Author(s): Jingyi Guo

import random
import time      # functionality like C++ <ctime>
# 1.b
import min_heap

# BEGINNING OF SORTING ALGORITHMS CODE

# QUICKSORT ALGORITHM -- three functions

# a is the "array" of values to partition
# b is the beginning index within a
# e is one past the ending index within a
def qsort_partition(a, b, e):
    if e - b <= 0:
        return -1         # nothing to partition: no pivot index
    pivot = a[b]
    j = b                 # initial pivot index
    for k in range(b+1,e):
        if a[k] <= pivot:
            j += 1        # bump the pivot index forward
            a[j], a[k] = a[k], a[j]  # Python swap "trick"
    a[b], a[j] = a[j], a[b]
    return j              # return the pivot index

# this is the recursive function: we don't have pointers
# in Python, so use a helper
def quicksort_help(a, b, e):
    if e - b <= 0:
        return            # no array to sort
    pindex = qsort_partition(a, b, e)
    if pindex >= 0:
        quicksort_help(a, b, pindex)
        quicksort_help(a, pindex + 1, e)

# this is the top-level non-recursive function for the user to call:
# the "array" a is sorted in place
def quicksort(a):
    quicksort_help(a, 0, len(a))

# END OF QUICKSORT

# INSERTION SORT ALGORITHM

# a is the "array" of values to partition
def insertionsort(a):
    alen = len(a)
    for k in range(1,alen):
        kth_item = a[k]
        rev_idx = k
        while rev_idx > 0 and kth_item < a[rev_idx-1]:
            a[rev_idx] = a[rev_idx-1]
            rev_idx -= 1
        a[rev_idx] = kth_item

# END OF INSERTION SORT

# SELECTION SORT ALGORITHM

# a is the "array" of values to partition
def selectionsort(a):
    alen = len(a)
    for k in range(0,alen-1):
        min_idx = k
        for j in range(k, alen):
            if a[j] < a[min_idx]:
                min_idx = j
        a[k], a[min_idx] = a[min_idx], a[k]

# END OF SELECTION SORT

# BUBBLE SORT ALGORITHM

# a is the "array" of values to partition
def bubblesort(a):
    alen = len(a)
    for k in range(0,alen-1):
        num_swaps = 0
        for j in range(0,alen-1):  # or alen-1-k as a small optimization
            if a[j+1] < a[j]:
                a[j+1], a[j] = a[j], a[j+1]
                num_swaps += 1
        if num_swaps == 0:
            return

# END OF BUBBLE SORT

# MERGE SORT ALGORITHM

# merge the lists a1 and a2 into a
def merge(a, a1, a2):
    a1len = len(a1)
    a2len = len(a2)
    alen = a1len + a2len
    a1idx = 0
    a2idx = 0
    for i in range(alen):
        if a1idx == a1len:      # a1 has no items left
            a[i] = a2[a2idx]
            a2idx += 1
        elif a2idx == a2len:    # a2 has no items left
            a[i] = a1[a1idx]
            a1idx += 1
        else:                   # both a1 and a2 have items left
            if a1[a1idx] < a2[a2idx]:
                a[i] = a1[a1idx]
                a1idx += 1
            else:
                a[i] = a2[a2idx]
                a2idx += 1
    
# a is the "array" of values to partition
def mergesort(a):
    alen = len(a)
    if alen <= 1:
        return    # array is already sorted
    mid = alen // 2    # midpoint
    a1 = a[:mid]       # first "half"
    a2 = a[mid:]       # second "half"
    mergesort(a1)
    mergesort(a2)
    # merge the two sorted lists, a1 and a2, back into a
    merge(a, a1, a2)

# END OF MERGE SORT

# BUCKET SORT ALGORITHM

# a is the "array" of values to partition
def bucketsort(a):
    alen = len(a)
    amin = min(a)  # we know how to get min/max faster, but won't bother
    amax = max(a)
    num_buckets = amax - amin + 1
    buckets = [0] * num_buckets
    for val in a:
        buckets[val - amin] += 1
    aidx = 0
    for bidx in range(num_buckets):
        for i in range(buckets[bidx]):
            a[aidx] = amin + bidx
            aidx += 1

# END OF BUCKET SORT

# END OF SORTING ALGORITHMS CODE

# sorting algorithm testing function
# for "array" sizes of 1000, 2000, ..., 10000, we compute the mean
# run time from sorting 20 randomized test arrays
def sort_alg_tester(alg):    # alg is the algorithm (function object) to test
    alg_name = str(alg).split(' ')[1]
    mean_times = []
    for a_size in range(1,11):
        tot_time = 0
        for it in range(20):
            # randomly generated test "array"
            a_test = [random.randint(0,10_000_000) for i in range(a_size * 1_000)]

            a_test_copy = a_test.copy()    # a_test_copy refers to a COPY of a_test
            a_test_copy.sort()             # use built-in list sort on a_test_copy

            # test and time the sorting algorithm
            start_time = time.time()
            alg(a_test)
            end_time = time.time()
            run_time = end_time - start_time
            tot_time += run_time

            if a_test == a_test_copy:
                print('{}, a_size: {:2d},000, iter: {:2d}, {:10.4f} sec'.format(
                    alg_name, a_size, it, run_time))
            else:
                print(alg_name, 'NOT successful')
        mean_times.append(tot_time / 20)
    print(alg_name, 'mean times:', mean_times)
    return mean_times
    
def main():
    qs_times = sort_alg_tester(quicksort)
    # is_times = sort_alg_tester(insertionsort)
    # ss_times = sort_alg_tester(selectionsort)
    # bubs_times = sort_alg_tester(bubblesort)
    ms_times = sort_alg_tester(mergesort)
    # bucks_times = sort_alg_tester(bucketsort)
    hs_times = sort_alg_tester(min_heap_test_solution.heapsort)

    # you can be more (or less!) sophisticated than this
    import matplotlib.pyplot as plt
    N = [ x * 1000 for x in range(1,11)]
    plt.plot(N, qs_times, color='red')
    # plt.plot(N, is_times, color='blue')
    # plt.plot(N, ss_times, color='green')
    # plt.plot(N, bubs_times, color='orange')
    plt.plot(N, ms_times, color='purple')
    # plt.plot(N, bucks_times, color='black')
    plt.plot(N, hs_times, color='orange')
    plt.title('Time (sec) vs. Number of Values (N)')
    plt.xlabel('N')
    plt.ylabel('sec')
    # plt.legend(['quick', 'insertion', 'selection', 'bubble', 'merge', 'bucket'])
    plt.legend(['quick', 'merge', 'heap'])
    plt.show()
    

if __name__ == '__main__':
    main()

