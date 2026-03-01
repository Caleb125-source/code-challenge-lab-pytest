"""
test_palindrome.py
==================
Pytest test suite for longest_palindromic_substring().

Follows TDD: these tests are written to FAIL against the stub (pass),
then PASS once the function is implemented.

"""

import pytest
from palindrome import longest_palindromic_substring


# Helper

def is_palindrome(s: str) -> bool:
    """Return True if s reads the same forwards and backwards."""
    return s == s[::-1]


# 1. Basic / happy-path cases

@pytest.mark.parametrize("input_str, valid_answers", [
    ("babad",   {"bab", "aba"}),   # two equally valid answers
    ("cbbd",    {"bb"}),
    ("racecar", {"racecar"}),
    ("noon",    {"noon"}),
    ("abacaba", {"abacaba"}),
])
def test_basic_cases(input_str, valid_answers):
    """Common inputs should return one of the accepted palindromic answers."""
    result = longest_palindromic_substring(input_str)
    assert result in valid_answers, (
        f"Input '{input_str}': expected one of {valid_answers}, got '{result}'"
    )


# 2. Whole-string palindromes

@pytest.mark.parametrize("palindrome", [
    "aba",
    "abba",
    "abcba",
    "racecar",
    "madam",
    "level",
    "12321",
    "amanaplanacanalpanama",
])
def test_whole_string_is_palindrome(palindrome):
    """When the entire input is a palindrome, the function returns the full string."""
    assert longest_palindromic_substring(palindrome) == palindrome


# 3. Single-character strings  (len == 1 — lower boundary of the constraint)

def test_single_character_letter():
    """A single letter is a palindrome of length 1."""
    assert longest_palindromic_substring("a") == "a"


def test_single_character_digit():
    """A single digit is a palindrome of length 1."""
    assert longest_palindromic_substring("7") == "7"


def test_single_character_z():
    assert longest_palindromic_substring("z") == "z"


# 4. Two-character strings

def test_two_identical_characters():
    """'aa' — both characters match, whole string is a palindrome."""
    assert longest_palindromic_substring("aa") == "aa"


def test_two_different_characters():
    """'ac' — characters differ; either single character is valid."""
    result = longest_palindromic_substring("ac")
    assert result in {"a", "c"}, f"Expected 'a' or 'c', got '{result}'"
    assert len(result) == 1


# 5. Even-length palindromes

def test_even_length_bb():
    """'cbbd' contains even-length palindrome 'bb'."""
    assert longest_palindromic_substring("cbbd") == "bb"


def test_even_length_abba():
    """'abba' is itself an even-length palindrome."""
    assert longest_palindromic_substring("abba") == "abba"


def test_even_length_embedded():
    """'xyzabbauvw' — 'abba' is buried inside."""
    assert longest_palindromic_substring("xyzabbauvw") == "abba"


def test_even_length_noon():
    assert longest_palindromic_substring("noon") == "noon"


# 6. Multiple valid answers

def test_multiple_valid_babad():
    """'babad' — 'bab' and 'aba' are equally long; either is correct."""
    result = longest_palindromic_substring("babad")
    assert result in {"bab", "aba"}, f"Expected 'bab' or 'aba', got '{result}'"
    assert is_palindrome(result)
    assert len(result) == 3


def test_multiple_valid_single_char():
    """'ac' — 'a' and 'c' are equally long; either is correct."""
    result = longest_palindromic_substring("ac")
    assert result in {"a", "c"}
    assert len(result) == 1


# 7. Palindrome position variants

def test_palindrome_at_start():
    """'aabcd' — palindrome 'aa' sits at the very beginning."""
    assert longest_palindromic_substring("aabcd") == "aa"


def test_palindrome_at_end():
    """'abcdaa' — palindrome 'aa' sits at the very end."""
    assert longest_palindromic_substring("abcdaa") == "aa"


def test_palindrome_in_middle():
    """'abcbad' — odd-length palindrome 'abcba' spans the middle."""
    assert longest_palindromic_substring("abcbad") == "abcba"


