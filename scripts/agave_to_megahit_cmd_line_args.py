"""
Convert Agave app arguments such as

  -r file1 -r file2 -r file3 -x -y -z

to MEGAHIT command line arguments such as

  -r file1,file2,file3 -x -y -z

In addition assume the first positional argument is the output directory and give it -o.

"""
import argparse
import io


def agave_to_megahit_cmd_line_args():
    known_args, unknown_args = get_args()
    #print(known_args)
    #print(unknown_args)

    input_file_table = {
        '-1': list(),
        '-2': list(),
        '--12': list(),
        '-r': list()
    }

    additional_args = []

    unknown_arg_list = list(unknown_args)
    while len(unknown_arg_list) > 0:
        next_arg = unknown_arg_list.pop(0)
        if next_arg in input_file_table.keys():
            input_file_table[next_arg].append(unknown_arg_list.pop(0))
        else:
            additional_args.append(next_arg)

    cmd_line_args = io.StringIO()
    cmd_line_args.write('-o ')
    cmd_line_args.write(known_args.output_dir)

    for opt, arg_list in input_file_table.items():
        if len(arg_list) > 0:
            cmd_line_args.write(' {} {}'.format(opt, ','.join(arg_list)))

    print(cmd_line_args.getvalue())


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('output_dir', help='Directory for MEGAHIT output.')
    return arg_parser.parse_known_args()


if __name__ == '__main__':
    agave_to_megahit_cmd_line_args()