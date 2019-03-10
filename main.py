#!/usr/bin/python3

# Remember to push program through pylint later

import argparse
import os
import sys
import datetime

import languages
import voice_synth

from pathlib import Path
from shutil import rmtree
from googletrans import Translator


def parse_arguments():
    parser = argparse.ArgumentParser(description="""Google Translate game. The point is to translate a single text 
                                                    multiple times (max. 20) using various languages in order to see 
                                                    how much of the original meaning remains after all the tossing and 
                                                    twirling between different languages and language families.
                                                    Takes text directly from the commandline or from a .txt file""")

    parser.add_argument("text_or_path", help="A block of text to translate or path to .txt file.", \
                        type=str, nargs='?', metavar="[SOURCE]")
    parser.add_argument("target_language", help="Desired language to translate to.", \
                        type=str, nargs='?', metavar="[LANGUAGE]")
    parser.add_argument('-l', "--language_help", help="Print all usable languages.", action="store_true")
    parser.add_argument('-rm', '--remove_results', help="Remove result folder and its contents", action="store_true")

    args = parser.parse_args()

    return args


def parse_text_file(text_filepath):
    try:
        file = open(text_filepath, 'r')

        file_contents = file.read()

    finally:
        file.close()

    return file_contents


def parse_text_block(text_block):

    return text_block


def save_text_prompt():
    save_or_not = input("Would you like to save the last translation? (Y/N) ")

    if save_or_not.upper() == 'Y':
        return True
    elif save_or_not.upper() == 'N':
        return False


def write_results_file(text_block):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

    if not os.path.exists("results"):
        os.mkdir("results")


# try-finally ensures that the open file will be closed even in the case of write error

    try:
        file = open("results/gtgame"+current_datetime, 'w+')

        file.write(text_block)

    finally:
        file.close()


def remove_results_folder():
    if os.path.exists("results"):
        rmtree("results")
        print("results folder has been removed")
    else:
        sys.stderr.write("results folder does not exist\n")


def save_translation_to_file(text_block):
    if save_text_prompt() == True:
        write_results_file(text_block)


def determine_input_type(input):
    # determine if input is path to text file or simple block of text

    if not os.path.isfile(input) and Path(input).suffix != '.txt':
        return "textblock"
    elif os.path.isfile(input):
        if Path(input).suffix == '.txt':
            return "textfile"
        else:
            return input


def translate(text_block, language):
    translator = Translator()

    split_string = lambda x, n: [x[i:i + n] for i in range(0, len(x), n)]

    # so far slices of 1250 chars seem safe and do not crash the program.
    # to-do: split at 1250+number of letters to constitute a complete word,
    # so the text is not cut at incomplete words, thus causing maltranslation.
    text_chunks = split_string(text_block, 1250)
    translated_text_list = []

    for text_chunk in text_chunks:
        translated_text_chunk = translator.translate(text_chunk, language)
        translated_text_list.append(translated_text_chunk.text)

    translated_text_string = ''.join(translated_text_list)

    return translated_text_string


def main():

    args = parse_arguments()

    if args.language_help:
        languages.print_available_languages()

    elif args.remove_results:
        remove_results_folder()

    else:
        input_type = determine_input_type(args.text_or_path)
        input_stream = args.text_or_path
        iteration_counter = 1

        target_language = args.target_language

        if input_type == "textblock":
            text_to_translate = parse_text_block(input_stream)
        elif input_type == "textfile":
            text_to_translate = parse_text_file(input_stream)
        else:
            sys.stderr.write("Invalid input: {0}\n".format(input_type))
            sys.stderr.write("Run the script again with valid input (see -h --help)")
            sys.exit(-1)

        translated = translate(text_to_translate, target_language)

        print(translated)
        voice_synth.say_text(translated, target_language)
        new_translation = translated

        while True:

            try:
                desired_action = input("What language to translate to next? (input stop to quit, "
                                       "-l for available languages) ")

                if desired_action == "stop":
                    save_translation_to_file(new_translation)
                    break
                elif desired_action == "-l":
                    languages.print_available_languages()
                    pass
                else:
                    target_language = desired_action
                    iteration_counter = iteration_counter + 1
                    new_translation = translate(new_translation, target_language)

                    print(new_translation)
                    voice_synth.say_text(new_translation, target_language)
                    print("iterations: ", iteration_counter)

                    if iteration_counter == 20:
                        save_translation_to_file(new_translation)
                        break

            # maybe catch OSError @ network here?

            except ValueError:
                print("Invalid input")
                pass

            except KeyboardInterrupt:
                print("\nProgram stopped")
                break


if __name__ == "__main__":
    main()
