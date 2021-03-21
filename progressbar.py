import time
import sys

'''
From https://gist.github.com/sibosutd/c1d9ef01d38630750a1d1fe05c367eb8
Modified by accik
Version 0.2
'''

def p_bar(total, i_text): # Whole bar
    if i_text == "":
        text = "Completed"
    else:
        text = i_text
    bar_length = 30  # should be less than 100
    for i in range(total+1):
        percent = 100.0*i/total
        sys.stdout.write('\r')
        sys.stdout.write("{:}: [{:{}}] {:>3}%"
                        .format(text,'='*int(percent/(100.0/bar_length)),
                                bar_length, int(percent)))
        sys.stdout.flush()
        time.sleep(0.005)
    return None

def progress_bar2(total, i): # One i at the time
    bar_length = 30  # should be less than 100
    percent = 100.0*i/total
    sys.stdout.write('\r')
    sys.stdout.write("Completed: [{:{}}] {:>3}% "
                    .format('='*int(percent/(100.0/bar_length)),
                                bar_length, int(percent)))
    sys.stdout.flush()
    time.sleep(0.005)
    return None