def test_palindrome_surrounded_by_noise():
    """'xyzracecarzyx' — 'racecar' is the longest palindrome."""
    assert longest_palindromic_substring("xyzracecarzyx") == "xyzracecarzyx"


# 8. No palindrome longer than 1

def test_no_palindrome_abcd():
    """'abcd' — all characters differ; answer is any single character."""
    result = longest_palindromic_substring("abcd")
    assert len(result) == 1
    assert result in set("abcd")
    assert is_palindrome(result)


def test_no_palindrome_strictly_increasing():
    result = longest_palindromic_substring("abcde")
    assert len(result) == 1
    assert is_palindrome(result)


# 9. Mixed digits and letters

def test_digits_only():
    """A numeric palindrome — function must handle digit characters."""
    assert longest_palindromic_substring("12321") == "12321"


def test_mixed_digits_and_letters():
    """'a1221b' — the palindrome '1221' lives between letters."""
    assert longest_palindromic_substring("a1221b") == "1221"


def test_digits_no_palindrome():
    """'1234' — no repeating digits; answer is a single digit."""
    result = longest_palindromic_substring("1234")
    assert len(result) == 1
    assert is_palindrome(result)


# 10. Long / stress inputs

def test_all_same_characters_1000():
    """1000 identical characters — the entire string is the palindrome."""
    s = "a" * 1000
    assert longest_palindromic_substring(s) == s


def test_long_string_with_embedded_palindrome():
    """Embed a 51-char palindrome; it must be detected even inside noise."""
    center = "b" * 51            # odd-length palindrome of 51 chars
    noise  = "ac" * 100          # 200-char non-palindromic wrapper each side
    s = noise + center + noise
    result = longest_palindromic_substring(s)
    assert is_palindrome(result)
    assert len(result) >= 51


def test_alternating_characters():
    """'ababababab' — longest palindrome is the whole string (odd count)."""
    s = "ababababab"
    result = longest_palindromic_substring(s)
    assert is_palindrome(result)
    assert len(result) >= 9   # 'ababababa' spans 9 chars


# 11. Return-value invariants (must hold for ANY valid input)

@pytest.mark.parametrize("input_str", [
    "a", "ab", "abc", "abba", "racecar", "babad", "cbbd",
    "noon", "12321", "a" * 50,
])
def test_result_is_always_a_palindrome(input_str):
    """Whatever is returned MUST itself be a palindrome."""
    result = longest_palindromic_substring(input_str)
    assert is_palindrome(result), (
        f"Result '{result}' for input '{input_str}' is not a palindrome"
    )


@pytest.mark.parametrize("input_str", [
    "a", "ab", "abc", "abba", "racecar", "babad", "cbbd",
    "noon", "12321", "a" * 50,
])
def test_result_is_always_a_substring(input_str):
    """Whatever is returned MUST be a contiguous substring of the input."""
    result = longest_palindromic_substring(input_str)
    assert result in input_str, (
        f"'{result}' is not a substring of '{input_str}'"
    )


@pytest.mark.parametrize("input_str", [
    "a", "ab", "abc", "abba", "racecar", "babad", "cbbd",
])
def test_result_length_is_at_least_one(input_str):
    """Result must always contain at least one character."""
    result = longest_palindromic_substring(input_str)
    assert len(result) >= 1


# 12. Failure / type-guard cases

def test_integer_input_raises_error():
    """An integer argument should raise TypeError or AttributeError."""
    with pytest.raises((TypeError, AttributeError)):
        longest_palindromic_substring(12321)


def test_none_input_raises_error():
    """None should raise TypeError or AttributeError."""
    with pytest.raises((TypeError, AttributeError)):
        longest_palindromic_substring(None)


def test_float_input_raises_error():
    """A float should raise TypeError or AttributeError."""
    with pytest.raises((TypeError, AttributeError)):
        longest_palindromic_substring(3.14)