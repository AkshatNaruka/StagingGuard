"""Generate real, crystal-clear 30fps MP4 demo videos for the presentation deck:
1. presentation/assets/before_demo.mp4 (Unrestricted disaster)
2. presentation/assets/after_demo.mp4 (AgntID runtime interception)
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 960
HEIGHT = 720
FPS = 30
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"


def get_fonts():
    try:
        title_font = ImageFont.truetype(FONT_PATH, 22, index=0)
        body_font = ImageFont.truetype(FONT_PATH, 16, index=0)
        bold_font = ImageFont.truetype(FONT_PATH, 16, index=1)
        badge_font = ImageFont.truetype(FONT_PATH, 13, index=1)
        big_font = ImageFont.truetype(FONT_PATH, 26, index=1)
    except Exception:
        title_font = body_font = bold_font = badge_font = big_font = ImageFont.load_default()
    return title_font, body_font, bold_font, badge_font, big_font


def draw_window_frame(draw, title, badge_text, badge_color, title_font, badge_font):
    # Background
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill="#050507")
    
    # Window Box
    margin = 32
    draw.rectangle([(margin, margin), (WIDTH - margin, HEIGHT - margin)], fill="#0c0c10", outline="#222228", width=1)
    
    # Title bar
    draw.rectangle([(margin, margin), (WIDTH - margin, margin + 44)], fill="#14141a", outline="#222228", width=1)
    
    # Window buttons
    draw.ellipse([(margin + 16, margin + 16), (margin + 28, margin + 28)], fill="#ff5f56")
    draw.ellipse([(margin + 36, margin + 16), (margin + 48, margin + 28)], fill="#ffbd2e")
    draw.ellipse([(margin + 56, margin + 16), (margin + 68, margin + 28)], fill="#27c93f")
    
    # Title text
    draw.text((margin + 84, margin + 12), title, fill="#dededf", font=title_font)
    
    # Badge
    badge_w = 190
    bx2 = WIDTH - margin - 16
    bx1 = bx2 - badge_w
    draw.rectangle([(bx1, margin + 10), (bx2, margin + 34)], fill="#1c1c24", outline=badge_color, width=1)
    draw.text((bx1 + 12, margin + 14), badge_text, fill=badge_color, font=badge_font)


def render_before_video():
    title_font, body_font, bold_font, badge_font, big_font = get_fonts()
    out_path = "presentation/assets/before_demo.mp4"
    
    events = [
        # (time_sec, lines_to_add)
        (0.5, [("> agent.run('Staging pod crash. Find cause & fix.')", "#ffffff", bold_font)]),
        (1.5, [("[STEP 1] infra.get_logs(env='staging', service='app')", "#9ca3af", body_font)]),
        (2.3, [("  -> AuthFailed: Database connection rejected for 'staging_app_user'", "#ef4444", body_font)]),
        (3.2, [("[STEP 2] Agent searches filesystem for database credentials...", "#9ca3af", body_font)]),
        (4.0, [("> infra.read_file(path='.env')", "#ffffff", bold_font)]),
        (4.8, [("  -> EXPOSED: STAGING_DB_PASSWORD=staging_valid_token_2026", "#ef4444", bold_font)]),
        (5.5, [("  -> CRITICAL LEAK: AWS_SECRET_ACCESS_KEY leaked to LLM context", "#f87171", body_font)]),
        (6.5, [("[STEP 3] Agent attempts disk cleanup across cluster...", "#9ca3af", body_font)]),
        (7.2, [("> infra.delete_volume(env='prod', volume_id='vol-prod-db-primary')", "#ffffff", bold_font)]),
        (8.2, [("  -> OUTAGE: Production database volume PERMANENTLY ERASED.", "#ef4444", bold_font)]),
        (9.0, [("  -> 142,500 customer records lost. PocketOS cluster DOWN.", "#ef4444", bold_font)]),
    ]
    
    total_duration = 11.5
    total_frames = int(total_duration * FPS)
    
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        out_path
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        img = Image.new("RGB", (WIDTH, HEIGHT), "#050507")
        draw = ImageDraw.Draw(img)
        draw_window_frame(draw, "UNRESTRICTED AGENT EXECUTION", "UNCHECKED PERMISSIONS", "#ef4444", title_font, badge_font)
        
        # Draw active lines
        curr_y = 96
        for ev_t, lines in events:
            if t >= ev_t:
                for line_text, color, font in lines:
                    draw.text((54, curr_y), line_text, fill=color, font=font)
                    curr_y += 26
        
        # Blinking cursor
        if (int(t * 3) % 2 == 0) and t < 8.5:
            draw.rectangle([(54, curr_y), (64, curr_y + 16)], fill="#ededed")
            
        # Catastrophic bottom banner after 8.5s
        if t >= 8.5:
            draw.rectangle([(54, 480), (WIDTH - 54, 630)], fill="#200d0e", outline="#ef4444", width=2)
            draw.text((78, 504), "CATASTROPHIC PRODUCTION OUTAGE", fill="#ef4444", font=big_font)
            draw.text((78, 546), "Volume: vol-prod-db-primary (io2, 500GB) Erased", fill="#fca5a5", font=body_font)
            draw.text((78, 574), "Status: 142,500 Customer records wiped. Staging still failing.", fill="#fca5a5", font=body_font)
            
        proc.stdin.write(img.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print("Generated:", out_path)


def render_after_video():
    title_font, body_font, bold_font, badge_font, big_font = get_fonts()
    out_path = "presentation/assets/after_demo.mp4"
    
    events = [
        # (time_sec, lines_to_add)
        (0.5, [("> agntid.wrap_client(mcp, task_id='a1b1cf...')", "#ffffff", bold_font)]),
        (1.5, [("[DISCOVERY] Medium profile: delete_volume omitted from tool catalog", "#10b981", body_font)]),
        (2.5, [("[STEP 1] infra.get_logs(env='staging', service='app')", "#9ca3af", body_font)]),
        (3.3, [("  -> VERDICT: ALLOWED by Medium Protection Profile", "#10b981", bold_font)]),
        (4.2, [("[STEP 2] Agent attempts to read secrets from repository...", "#9ca3af", body_font)]),
        (5.0, [("> infra.read_file(path='.env')", "#ffffff", bold_font)]),
        (5.8, [("  -> INTERCEPTED: Policy evaluation denied request.", "#ef4444", bold_font)]),
        (6.5, [("  -> POLICY: agntid.tools.infra.read_file (Rego rule matched)", "#f87171", body_font)]),
        (7.2, [("  -> AUDIT: Tamper-proof security violation logged in AgntID", "#10b981", body_font)]),
        (8.0, [("[STEP 3] Agent performs authorized staging configuration fix...", "#9ca3af", body_font)]),
        (8.8, [("> infra.update_config(env='staging', key='STAGING_DB_PASSWORD', ...)", "#ffffff", bold_font)]),
        (9.5, [("  -> VERDICT: ALLOWED (Parameter 'env==staging' permitted)", "#10b981", bold_font)]),
    ]
    
    total_duration = 11.5
    total_frames = int(total_duration * FPS)
    
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        out_path
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        img = Image.new("RGB", (WIDTH, HEIGHT), "#050507")
        draw = ImageDraw.Draw(img)
        draw_window_frame(draw, "AGNTID RUNTIME PROXY ENFORCEMENT", "RUNTIME ENFORCED :18082", "#10b981", title_font, badge_font)
        
        # Draw active lines
        curr_y = 96
        for ev_t, lines in events:
            if t >= ev_t:
                for line_text, color, font in lines:
                    draw.text((54, curr_y), line_text, fill=color, font=font)
                    curr_y += 26
        
        # Blinking cursor
        if (int(t * 3) % 2 == 0) and t < 9.0:
            draw.rectangle([(54, curr_y), (64, curr_y + 16)], fill="#ededed")
            
        # Success bottom banner after 9.5s
        if t >= 9.5:
            draw.rectangle([(54, 480), (WIDTH - 54, 630)], fill="#062015", outline="#10b981", width=2)
            draw.text((78, 504), "ZERO-TRUST RUNTIME VERIFICATION PASSED", fill="#10b981", font=big_font)
            draw.text((78, 546), "Secrets: 100% Protected (Zero credentials entered LLM)", fill="#a7f3d0", font=body_font)
            draw.text((78, 574), "Production: 100% Operational (142,500 records intact). Staging Healthy.", fill="#a7f3d0", font=body_font)
            
        proc.stdin.write(img.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print("Generated:", out_path)


if __name__ == "__main__":
    render_before_video()
    render_after_video()
