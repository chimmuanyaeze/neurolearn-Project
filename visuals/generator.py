import subprocess
import time
import re
from pathlib import Path
import cv2
import openai
import os
import logging
import string

# ------------------ CONFIG & LOGGING ------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")

DEFAULT_MEDIA_DIR = Path("/tmp") / "media"
DEFAULT_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
final_output_dir = DEFAULT_MEDIA_DIR / "final"
final_output_dir.mkdir(parents=True, exist_ok=True)

log_file = DEFAULT_MEDIA_DIR / "generator.log"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

# ----------------- RETRY UTILITY -----------------
def run_with_retries(func, *args, retries=3, wait=2, **kwargs):
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                logging.error(f"Function failed after {retries} attempts: {e}")
                raise
            time.sleep(wait)

# ----------------- UTILS -----------------
def sanitize_filename(name: str) -> str:
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return "".join(c for c in name if c in valid_chars).replace(" ", "_")[:50]

def cleanup_old_media(media_dir: Path, keep_recent: int = 10):
    """
    Keeps only the most recent 'keep_recent' files in media_dir to prevent disk bloat.
    """
    if not media_dir.exists():
        return
    files = sorted(media_dir.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_file in files[keep_recent:]:
        try:
            old_file.unlink()
            logging.info(f"Deleted old media file: {old_file}")
        except Exception as e:
            logging.warning(f"Failed to delete {old_file}: {e}")

# ----------------- MANIM VISUALS -----------------
def visual_to_manim_code(visuals) -> str:
    if not visuals:
        return ""
    if isinstance(visuals, dict):
        visuals = [visuals]

    code = ""
    for visual in visuals:
        vtype = visual.get("type", "")
        content = visual.get("content", "").replace('"', '\\"')
        actions = visual.get("actions", [])
        position = visual.get("position", "CENTER").upper()
        extra = visual.get("extra", {})
        obj_name = f'obj_{hash(content) % 10000}'

        if vtype == "shape":
            shape_map = {"cylinder": "Cylinder()", "rectangle": "Rectangle()", "circle": "Circle()"}
            shape_code = shape_map.get(content.lower(), f'Text("{content}", font_size=28)')
            code += f'{obj_name} = {shape_code}.to_edge({position})\n'
        elif vtype == "formula":
            code += f'{obj_name} = MathTex(r"{content}").to_edge({position})\n'
        else:
            code += f'{obj_name} = Text("{content}", font_size=28).to_edge({position})\n'

        if "color" in extra:
            code += f'{obj_name}.set_color({extra["color"].upper()})\n'
        if "scale" in extra:
            code += f'{obj_name}.scale({extra["scale"]})\n'

        for act in actions:
            act_lower = act.lower()
            if "draw" in act_lower or "fade in" in act_lower or "write" in act_lower:
                if vtype == "formula" and "write" in act_lower:
                    code += f'self.play(Write({obj_name}))\n'
                else:
                    code += f'self.play(FadeIn({obj_name}))\n'
            if "fade out" in act_lower:
                code += f'self.play(FadeOut({obj_name}))\n'
            if "highlight" in act_lower:
                code += f'self.play({obj_name}.animate.set_color(YELLOW))\n'
            if "move" in act_lower:
                match = re.search(r"(right|left|up|down)(?: (\d+(?:\.\d+)?))?", act_lower)
                if match:
                    dir_map = {"right": "RIGHT", "left": "LEFT", "up": "UP", "down": "DOWN"}
                    dir_str = match.group(1)
                    dist = float(match.group(2)) if match.group(2) else 1.0
                    code += f'self.play({obj_name}.animate.shift({dir_map[dir_str]}*{dist}))\n'
            if "scale" in act_lower:
                code += f'self.play(ScaleInPlace({obj_name}, 0.7))\n'
            if "rotate" in act_lower:
                code += f'self.play(Rotate({obj_name}, angle=PI/4))\n'

        code += "self.wait(1)\n"
    return code

# ----------------- VIDEO GENERATION -----------------
def generate_full_solution_video(solution: dict, video_name: str = "full_solution",
                                 resolution: str = "720p",
                                 media_dir: Path = DEFAULT_MEDIA_DIR,
                                 progress_callback=None) -> Path:
    video_name = sanitize_filename(video_name)
    media_dir.mkdir(parents=True, exist_ok=True)
    cleanup_old_media(media_dir)

    def _generate():
        script_temp_dir = media_dir / "manim_scripts"
        script_temp_dir.mkdir(parents=True, exist_ok=True)
        script_path = script_temp_dir / f"{video_name}.py"
        output_path = media_dir / f"{video_name}.mp4"

        use_3d = any(
            any(v.get("type") == "shape" and v.get("content", "").lower() == "cylinder"
                for v in step.get("visual", [])) for step in solution.get("steps", [])
        )
        scene_class = "ThreeDScene" if use_3d else "Scene"
        scene_name = "FullSolution"

        quality_flags = {"480p": "-ql", "720p": "-qm", "1080p": "-qh"}
        quality_flag = quality_flags.get(resolution, "-qm")

        steps = solution.get("steps", [])
        total_steps = len(steps)
        steps_code = []

        for i, step in enumerate(steps, 1):
            title = step.get("title", f"Step {i}").replace('"', '\\"')
            explan = step.get("explanation", "").replace('"', '\\"')
            visuals = step.get("visual", [])
            visual_code = visual_to_manim_code(visuals)
            steps_code.append(f'''
            title{i} = Text("{title}", font_size=36).to_edge(UP)
            title{i}.scale_to_fit_width(config.frame_width - 1)
            self.play(Write(title{i}))
            self.wait(0.5)
            body{i} = Text("{explan}", font_size=24).next_to(title{i}, DOWN)
            self.play(Write(body{i}))
            self.wait(1)
            {visual_code}
            self.play(FadeOut(title{i}), FadeOut(body{i}))
            self.wait(0.5)
            ''')

        scene_code = f'''from manim import *

class {scene_name}({scene_class}):
    def construct(self):
        {''.join(steps_code)}
        '''
        script_path.write_text(scene_code, encoding="utf-8")
        logging.info(f"Manim script written to {script_path}")

        cmd = ["manim", str(script_path), scene_name, "-o", str(output_path),
               quality_flag, "--disable_caching"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        frame_count = 0
        start_time = time.time()
        for line in process.stdout:
            if "Writing frame" in line:
                frame_count += 1
                if progress_callback:
                    elapsed = time.time() - start_time
                    progress = min(frame_count / max(total_steps * 5, 1), 1.0)
                    eta = (elapsed / max(progress, 1e-5)) * (1 - progress)
                    progress_callback(progress, eta)
        process.wait()
        if process.returncode != 0:
            logging.error(f"Manim failed: returncode={process.returncode}")
            raise subprocess.CalledProcessError(process.returncode, cmd)
        if progress_callback:
            progress_callback(1.0, 0)
        logging.info(f"Video generated at {output_path}")
        return output_path

    return run_with_retries(_generate, retries=3, wait=3)

# ----------------- TTS GENERATION -----------------
def generate_tts_audio(solution: dict, audio_name: str = "narration",
                       media_dir: Path = DEFAULT_MEDIA_DIR,
                       progress_callback=None) -> Path:
    audio_name = sanitize_filename(audio_name)
    media_dir.mkdir(parents=True, exist_ok=True)
    cleanup_old_media(media_dir)

    def _generate():
        audio_path = media_dir / f"{audio_name}.mp3"
        steps = solution.get("steps", [])
        text_chunks = [f"{step['title']}: {step['explanation']}" for step in steps]
        full_text = " ".join(text_chunks)

        try:
            audio_data = openai.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=full_text,
                format="mp3"
            )
            with open(audio_path, "wb") as f:
                f.write(audio_data.read())
            logging.info(f"TTS audio generated at {audio_path}")
        except Exception as e:
            logging.error(f"TTS generation failed: {e}")
            raise

        if progress_callback:
            progress_callback(1.0, 0)
        return audio_path

    return run_with_retries(_generate, retries=3, wait=2)

# ----------------- MERGE AUDIO & VIDEO -----------------
def merge_audio_video(video_path: Path, audio_path: Path, output_name: str,
                      media_dir: Path = DEFAULT_MEDIA_DIR,
                      progress_callback=None) -> Path:
    output_name = sanitize_filename(output_name)
    media_dir.mkdir(parents=True, exist_ok=True)
    cleanup_old_media(media_dir)

    def _merge():
        final_path = media_dir / f"{output_name}_final.mp4"
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
            audio_duration = float(subprocess.check_output(cmd))
        except Exception:
            audio_duration = 10.0

        video = cv2.VideoCapture(str(video_path))
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video_duration = frame_count / fps if fps else 1.0
        video.release()

        stretch_factor = audio_duration / video_duration
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-filter_complex", f"[0:v]setpts={stretch_factor}*PTS[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", str(final_path)
        ]
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Merged video saved at {final_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Video merge failed: {e}")
            raise

        if progress_callback:
            progress_callback(1.0, 0)
        return final_path

    return run_with_retries(_merge, retries=2, wait=2)
