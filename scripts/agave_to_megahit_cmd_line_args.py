"""
Usage:

  python agave_to_megahit_cmd_line-args.py \
      -o /path/to/output/directory \
      -1 /path/to/forward/reads \
      -1 /path/to/more/forward/reads \
      -2 /path/to/reverse/reads \
      -2 /path/to/more/reverse/reads \
      -some more -options

Convert Agave app arguments such as

  -r file1 -r file2 -r file3 -x -y -z

to MEGAHIT command line arguments such as

  -r file1,file2,file3 -x -y -z

In addition the optional -o argument specifies the output directory. If it is
not given then the default '$PWD/megahit-out' will be passed to MEGAHIT.

Since this script may also be invoked in contexts other than an Agave job it should
leave normal MEGAHIT command line args alone.

"""
import argparse
import io
import os
import sys


def get_args(argv):
    """
    The first positional argument is the output directory. Remaining command line arguments
    either need conversion from Agave repeated-option format or can be passed directly to
    MEGAHIT.

    :return: (1-ple of output directory, tuple of everything else)
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-o', '--output_dir',
        required=False,
        default=os.path.join(os.getcwd(), 'megahit-out'),
        help='Directory for MEGAHIT output.')
    return arg_parser.parse_known_args(args=argv)


def agave_to_megahit_cmd_line_args(argv):
    output_arg, agave_cmd_line_args = get_args(argv)
    megahit_cmd_line = convert_agave_args_to_megahit_cmd_line(agave_cmd_line_args)

    cmd_line_args = io.StringIO()
    cmd_line_args.write('-o ')
    cmd_line_args.write(output_arg.output_dir)
    cmd_line_args.write(' ')
    cmd_line_args.write(megahit_cmd_line)

    return cmd_line_args.getvalue()


def convert_agave_args_to_megahit_cmd_line(agave_cmd_line_args):

    # the options in this table need conversion from Agave to MEGAHIT
    input_option_table = {
        '-1': list(),
        '-2': list(),
        '--12': list(),
        '-r': list()
    }

    additional_args = []

    unknown_arg_list = list(agave_cmd_line_args)
    while len(unknown_arg_list) > 0:
        next_arg = unknown_arg_list.pop(0)
        if next_arg in input_option_table.keys():
            input_option_table[next_arg].append(unknown_arg_list.pop(0))
        else:
            additional_args.append(next_arg)

    cmd_line_args = io.StringIO()

    for opt, arg_list in [(opt_, input_option_table[opt_]) for opt_ in ('-1', '-2', '--12', '-r')]:
        if len(arg_list) > 0:
            cmd_line_args.write(' {} {}'.format(opt, ','.join(arg_list)))

    if len(additional_args) > 0:
        cmd_line_args.write(' ')
        cmd_line_args.write(' '.join(additional_args))

    return cmd_line_args.getvalue().strip()


if __name__ == '__main__':
    print(agave_to_megahit_cmd_line_args(sys.argv))


def test_agave_to_megahit_cmd_line_args():
    # default output directory
    cmd_line_args = agave_to_megahit_cmd_line_args(['-1', 'file1', '-1', 'file2', '-2', 'file3'])
    assert cmd_line_args == '-o {} -1 file1,file2 -2 file3'.format(os.path.join(os.getcwd(), 'megahit-out'))

    # secified output directory
    cmd_line_args = agave_to_megahit_cmd_line_args(['-o', '/output/dir', '-1', 'file1', '-1', 'file2', '-2', 'file3'])
    assert cmd_line_args == '-o /output/dir -1 file1,file2 -2 file3'


def test_paired_end_conversions():
    megahit_cmd_line_args = convert_agave_args_to_megahit_cmd_line(
        ['-1', 'file1', '-2', 'file2', '-x', 'x', '-y', 'y', '-z', 'z']
    )

    assert megahit_cmd_line_args == '-1 file1 -2 file2 -x x -y y -z z'


def test_all_agave_conversions():
    megahit_cmd_line_args = convert_agave_args_to_megahit_cmd_line(
        [
            '-1', 'file1', '-x', 'x', '-1', 'file2',
            '-2', 'file3', '-y', 'y', '-2', 'file4',
            '--12', 'file5', '-z', '--12', 'file6',
            '-r', 'file7', '-r', 'file8'
        ]
    )

    assert megahit_cmd_line_args == '-1 file1,file2 -2 file3,file4 --12 file5,file6 -r file7,file8 -x x -y y -z'


def test_no_conversion():
    megahit_cmd_line_args = convert_agave_args_to_megahit_cmd_line(
        [
            '-1', 'file1,file2', '-x', 'x', '-2', 'file3,file4', '-y', 'y'
        ]
    )

    assert megahit_cmd_line_args == '-1 file1,file2 -2 file3,file4 -x x -y y'
