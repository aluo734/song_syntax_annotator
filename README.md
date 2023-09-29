# Song Syntax Annotator

Song syntax annotator is a GUI that helps to efficiently label the syntax of bird songs or other short bioacoustic signals. It will produce a text file in which each line contains the file name for a song and the song's syntax.

## Installation

* Download Song Syntax Annotator
* In terminal, change directories to song_syntax_annotator
* Install the dependencies with pip:

```
pip install -r requirements.txt
```

## Usage
This program processes wav files of short bioacoustic signals.
To start the GUI, run the following in your terminal:

```
python path/to/song_syntax_annotator/song_syntax_annotator.py
```

Each note can be labeled with any **single alphanumeric character**. The annotator will display a spectrogram, and the user will input a string labeling the note order, with **no spaces or separators** (e.g., abbcdddc).

The output will be a text file with two columns (song file, followed by a list of syllables). For example:

*song&nbsp;&nbsp;&nbsp;&nbsp;syntax \
file1.wav&nbsp;&nbsp;&nbsp;&nbsp;['1', '1', '3', '2', '4'] \
file2.wav&nbsp;&nbsp;&nbsp;&nbsp;['1', '2', '3'] \
file3.wav&nbsp;&nbsp;&nbsp;&nbsp;['1', '2', '3', '5']*