import os
import subprocess
from pathlib import Path
# from dotenv import load_dotenv # <-- REMOVE THIS IMPORT
import cv2
import wave
import contextlib

# Setup paths
# dir_path is no longer used for media_dir or .env loading in this context
media_dir = Path("/tmp") / "media" # Correctly points to /tmp
media_dir.mkdir(parents=True, exist_ok=True)

# Create final output folder for merged files
final_output_dir = media_dir / "final"
final_output_dir.mkdir(parents=True, exist_ok=True)

# Load env
# REMOVE THIS BLOCK ENTIRELY, as environment variables will be passed directly to Railway
# dotenv_path = dir_path.parent / ".env"
# if dotenv_path.exists():
#     load_dotenv(dotenv_path)

def generate_full_solution_video(solution: dict, video_name: str = "full_solution", resolution: str = "720p") -> Path:
    """
    Generates a Manim video visualizing the solution step-by-step.
    Supports resolution: 480p, 720p, 1080p.
    """
    # We still need a base path for the Manim script itself, which is part of your deployed code.
    # This script_path needs to be relative to where your code is deployed.
    # If visuals/generator.py is in 'your_app_root/visuals/', then the script needs to be written there.
    # Let's re-introduce a 'script_temp_dir' within /tmp for the temporary manim script.
    script_temp_dir = Path("/tmp") / "manim_scripts"
    script_temp_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_temp_dir / f"{video_name}.py" # Manim script will be written to /tmp

    output_path = media_dir / f"{video_name}.mp4" # Video output goes to /tmp/media
    scene_name = "FullSolution"

    # Resolution quality flags
    quality_flags = {
        "480p": "-ql",
        "720p": "-qm",
        "1080p": "-qh"
    }
    quality_flag = quality_flags.get(resolution, "-qm")

    steps_code = []
    for i, step in enumerate(solution["steps"], 1):
        title = step["title"].replace('"', '\\"')
        explan = step["explanation"].replace('"', '\\"')
        visual_cue = step.get("visual_cue", "").replace('"', '\\"').strip()

        visual_cue_code = ""
        if visual_cue:
            if any(symbol in visual_cue.lower() for symbol in ["=", "d/dx", "^", "∫", "+", "-", "$"]):
                visual_cue_code = f'''
        try:
            cue_obj = MathTex(r"{visual_cue.replace('d/dx', '\\frac{{d}}{{dx}}')}", font_size=32, color=YELLOW).to_edge(DOWN)
        except Exception:
            cue_obj = Text("{visual_cue}", font_size=28, color=YELLOW).to_edge(DOWN)
        '''
            else:
                visual_cue_code = f'''
        cue_obj = Text("{visual_cue}", font_size=28, color=YELLOW).to_edge(DOWN)
        '''

            visual_cue_code += '''
        self.play(FadeIn(cue_obj))
        self.wait(1.5)
        self.play(FadeOut(cue_obj))
        '''

        steps_code.append(f'''
        title{i} = Text("{title}", font_size=36)
        self.play(Write(title{i}))
        self.wait(0.5)
        body{i} = Text("{explan}", font_size=24).next_to(title{i}, DOWN)
        self.play(Write(body{i}))
        self.wait(1)
        {visual_cue_code}
        self.play(FadeOut(title{i}), FadeOut(body{i}))
        self.wait(0.5)
        ''')

    scene_code = f'''from manim import *

class FullSolution(Scene):
    def construct(self):
        {''.join(steps_code)}
'''

    script_path.write_text(scene_code, encoding="utf-8")

    cmd = [
        "manim",
        str(script_path),
        scene_name,
        "-o", str(output_path),
        quality_flag,
        "--disable_caching",
    ]

    print(f"▶️ Running Manim: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Manim Error:\n{result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd)

    return output_path


def generate_tts_audio(solution: dict, audio_name: str = "narration") -> Path:
    """
    Generates TTS audio narration using OpenAI or pyttsx3 fallback.
    """
    transcript = f"Problem: {solution['problem']}. "
    for i, step in enumerate(solution["steps"], 1):
        transcript += f"Step {i}. {step['title']}. {step['explanation']} "

    audio_path = media_dir / f"{audio_name}.wav"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=transcript
        )
        # Write as .mp3, then convert to .wav
        mp3_temp = media_dir / f"{audio_name}.mp3"
        mp3_temp.write_bytes(resp.audio.data)

        # Convert to WAV for processing
        subprocess.run(["ffmpeg", "-y", "-i", str(mp3_temp), str(audio_path)], check=True)
        print(f"🔊 TTS Audio generated at {audio_path}")
    except Exception as e:
        print(f"❌ OpenAI TTS failed: {e} — falling back to pyttsx3")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(transcript, str(audio_path))
            engine.runAndWait()
            print(f"🔊 Audio fallback saved to {audio_path}")
        except Exception as e2:
            raise RuntimeError("TTS failed with both OpenAI and pyttsx3.") from e2

    return audio_path


def merge_audio_video(video_path: Path, audio_path: Path, output_name: str) -> Path:
    final_path = video_path.parent / f"{output_name}_final.mp4"

    # Get audio duration
    with contextlib.closing(wave.open(str(audio_path), 'r')) as f:
        audio_duration = f.getnframes() / float(f.getframerate())

    # Get video duration
    video = cv2.VideoCapture(str(video_path))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video_duration = frame_count / fps
    video.release()

    stretch_factor = audio_duration / video_duration
    print(f"🧮 Stretch factor: {stretch_factor:.3f} (Audio: {audio_duration:.2f}s, Video: {video_duration:.2f}s)")

    command = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-filter_complex", f"[0:v]setpts={stretch_factor}*PTS[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-c:a", "aac",
        "-shortest", str(final_path)
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✔️ Final synced video saved to: {final_path}")
        return final_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError("❌ FFmpeg merge failed.") from e