"""Illustrate snapshotting a function and restarting it from an arbitrary place.
"""

import copy
import logging

import function_checkpointing.save_restore as save_restore

checkpoints = []


def save_checkpoint():
    ckpt = save_restore.save_jump()
    if ckpt:
        checkpoints.append(copy.deepcopy(ckpt))
    else:
        print("Checkpoint is being resumed")
        checkpoints.clear()
    return ckpt


def subroutine(a):
    print("entering subroutine. a=%d" % a)
    if not save_checkpoint():
        print('Resuming from subroutine')
        raise Exception()
    print("leaving subroutine. a=%d" % a)
    return 100


def processing(a, b):
    lst = []
    step = "step1"
    lst.append(step)
    print(step, "a=", a, "lst=", lst)

    if not save_checkpoint():
        print('Resuming from step1')

    d = subroutine(a)

    step = "step2"
    b = 2
    a *= b
    lst.append(step)
    print(step, "a=", a, "lst=", lst)

    if not save_checkpoint():
        print('Resuming from step2')

    step = "step3"
    c = 2
    a *= c
    lst.append(step)
    print(step, "a=", a, "lst=", lst)

    if not save_checkpoint():
        print('Resuming from step3')

    print("end")


def main():
    logging.basicConfig()
    logging.getLogger("function_checkpointing.save_restore").setLevel(logging.DEBUG)
    logging.root.setLevel(logging.DEBUG)

    print("---Run processing to completion, saving checkpoints---")
    processing(a=2, b=3)

    if len(checkpoints) == 4:
        print("---There are 4 checkpoints. Fastforward to 2nd checkpont---")
        save_restore.jump(checkpoints[1])
    else:
        print("---There are only %d checkpoints now---" % len(checkpoints))


main()
