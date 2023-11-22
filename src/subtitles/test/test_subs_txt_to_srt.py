"""
Test the subs_txt_to_srt.py module using pytest.
"""

from src.subtitles.subs_txt_to_srt import srt_from_raw_youtube


def test_subs_txt_to_srt() -> None:
    """
    Test case for the function `srt_from_raw_youtube` in the `subs_txt_to_srt` module.
    """
    # Arrange

    input_text = """\
00:00
hola
00:01
adiós
00:02\
"""

    expected_text = """\
1
00:00:00,00 --> 00:00:01,00
Hola

2
00:00:01,00 --> 00:00:02,00
Adiós

"""
    # Act
    output_text = srt_from_raw_youtube(input_text=input_text)

    # Assert
    assert output_text == expected_text
