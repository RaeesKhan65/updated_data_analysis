"""
This script is created to analyze RB Data.
Written by Ahmed Omran and Pubudu Wijesinghe on 10/15/21
"""

import numpy as np

def percent_change(signal,reference):
    return (signal-reference)/reference


def fidelity_calculation(content):

    threshold,sig_all,ref_all,Ne,x_all,expected_state_all = content

    sig_run, ref_run = np.array_split(sig_all, Ne), np.array_split(ref_all, Ne)  # breaking the data into num of runs
    x_run, expected_state_run = np.array_split(x_all, Ne), np.array_split(expected_state_all,Ne)  # breaking the truncation lengths and expected states into num of runs

    r_list = x_run[0]
    num_sequences = len(r_list)
    fidelity_list = [0] * num_sequences
    for i in range(num_sequences):
        num_correct_states = 0
        for j in range(Ne):
            pch = percent_change(sig_run[j][i],ref_run[j][i])
            if pch > threshold:
                actual_final_state = 0
            else:
                actual_final_state = 1
            if actual_final_state == expected_state_run[j][i]:
                num_correct_states += 1
        fidelity_list[i] = num_correct_states / Ne

    a, b = np.polyfit(np.array([float(i) for i in r_list]),np.array([float(i) for i in fidelity_list])*100, 1)
    plot_list = a*np.array([float(i) for i in r_list])+b
    return (r_list,fidelity_list,plot_list)
