import os
import subprocess
from pathlib import Path
import cv2
import wave
import contextlib

# Setup paths
media_dir = Path("/tmp") / "media"
media_dir.mkdir(parents=True, exist_ok=True)

# Create final output folder for merged files
final_output_dir = media_dir / "final"
final_output_dir.mkdir(parents=True, exist_ok=True)

def generate_full_solution_video(solution: dict, video_name: str = "full_solution", resolution: str = "720p") -> Path:
    """
    Generates a Manim video visualizing the solution step-by-step.
    """
    script_temp_dir = Path("/tmp") / "manim_scripts"
    script_temp_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_temp_dir / f"{video_name}.py" # Manim script will be written to /tmp

    output_path = media_dir / f"{video_name}.mp4" # Video output goes to /tmp/media
    scene_name = "FullSolution"

    # Quality flags from the reverted code (defaulting to -qm for 720p)
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
    Generates a silent placeholder audio track.
    (OpenAI TTS is disabled due to exceeded quota, and pyttsx3 does not work in this environment.)
    """
    audio_path = media_dir / f"{audio_name}.wav"
    
    print("⚠️ OpenAI TTS disabled due to quota. Generating silent audio placeholder.")

    # Use ffmpeg to generate a 10-second silent WAV file
    # This ensures the merge_audio_video function has an audio track to work with.
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "10", str(audio_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"🔊 Silent audio placeholder generated at {audio_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("❌ FFmpeg failed to generate silent audio. Check your FFmpeg installation.") from e
    
    return audio_path


def merge_audio_video(video_path: Path, audio_path: Path, output_name: str) -> Path:
    final_path = video_path.parent / f"{output_name}_final.mp4"

    # Get audio duration
    try:
        with contextlib.closing(wave.open(str(audio_path), 'r')) as f:
            audio_duration = f.getnframes() / float(f.getframerate())
    except wave.Error as e:
        # Handle case if the audio file generated above is not a valid WAV header, 
        # though ffmpeg should produce a valid one.
        print(f"Error reading WAV duration: {e}. Attempting FFmpeg duration check.")
        # Fallback to ffprobe or simpler duration check if wave.open fails
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)]
            audio_duration = float(subprocess.check_output(cmd))
        except Exception as e:
            print(f"Failed to get audio duration with FFmpeg: {e}. Assuming 10s for silent track.")
            audio_duration = 10.0 # Default duration for silent track


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