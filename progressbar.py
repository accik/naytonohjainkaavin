import time
import sys

def p_bar(total):
    bar_length = 30  # should be less than 100
    for i in range(total+1):
        percent = 100.0*i/total
        sys.stdout.write('\r')
        sys.stdout.write("Completed: [{:{}}] {:>3}%"
                        .format('='*int(percent/(100.0/bar_length)),
                                bar_length, int(percent)))
        sys.stdout.flush()
        time.sleep(0.005)

def progress_bar2(total, i):

    bar_length = 30  # should be less than 100
    percent = 100.0*i/total
    sys.stdout.write('\r')
    sys.stdout.write("Completed: [{:{}}] {:>3}%"
                    .format('='*int(percent/(100.0/bar_length)),
                                bar_length, int(percent)))
    sys.stdout.flush()
    time.sleep(0.005)

# total = 2000  # total number to reach
# bar_length = 30  # should be less than 100
# for i in range(total+1):
#     percent = 100.0*i/total
#     sys.stdout.write('\r')
#     sys.stdout.write("Completed: [{:{}}] {:>3}%"
#                      .format('='*int(percent/(100.0/bar_length)),
#                              bar_length, int(percent)))
#     sys.stdout.flush()
#     time.sleep(0.002)
#     # time.sleep(5)

# p_bar(50)

# p_bar2(50)