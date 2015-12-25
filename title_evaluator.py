__author__ = 'anish'

"""
Class which can be configured to extract match info out of strings
"""

import re


class TitleEvaluator:

    def __init__(self, regexps):
        """
        Initial config
        are words unique to their respective matches which appear in the input strings
        :param regexps This should be a dictionary of the form {"qm": "q_pseudoregex", "qf": "qf_pseudoregex",
        "sf": "sf_pseduoregex", "f": "f_pseudoregex"}, where the pseudo-regex are built with the given syntax
        :return:
        """

        self.regexps = regexps

        symbols = {"~": "(?P<matchnum>[0-9]+)", "^": "(?P<elim_id>[0-9]+)", "&": "[0-9]+"}

        for key in self.regexps:

            sanitized_re = re.escape(self.regexps[key])

            for symbol in symbols:

                sanitized_re = sanitized_re.replace("\\" + symbol, symbols[symbol])

            print(sanitized_re)

            self.regexps[key] = re.compile(sanitized_re)

    def extract_match_id(self, title):
        """
        Return the TBA match ID given a string
        :param title: The string to generate information from
        :return: The match id if  it can extract the info, None if otherwise
        """
        for match_type, regex in self.regexps.items():

            results = re.match(regex, title)

            if results is None:
                continue

            match_id = match_type

            if match_type is not "qm":

                try:
                    elim_id = results.group("elim_id")
                except IndexError:
                    elim_id = "1"

                if elim_id is None:
                    elim_id = "1"

                match_id += elim_id + "m"

            else:
                pass

            match_id += results.group("matchnum")

            return match_id