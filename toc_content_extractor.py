from collections import Counter
import re
import unicodedata

class TocContentExtractor:
    def __init__(self, toc_search_min_length: int = 6, toc_max_level: int = 3):
        self.toc_search_min_length = toc_search_min_length
        self.toc_max_level = toc_max_level

    def find_closest_match(self, matches, N):
        """Returns the match from matches that is closest in length to N."""
        if not matches:
            return None

        closest_match = min(matches, key=lambda m: abs(len(m.group(1)) - N))
        return closest_match

    def normalize(self, text):
        """
        Normalizes the text, ignoring differences between full-width and half-width characters.
        """
        # Convert the string to the normalized form 'NFKC'
        text = unicodedata.normalize("NFKC", text)
        # Remove spaces
        return re.sub(r"[\s\u3000]+", "", text.lower())

    def generate_filtered_toc(self, toc_list, toc_max_level):
        """
        Generates a table of contents from Markdown text, filters it to include only hierarchies 
        below the specified level, and removes duplicates and short strings.

        Args:
            markdown_text: Text in Markdown format.
            toc_max_level: The maximum header level to filter (default is 2, up to ##).
            # toc_search_min_length: The minimum string length to remove (default is 4).

        Returns:
            A list of table of contents (string list) below the specified level hierarchy. 
            May return an empty list.
        """

        # Level determination and filtering
        filtered_toc = []
        for item in toc_list:
            if bool(re.match(r"^#{1,6}\s", item)) == False:
                continue
            item = item.strip()
            level = len(item) - len(item.lstrip("# ")) - 1  # Determine the level by the number of '#'
            if level <= toc_max_level:
                filtered_toc.append(item)

        # Remove duplicates and short strings
        # filtered_array = [item.strip() for item in filtered_toc if len(item.strip()) > self.toc_search_min_length]
        counts = Counter(filtered_toc)
        return [item for item in filtered_toc if counts[item] == 1]

    def convert_toc_to_regex(self, toc):
        """
        Converts a TOC to a regular expression format.
        """
        normalized_line = self.normalize(toc)
        pattern = re.sub(r"[#\s]+", r".*", re.escape(normalized_line))
        return re.compile(pattern).pattern

    def extract_content_by_toc(self, toc_text: str, content: str):
        """
        Extracts the corresponding section from the content using the TOC.
        """
        result = []
        normalized_content = self.normalize(content)
        search_start = 0  # Manage the starting position of the search

        toc_list = toc_text.splitlines()
        toc_list = self.generate_filtered_toc(toc_list, self.toc_max_level)
        for i, toc_line in enumerate(toc_list):
            # Extract the range up to the next heading
            next_toc_line = None
            if i + 1 < len(toc_list):
                next_toc_line = toc_list[i + 1]

                # Search for the text corresponding to the current section
                next_toc_line_temp = next_toc_line.lstrip("#").lstrip(" ")
            toc_line_temp = toc_line.lstrip("#").lstrip(" ")

            while True:
                target_text = normalized_content[search_start:]
                if next_toc_line:
                    regex_patterns = f"({self.convert_toc_to_regex(toc_line_temp)})(.*?)(?={self.convert_toc_to_regex(next_toc_line_temp)})"
                    regex_patterns = (
                        f"(.*?)(?={self.convert_toc_to_regex(next_toc_line_temp)})"
                    )
                else:
                    regex_patterns = f"({self.convert_toc_to_regex(toc_line_temp)})(.*)"
                    regex_patterns = f"(.*)"
                matches = list(re.finditer(regex_patterns, target_text, re.DOTALL))
                if len(matches) > 0:
                    break
                else:
                    if i == 0:
                        toc_line_temp = toc_line_temp[1:-1]
                        next_toc_line_temp = next_toc_line_temp[1:-1]
                    elif i == len(toc_list) - 1:
                        toc_line_temp = toc_line_temp[1:-1]
                    else:
                        next_toc_line_temp = next_toc_line_temp[1:-1]

                    if (
                        len(toc_line_temp) < self.toc_search_min_length
                        or len(next_toc_line_temp) < self.toc_search_min_length
                    ):
                        print(f"match failed :{next_toc_line}")
                        break

            # Select the longest content among the matches
            # longest_match = self.find_closest_match(matches, N=1000)
            # longest_match = max(matches, key=lambda m: len(m.group(1)), default=None)

            # if longest_match:
            if len(matches) > 0:
                longest_match = matches[0]

                extracted_text = longest_match.group(1).strip()
                print(f"match success :{next_toc_line} length:{len(extracted_text)}")
                # Add to the result while keeping the original TOC format
                result.append(toc_line)
                result.append(re.sub(r"\\s+", "", extracted_text))
                # Update the search start position (start searching from the next position after the last hit)
                search_start += longest_match.end()
            print(search_start)
        return "\n".join(result)