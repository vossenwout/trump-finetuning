import assemblyai as aai
import yt_dlp
from dotenv import load_dotenv
import os

"""
Script used to get raw transcripts from youtube.
Note that some manual cleaning is still necessary to identify TRUMP and clean up the transcript.
I manually clean it and then move it to the clean folder.
"""
load_dotenv("config/.env")

assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not assemblyai_api_key:
    raise ValueError("ASSEMBLYAI_API_KEY is not set")

aai.settings.api_key = assemblyai_api_key
transcriber = aai.Transcriber()


def _get_youtube_audio(youtube_url: str) -> tuple[str, str]:
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(youtube_url, download=False)

    for format in info["formats"][::-1]:
        if format["resolution"] == "audio only" and format["ext"] == "m4a":
            return info["title"], format["url"]

    raise ValueError("No audio url found")


def download_youtube_audio(youtube_url: str, output_dir: str = "data/audio") -> str:
    """
    Downloads the best m4a audio from YouTube and saves it locally.
    Returns the local file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    with yt_dlp.YoutubeDL(
        {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
            "quiet": True,
        }
    ) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        # Ensure extension is .m4a
        if not filename.endswith(".m4a"):
            filename = os.path.splitext(filename)[0] + ".m4a"
        return filename


def _transcribe_audio(url: str, title: str):
    print("Audio URL:", url)

    if url:
        print("Transcribing...")
        config = aai.TranscriptionConfig(speaker_labels=True)

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(url, config=config)
        print(transcript)
        if not transcript.utterances:
            raise ValueError(
                "Something went wrong with downloading the audio (might be protected). Please download manually"
            )

        transcript_text = ""
        for utterance in transcript.utterances:
            transcript_text += f"Speaker {utterance.speaker}: {utterance.text}\n"

        print(transcript_text)

        with open(f"data/transcripts/raw/{title}.txt", "w") as file:
            file.write(transcript_text)

        print("Transcription completed and saved to transcript.txt")


def transcribe_from_youtube(youtube_url: str, download_audio: bool = True):
    if download_audio:
        local_audio_path = download_youtube_audio(youtube_url)
        title = os.path.splitext(os.path.basename(local_audio_path))[0]
        _transcribe_audio(url=local_audio_path, title=title)
    else:
        title, url = _get_youtube_audio(youtube_url)
        _transcribe_audio(url=url, title=title)


# Insert YT URL here
YT_URL = "https://www.youtube.com/watch?v=qCbfTN-caFI&t"

transcribe_from_youtube(YT_URL, download_audio=True)
