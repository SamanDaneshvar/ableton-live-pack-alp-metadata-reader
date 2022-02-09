import csv
import os
import re


def read_alp_metadata_from_file(alp_file_path):
    """Read an ALP file and return its metadata (and sometimes a few lines around it) as a string."""

    MAX_LINES_TO_READ = 1000
    num_lines_to_read = 0

    # Read the first few lines from the top of the file.
    # This lines contain all the metadata that we are looking for.
    with open(alp_file_path, mode='rb') as alp_file:
        # lines = alp_file.readlines()
        lines = []

        for i in range(MAX_LINES_TO_READ):
            binary_line = alp_file.readline()
            try:
                line = binary_line.decode('utf-8')
            except:
                line = '*Could not decode this line.*\n'

            # In this line, look for the keywords that mark the beginning of the metadata.
            # If found, break, so that we get to the other *for* loop below.
            if 'FolderConfigData' in line:
                num_lines_to_read = 11
                # print('* Metadata began on line {} for file "{}"'.format(i + 1, alp_file_path))
                break
            elif '"patcher"' in line:
                num_lines_to_read = 9
                # print('* Metadata began on line {} for file "{}"'.format(i + 1, alp_file_path))
                break

        if num_lines_to_read == 0:
            # This means that in the *for* loop above, none of the keywords that mark the beginning of the metadata
            # were found.
            print('** ERROR: No metadata keyword was spotted on file "{}"'.format(alp_file_path))
            pass
        else:
            # Record this line.
            lines.append(line)
            # Record the appropriate number of lines that follow this line.
            for i in range(num_lines_to_read - 1):
                binary_line = alp_file.readline()
                try:
                    line = binary_line.decode('utf-8')
                except:
                    line = '*Could not decode this line.*\n'

                lines.append(line)

        return ''.join(lines)


def parse_alp_metadata(metadata_str):
    """Parse the metadata of an ALP file.

    Args:
        metadata_str: A string containing the metadata of an ALP file.
    Returns:
        metadata_dict: A Python dictionary containing the parsed metadata of the ALP file.
    """

    REGEX_PATTERNS = {
        'FolderConfigData': {
            'name': r'String PackDisplayName = "(.*)";',
            'vendor': r'String PackVendor = "(.*)";',
            'version_major': r'Int PackMajorVersion = (.*);',
            'version_minor': r'Int PackMinorVersion = (.*);',
            'version_revision': r'Int PackRevision = (.*);',
        },
        'Patcher': {
            'version_major': r'"major" : (.*),',
            'version_minor': r'"minor" : (.*),',
            'version_revision': r'"revision" : (.*),',
        },
    }

    metadata_dict = {}

    # Decide which series of patterns to use.
    if 'FolderConfigData' in metadata_str:
        patterns = REGEX_PATTERNS['FolderConfigData']
    elif '"patcher"' in metadata_str:
        patterns = REGEX_PATTERNS['Patcher']
    else:
        # The metadata string is non-standard for our purposes. Exit the function and return an empty dictionary.
        return {}

    for key in patterns:
        match = re.search(patterns[key], metadata_str)
        if match:
            metadata_dict[key] = match.group(1)
        else:
            # No match for this pattern.
            metadata_dict[key] = None

    return metadata_dict


def main():
    """The main function"""

    ALPS_DIR = 'data'
    REPORT_FILE_PATH = 'data/report.csv'
    COLUMN_NAMES = ['Filename', 'Name', 'Vendor', 'Version']

    # Write the header of the report CSV file.
    # In the 'w' mode, if a file with the same name exists, it will be overwritten.
    with open(REPORT_FILE_PATH, 'w', encoding='utf-8', newline='') as report_file:
        writer = csv.writer(report_file)
        writer.writerow(COLUMN_NAMES)

    file_and_folder_names = os.listdir(ALPS_DIR)
    for file_name in file_and_folder_names:
        if file_name[-4:].lower() == '.alp':
            metadata_str = read_alp_metadata_from_file(os.path.join(ALPS_DIR, file_name))
            metadata_dict = parse_alp_metadata(metadata_str)

            # print(metadata_str)
            print(metadata_dict)

            # Assemble the version string.
            if metadata_dict.get('version_major') or metadata_dict.get('version_minor') or metadata_dict.get('version_revision'):
                version = 'v{}.{} r{}'.format(metadata_dict.get('version_major'),
                                              metadata_dict.get('version_minor'),
                                              metadata_dict.get('version_revision'))
            else:
                # None of the version components exist. Therefore, there is no point in concatenating them.
                # (The result would have been "vNone.None rNone".)
                version = None

            # Write the metadata of this ALP file onto a new row on the report file.
            # In the 'a' mode, new lines will be appended to the existing file.
            with open(REPORT_FILE_PATH, 'a', encoding='utf-8', newline='') as report_file:
                writer = csv.writer(report_file)
                writer.writerow([file_name,
                                 metadata_dict.get('name'),
                                 metadata_dict.get('vendor'),
                                 version])


main()
