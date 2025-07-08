from chains.solution_chain import get_solution
from visuals.generator import (
    generate_full_solution_video,
    generate_tts_audio,
    merge_audio_video,
)
from pathlib import Path

def main():
    query = input("Enter your STEM question: ")
    sol = get_solution(query)

    print("\n--- Solution Breakdown ---")
    print("Restated Problem:", sol["problem"])
    for i, step in enumerate(sol["steps"], 1):
        print(f"{i}. {step['title']}: {step['explanation']}")
    print("------------------------\n")

    video_name = "solution_" + "".join(e for e in sol["problem"] if e.isalnum())[:20]
    video_path = audio_path = final_path = None

    # --- Step 1: Generate Visuals ---
    try:
        video_path = generate_full_solution_video(sol, video_name)
        print(f"✔️ Video rendered successfully at: {video_path}")
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        return

    # --- Step 2: Generate Audio ---
    try:
        audio_path = generate_tts_audio(sol, audio_name=video_name)
        print(f"✔️ Audio narration created at: {audio_path}")
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return

    # --- Step 3: Merge ---
    if video_path and audio_path:
        try:
            final_path = merge_audio_video(video_path, audio_path, output_name=video_name)
            print(f"🎉 Final merged video at: {final_path}")
        except Exception as e:
            print(f"❌ Merge failed: {e}")
    else:
        print("⚠️ Skipping merge due to missing video or audio.")

if __name__ == "__main__":
    main()
