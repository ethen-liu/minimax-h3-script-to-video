from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit generated H3 MP4 files.")
    parser.add_argument("video_dir", type=Path)
    parser.add_argument("--expected-width", type=int, default=544)
    parser.add_argument("--expected-height", type=int, default=960)
    parser.add_argument("--expected-fps", type=float, default=24.0)
    args = parser.parse_args()
    try:
        import av
    except ImportError:
        print("PyAV is required for audit_video.py", file=sys.stderr)
        return 2
    reports: list[dict] = []
    passed = True
    for path in sorted(args.video_dir.glob("*.mp4")):
        try:
            with av.open(str(path)) as container:
                stream = container.streams.video[0]
                duration = float(container.duration / 1_000_000) if container.duration else 0.0
                fps = float(stream.average_rate or 0)
                report = {"file": str(path), "width": stream.width, "height": stream.height, "fps": fps, "frames": int(stream.frames or 0), "duration_seconds": round(duration, 3), "has_audio": bool(container.streams.audio), "decodable": True}
        except Exception as exc:
            report = {"file": str(path), "decodable": False, "error": str(exc)}
        report["passed"] = bool(report.get("decodable") and report.get("width") == args.expected_width and report.get("height") == args.expected_height and abs(report.get("fps", 0) - args.expected_fps) < 0.01 and report.get("has_audio"))
        passed = passed and report["passed"]
        reports.append(report)
    result = {"passed": passed and bool(reports), "files": reports}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
