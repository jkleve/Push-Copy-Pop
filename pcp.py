#!/bin/env python3
import argparse
from collections import namedtuple
import logging as log
import os
from os import getcwd
from os.path import exists, isdir, isfile
import shutil
import sys

_QueueItem = namedtuple('QueueItem', ['is_file', 'path'])

test = True


def _load_stack(save_file):
    stack = list()
    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            for l in f:
                path = l.strip()
                is_file = os.path.isfile(path)
                stack.append(_QueueItem(is_file, path))
    return stack

_stack_file = '/tmp/pop_files/stack.txt'
_delete_dir = '/tmp/pop_files/trash'
_stack = _load_stack(_stack_file)


def check_exists(path):
    if os.path.exists(path):
        c = input("%s already exists. Replace? " % path)
        if c != 'y':
            print("Aborting ...")
            return False
    return True


def push(file):
    if exists(file):
        is_file = os.path.isfile(file)
        _stack.append(_QueueItem(is_file, file))
    else:
        print("%s doesn't exists" % file)


def copy(item, dst):
    src = item.path
    if check_exists(dst):
        if item.is_file:
            log.info("Copying file %s to %s" % (src, dst))
            if not test:
                shutil.copy(src, dst)
        else:
            log.info("Copying directory %s to %s" % (src, dst))
            if not test:
                shutil.copytree(src, dst)
    else:  # restore stack
        push(item.path)


def move(item, dst):
    src = item.path
    if check_exists(dst):
        log.info("Moving %s to %s" % (src, dst))
        if not test:
            shutil.move(src, dst)
    else:  # restore stack
        push(item.path)


def delete(item):
    c = input("Delete %s? " % item.path)
    if c == 'y':
        _, f = os.path.split(item.path)
        move(item, os.path.join(_delete_dir, f))
    else:  # restore stack
        push(item.path)


def empty_stack():
    global _stack
    _stack = list()


def print_stack():
    if len(_stack) == 0:
        print("The stack is empty")
    else:
        for item, i in enumerate(_stack):
            print("{} \t {}".format(i, item.path))


def pop_stack():
    item = None
    try:
        item = _stack.pop()
    except IndexError:
        print("Stack is empty")
    return item


def save_stack(filename):
    d, f = os.path.split(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    with open(filename, 'w') as f:
        for item in _stack:
            f.write("%s\n" % item.path)


class _ArgsHandler:
    def __init__(self):
        usage = '\n'.join(("pop <command> [<args>]",
                           "",
                           "Available commands:",
                           " push    push files to stack",
                           " copy    copy files from stack",
                           " pop     pop files from stack",
                           " delete  delete file on top of stack",
                           ""))
        parser = argparse.ArgumentParser(
                description='Carry files with you as you move around in terminal',
                usage=usage)
        parser.add_argument('command', help='Subcommand to run')

        # if no command, print stack
        if len(sys.argv) == 1:
            print_stack()
            sys.exit(0)

        # parse just the command argument
        args = parser.parse_args(sys.argv[1:2])
        # call command method
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
        getattr(self, args.command)()

    def push(self):
        parser = argparse.ArgumentParser(description='push files to stack')
        parser.add_argument('files', metavar='f', type=str, nargs='+',
                                     help='files to push to stack')
        args = parser.parse_args(sys.argv[2:])
        # push all files
        cwd = getcwd()
        for f in args.files:
            path = os.path.join(cwd, f)
            push(path)
        # print and save
        print_stack()
        save_stack(_stack_file)

    def copy(self):
        parser = argparse.ArgumentParser(description='copy files from stack')
        parser.add_argument('file', metavar='f', type=str, nargs='?',
                                     help='directory or filename to copy to')
        args = parser.parse_args(sys.argv[2:])
        src = pop_stack()
        if src is None:
            print("Nothing is in the stack")
            sys.exit(1)
        _, src_f = os.path.split(src.path)
        cwd = getcwd()

        if args.file is None:
            dst = os.path.join(cwd, src_f)
        else:
            dst = os.path.join(cwd, args.file)

        if exists(dst):
            if isdir(dst):
                dst = os.path.join(dst, src_f)

        copy(src, dst)
        # print and save
        print_stack()
        save_stack(_stack_file)

    def pop(self):
        parser = argparse.ArgumentParser(description='pop files from stack')
        parser.add_argument('file', metavar='f', type=str, nargs='?',
                                     help='directory or filename to move to')
        args = parser.parse_args(sys.argv[2:])
        src = pop_stack()
        if src is None:
            print("Nothing is in the stack")
            sys.exit(1)
        _, src_f = os.path.split(src.path)
        cwd = getcwd()

        if args.file is None:
            dst = os.path.join(cwd, src_f)
        else:
            dst = os.path.join(cwd, args.file)

        if exists(dst):
            if isdir(dst):
                dst = os.path.join(dst, src_f)

        move(src, dst)
        # print and save
        print_stack()
        save_stack(_stack_file)

    def delete(self):
        src = pop_stack()
        if src is None:
            print("Nothing is in the stack")
            sys.exit(1)
        delete(src)
        # print and save
        print_stack()
        save_stack(_stack_file)

# TODO add option to choose to pop from somewhere else besides the top of the stack
if __name__ == "__main__":
    # setup logging
    log.basicConfig(stream=sys.stdout, level=log.INFO)

    # run arg handler
    _ArgsHandler()
    sys.exit()

