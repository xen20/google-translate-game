from beautifultable import BeautifulTable
import googletrans


def print_available_languages():
    available_languages = googletrans.LANGUAGES
    language_keys_list = list(available_languages.keys())
    language_values_list = list(available_languages.values())

    # pad the lists for easier table manipulation by using modulus for decision when to put new column
    # 120 is divisible by 15 w/o remainder, 106 values in key_list/value list

    language_keys_list += [''] * (121 - len(language_keys_list))
    language_values_list += [''] * (121 - len(language_values_list))

    language_table = BeautifulTable(max_width=1000)
    language_table.set_style(BeautifulTable.STYLE_COMPACT)

    for idx in range(1, len(language_keys_list)):
        if idx % 15 == 0:
            sliced_keys_list = language_keys_list[idx - 15:idx]
            sliced_values_list = language_values_list[idx - 15:idx]

            language_table.append_column("Code", sliced_keys_list)
            language_table.append_column("Language", sliced_values_list)

    print(language_table)
