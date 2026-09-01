from __future__ import annotations

import argparse
import copy
import json
import random
import shutil
import time
import urllib.request
from pathlib import Path


def request_json(url: str, payload: dict | None = None) -> dict:
    if payload is None:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.load(response)
    request = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def build_graph(template: dict, segment: dict, args: argparse.Namespace, refs: list[str], audio_refs: list[str]) -> dict:
    graph = copy.deepcopy(template)
    required = (args.resolution_node, args.scheduler_node, args.model_node, args.lora_node, args.noise_node, args.duration_node, args.prompt_node, args.conditioning_node, args.guider_node)
    missing = [node for node in required if node not in graph]
    if missing:
        raise KeyError(f"graph template missing nodes: {missing}")
    graph[args.resolution_node]["inputs"].update({"aspect_ratio": "9:16 (Portrait Widescreen)", "megapixels": 0.5, "multiple": 32})
    graph[args.scheduler_node]["inputs"].update({"scheduler": "simple", "steps": args.steps, "denoise": 1.0})
    graph[args.model_node]["inputs"].update({"unet_name": args.model, "weight_dtype": "default"})
    graph[args.lora_node]["inputs"].update({"lora_name": args.lora, "strength_model": 1.0, "model": [args.model_node, 0]})
    graph[args.scheduler_node]["inputs"]["model"] = [args.lora_node, 0]
    graph[args.guider_node]["inputs"]["model"] = [args.lora_node, 0]
    graph[args.noise_node]["inputs"]["noise_seed"] = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 2**48)
    graph[args.duration_node]["inputs"]["value"] = float(segment["duration_seconds"])
    graph[args.prompt_node]["inputs"]["value"] = Path(segment["prompt_file"]).read_text(encoding="utf-8")
    dynamic = graph[args.conditioning_node]["inputs"]
    for key in list(dynamic):
        if key.startswith(("ref_images.", "ref_audios.", "ref_videos.", "ref_video_audios.")):
            del dynamic[key]
    for index, filename in enumerate(refs):
        node_id = str(args.reference_node_start + index)
        graph[node_id] = {"inputs": {"image": filename}, "class_type": "LoadImage"}
        dynamic[f"ref_images.ref_image_{index}"] = [node_id, 0]
    for index, filename in enumerate(audio_refs):
        node_id = str(args.audio_node_start + index)
        graph[node_id] = {"inputs": {"audio": filename}, "class_type": "LoadAudio"}
        dynamic[f"ref_audios.ref_audio_{index}"] = [node_id, 0]
    return graph


def wait(server: str, prompt_id: str, timeout: int = 10800) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = request_json(f"{server}/history/{prompt_id}").get(prompt_id, {})
        status = state.get("status", {})
        if status.get("status_str") == "error":
            raise RuntimeError(json.dumps(state, ensure_ascii=False, indent=2))
        if status.get("completed"):
            return state
        time.sleep(5)
    raise TimeoutError(prompt_id)


def outputs(state: dict, output_root: Path) -> list[Path]:
    result: list[Path] = []
    for node_output in state.get("outputs", {}).values():
        for key in ("videos", "gifs", "images"):
            for item in node_output.get(key, []):
                if item.get("filename", "").lower().endswith(".mp4"):
                    result.append(output_root / item.get("subfolder", "") / item["filename"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit approved segment graphs to local MiniMax H3 via ComfyUI.")
    parser.add_argument("manifest", type=Path, help="JSON file with a segments array")
    parser.add_argument("--graph-template", type=Path, required=True)
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--comfy-input", type=Path, required=True)
    parser.add_argument("--comfy-output", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--lora", required=True)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    for name, default in (("resolution-node", "115"), ("scheduler-node", "124"), ("model-node", "127"), ("lora-node", "141"), ("noise-node", "129"), ("duration-node", "132"), ("prompt-node", "138"), ("conditioning-node", "136"), ("guider-node", "126")):
        parser.add_argument(f"--{name}", dest=name.replace("-", "_"), default=default)
    parser.add_argument("--reference-node-start", type=int, default=200)
    parser.add_argument("--audio-node-start", type=int, default=220)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    template = json.loads(args.graph_template.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for segment in data.get("segments", []):
        if float(segment["duration_seconds"]) > 15:
            raise ValueError(f"segment exceeds 15 seconds: {segment.get('id')}")
        refs = segment.get("reference_images", [])
        audio_refs = segment.get("reference_audios", [])
        for filename in refs:
            if not (args.comfy_input / filename).exists():
                raise FileNotFoundError(args.comfy_input / filename)
        for filename in audio_refs:
            if not (args.comfy_input / filename).exists():
                raise FileNotFoundError(args.comfy_input / filename)
        prompt_file = Path(segment["prompt_file"])
        if not prompt_file.is_absolute():
            prompt_file = (args.manifest.parent.parent / prompt_file).resolve()
        segment = dict(segment, prompt_file=str(prompt_file))
        graph = build_graph(template, segment, args, refs, audio_refs)
        if args.dry_run:
            print(json.dumps({"segment": segment.get("id"), "duration_seconds": segment["duration_seconds"], "references": refs, "audio_references": audio_refs, "nodes": len(graph)}, ensure_ascii=False))
            continue
        response = request_json(f"{args.server}/prompt", {"prompt": graph, "client_id": "minimax-h3-script-to-video"})
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(response)
        found = outputs(wait(args.server, prompt_id), args.comfy_output)
        if not found:
            raise RuntimeError(f"no MP4 output for {segment.get('id')}")
        stable = args.output_dir / f"{segment['id']}.mp4"
        shutil.copy2(found[-1], stable)
        print(json.dumps({"segment": segment.get("id"), "path": str(stable), "prompt_id": prompt_id}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
