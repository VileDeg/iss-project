# iss-project

Final project from [signals and systems university course](https://www.fit.vut.cz/study/course/ISS/.en).

The project is about signal processing and sound generation.

Briefly, the task was to generate an audio file containing piano melody from text file describing piano tones for each moment in time. From that description the audio file must be generated.

## Input of the project

An audio file containing all piano tones (`src/klavir.wav`) and a text file describing piano tones for each moment in time of the target audio file that needs to be generated (`src/skladba.txt`).

## Output of the project

Generated audio files with 8K and 48K frequencies (`audio/out_8k.wav` and `audio/out_48k.wav`).

## Run

To run the project, execute `src/xgonce00_e.ipynb` jupyter notebook containing all stages of the project task.

## Libs

Required libraries: `numpy`, `matplotlib`, `soundfile`, `scipy`

