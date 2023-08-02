#!/usr/bin/python3

# Passwords Please
# Author: e-nzym3 (https://github.com/e-nzym3)

import argparse
from datetime import datetime
import re

# A list which contains current year, and previous year, generated based on current date.
year = datetime.now().year
year_minus_one = year - 1
year_list = [year, year_minus_one]

# A list containing all months within a year.
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

# A list containing all days within a week.
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# A list containing all seasons
seasons = ["spring", "summer", "autumn", "winter", "autumn"]

# A list containing commonly used default passwords.
common_passwords = ["password", "passw0rd", "pass", "welcome", "changeme", "changeMe"]

# Same as above, but extended
common_passwords_extended = ["p@55word", "passwerd", "passw0rd3", "passw", "welc0me", "covid", "trump", "biden"]

# A list containing all common symbols/number/year combos found trailing in passwords.
trailers = ["!", "@", "#", "$", "?", ".", "123", "123!", "1234", "123$", "123#", str(year), str(year_minus_one), str(year)+"!", str(year)+"@", str(year)+"#", str(year)+"$", str(year_minus_one)+"!", str(year_minus_one)+"@", str(year_minus_one)+"#", str(year_minus_one)+"$"]

# Dictionary that will contain chosed default sets
defaults = []


def argument_handler():
    parser = argparse.ArgumentParser(description="Passwords Please! - A companion for generating passwords for password spraying. (https://github.com/e-nzym3/passpls)", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-i",
        "--input",
        help="(Optional) File containing a list of passwords to be modified. If not specified, will generate a default list using months (-d m), common passwords (-d c), and seasons (-d s).",
        type=argparse.FileType("r"),
        required=False
    )
    parser.add_argument(
        "-o",
        "--output",
        help="(Optional) File to which the modified passwords will be written. If not specified, will write to '[local directory]/modified_passwords.txt'.",
        type=argparse.FileType("w"),
        default="modified_passwords.txt",
        required=False
    )
    parser.add_argument(
        "-m",
        "--modifiers",
        metavar="x",
        help="(Optional) Modifiers to be used while processing the input file. (Defaults to 't l y r'.) \n    Example: '-m t y w'\n* Available modifiers are: \n  t (title), \n  l (lowercase), \n  u (uppercase), \n  y (years), \n  r (common trailers), \n  w (Windows/AD Compliant).",
        nargs="+",
        default=["t", "l", "r"]
    )
    parser.add_argument(
        "-d",
        "--defaults",
        metavar="x",
        help="(Optional) Use pre-defined default/common passwords during processing. \n    Example: '-d s m c' \n* Available lists for these include:\n  s (seasons), \n  d (days of the week), \n  c (common/default passwords), \n  e (extended common/default passwords), \n  m (months of the year).",
        nargs="+",
        required=False
    )
    args = parser.parse_args()

    # Constructing a list of chosen default passwords.
    if args.defaults:
        if "s" in args.defaults:
            defaults.extend(seasons)
        if "m" in args.defaults:
            defaults.extend(months)
        if "d" in args.defaults:
            defaults.extend(days)
        if "c" in args.defaults:
            defaults.extend(common_passwords)
        if "e" in args.defaults:
            defaults.extend(common_passwords_extended)

    # Checking if input file contains passwords.
    if args.input:
        input_file = args.input
        input_file_content = input_file.readlines()
        input_file_content = [pw.strip() for pw in input_file_content]
        input_file.close()
        args.input = input_file_content
    if args.input is None:
        print("No input file provided. Using default password lists.")
        if args.defaults:
            args.input = defaults
        else:
            args.input = common_passwords + months + seasons
    return args


# Module which accepts a password list and modifies it based on the selected modifiers.
def modify_passwords(password_list, modifier):
    passwords = []
    if "t" in modifier:
        passwords = [pw.title() for pw in password_list]
    elif "l" in modifier:
        passwords = [pw.lower() for pw in password_list]
    elif "u" in modifier:
        passwords = [pw.upper() for pw in password_list]
    elif "y" in modifier:
        passwords = [pw.replace(pw, pw + str(year)) for pw in password_list]
        passwords.extend([pw.replace(pw, pw + str(year_minus_one)) for pw in password_list])
        passwords.extend([pw.replace(pw, pw + str(year)[2:4]) for pw in password_list])
        passwords.extend([pw.replace(pw, pw + str(year_minus_one)[2:4]) for pw in password_list])
    elif "r" in modifier:
        for trailer in trailers:
            passwords.extend([pw.replace(pw, pw + trailer) for pw in password_list])
    
    # Deduplicate the list of passwords before returning it
    modified_passwords = list(set(passwords))
    return modified_passwords


def is_ad_compliant(password):
    # Check if password matches Active Directory complexity requirements
    x = 0
    while True:
        if re.search(r"[a-z]", password):
            x += 1
        if re.search(r"[A-Z]", password):
            x += 1
        if re.search(r"[0-9]", password):
            x += 1
        if re.search(r"[\`\~\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\{\}\\\|\;\:\'\"\,\<\.\>\/\?]", password):
            x += 1
        if x >= 3:
            return True
        else:
            return False


if __name__ == "__main__":
    args = argument_handler()
    password_list = args.input
    total_pass = {}

    # If there are multiple modifiers specified within the command, process them in a nested manner to generate the appropriate list of all requested permutations.
    if len(args.modifiers) > 1:
        final_list = []
        # Create a dictionary of all possible combinations of the password list and modifiers selected.
        for modifier in args.modifiers:
            if modifier == "w":
                continue
            total_pass[modifier] = modify_passwords(password_list, modifier)
            args.modifiers.remove(modifier)
            for rem_mod in args.modifiers:
                total_pass[rem_mod+modifier] = modify_passwords(total_pass[modifier], rem_mod)
        
        # Remove combos which are not useful, such as years + trailers.
        all_keys=list(total_pass.keys())
        for key in all_keys:
            if "y" in key and "r" in key:
                total_pass.pop(key)
        
        # Construct the final list of passwords
        for value in total_pass.values():
            final_list.extend([("{}\n".format(pw)) for pw in value])
        final_list = set(final_list)

        # Check if AD compliant (if set)
        print(args.modifiers)
        if "w" in args.modifiers:
            compliant_list = final_list.copy()
            for pw in final_list:
                if not is_ad_compliant(pw):
                    compliant_list.remove(pw)
            final_list = compliant_list
        print("Generating passwords...")
        try:
            args.output.writelines(sorted(set(final_list)))
        except:
            print("Something went wrong with writing to file!")
        print("Done!")

    # If there's only one modifier specified within hte command, process it as normal.
    elif len(args.modifiers) == 1:
        modified_passwords = modify_passwords(password_list, args.modifiers)
        print("Generating passwords...")
        try:
            args.output.writelines(sorted(set("{}\n".format(pw) for pw in modified_passwords)))
        except:
            print("Something went wrong with writing to file!")
        print("Done!")
    args.output.close()