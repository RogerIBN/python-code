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
00:02
vamos
"""

    expected_text = """\
1
00:00:00,00 --> 00:00:01,00
Hola

2
00:00:01,00 --> 00:00:02,00
Adiós

3
00:00:02,00 --> 00:00:05,00
Vamos

"""
    # Act
    output_text = srt_from_raw_youtube(input_text=input_text)

    # Assert
    assert output_text == expected_text, "The output text is not the expected."

    input_text = """\
00:00
español
00:05
inglés
00:10
francés
"""

    expected_text = """\
1
00:00:00,00 --> 00:00:05,00
Español

2
00:00:05,00 --> 00:00:10,00
Inglés

3
00:00:10,00 --> 00:00:15,00
Francés

"""
    # Act
    output_text = srt_from_raw_youtube(input_text=input_text, seg=5)

    # Assert
    assert output_text == expected_text, "The output text is not the expected."
