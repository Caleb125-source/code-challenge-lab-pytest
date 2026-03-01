def longest_palindromic_substring(s):
    """
    Given a string s, return the longest palindromic substring.

    A palindrome reads the same forwards and backwards.

    Args:
        s (str): Input string. Must be a string of digits or English letters.
                 1 <= len(s) <= 1000

    Returns:
        str: The longest palindromic substring found in s.
             If multiple substrings tie for longest, any valid one is returned.

    Examples:
        >>> longest_palindromic_substring("babad")
        'bab'
        >>> longest_palindromic_substring("cbbd")
        'bb'
        >>> longest_palindromic_substring("racecar")
        'racecar'
    """
    n = len(s)
    if n < 2:
        return s

    start = 0
    max_len = 1

    def expand_around_center(left, right):
        """Expand outward from center while characters match.
        Returns the length of the palindrome found."""
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(n):
        # Check odd-length palindromes  (single center character at i)
        len1 = expand_around_center(i, i)
        # Check even-length palindromes (center gap between i and i+1)
        len2 = expand_around_center(i, i + 1)

        max_curr_len = max(len1, len2)
        if max_curr_len > max_len:
            max_len = max_curr_len
            start = i - (max_len - 1) // 2

    return s[start:start + max_len]