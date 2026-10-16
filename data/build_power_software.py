"""Builds data/power.{json,js} and data/software.{json,js}.
Rule: every entry comes from a source that was actually opened. Unknown = None. No invented values."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
OPENED = "2026-10-16"

POWER = [
 dict(id="hydra-4x3090", name="HYDRA (LLM Monitor reference rig)", gpus="RTX 3090", gpu_count=4,
      platform="Intel X299 (Asus Pro WS X299 Sage II, i9-7920X), PLX-fed PCIe 3.0 x16 per GPU",
      power_limit_w=None, engine="vLLM 0.17 (driver 580, CUDA 13.0)", idle_w=170, inference_w=800, peak_w=None,
      measurement="wall", measured=True, psu="2x 1600W 80+ Titanium",
      notes="Source says '~800 W under load · ~170 W idle measured at the wall'. Power limit not stated.",
      source_url="https://ollama.linkworksinc.com/hardware/hydra", source_date=None, verified=OPENED),
 dict(id="lyth-8x3090", name="LYTH 8-GPU rig", gpus="7x RTX 3090 + 1x RTX 3090 Ti", gpu_count=8,
      platform="AMD EPYC on Supermicro H12SSL-i, 4 PSUs (1200W ATX + 1200W/1600W/750W HP server units)",
      power_limit_w="~250 W (3090), ~300 W (3090 Ti)", engine="vLLM (driver 580.126.20, P2P disabled)",
      idle_w=450, inference_w=823, peak_w=3100, measurement="wall (Tasmota meter)", measured=True, psu="4 PSUs, 4,750 W nameplate",
      notes="inference_w = 7-day mean continuous draw (19.754 kWh/day), which includes idle time. Short spikes ~3.1 kW; dashboard snapshot ~1,958 W with all 8 GPUs busy.",
      source_url="https://www.lyth.de/en/gpu-fallen-off-the-bus/", source_date="2026-08-05", verified=OPENED),
 dict(id="puget-2xr9700", name="Puget Systems 2x R9700 test bench", gpus="AMD Radeon AI PRO R9700", gpu_count=2,
      platform="Threadripper PRO 5995WX, ASUS Pro WS WRX80E-SAGE SE", power_limit_w=None,
      engine="vLLM v0.20.2 ROCm, FP8 TP=2 (Qwen3.6-27B)", idle_w=None, inference_w=480, peak_w=495,
      measurement="GPU only (sysfs hwmon, both cards), NOT wall", measured=True, psu=None,
      notes="480 W = both GPUs at 8 concurrent users; 310 W at 1 user. Puget estimates ~300 W more for the rest of the system (CPU measured ~120 W). Wall total not measured.",
      source_url="https://www.pugetsystems.com/labs/articles/amd-radeon-ai-pro-r9700-dual-gpu-ai-inference-performance/", source_date="2026-09-10", verified=OPENED),
 dict(id="cpompa-4x3090-est", name="cpompa.com 4x3090 guide (estimate)", gpus="RTX 3090", gpu_count=4,
      platform="AMD EPYC, ASRock Rack ROMED8-2T", power_limit_w="280 W (recommended)", engine="vLLM / TabbyAPI (guide)",
      idle_w=None, inference_w=1300, peak_w=1650, measurement="author estimate, NOT measured", measured=False, psu="1600W Titanium or 2x 1000W",
      notes="Guide estimates ~1,650 W peak at stock 350 W and ~1,300 W with a 280 W cap. Kept for planning reference only.",
      source_url="https://cpompa.com/docs/ai-inference-3090.html", source_date=None, verified=OPENED),
]

V = "https://github.com/vllm-project/vllm/issues/40980"
SOFT = [
 dict(card="AMD Radeon AI PRO R9700", count=2, engine="vLLM", version="0.19.1 (ROCm 7.2.1, RCCL 2.27.7 / librccl 70201)", backend="ROCm",
      works="no", tp_notes="TP=2 deadlocks: both GPUs at 100%, no tokens. TP=1 works. Also reported with TP=4 on 4x R9700.",
      flags="Fixed by NCCL_PROTO=Simple (see next entry). NCCL_P2P_DISABLE=1 and --enforce-eager don't help.",
      source_url=V, date="2026-04-27"),
 dict(card="AMD Radeon AI PRO R9700", count=4, engine="vLLM", version=">=0.19 (tested v0.20.1 image)", backend="ROCm",
      works="yes", tp_notes="TP=2 and TP=4 work with the workaround. One user saw a token-gen slowdown vs 0.18.1 on Qwen3.5-122B.",
      flags="NCCL_PROTO=Simple", source_url=V, date="2026-05-13"),
 dict(card="AMD Radeon AI PRO R9700", count=2, engine="vLLM", version="0.18.1 (vllm/vllm-openai-rocm:v0.18.1)", backend="ROCm",
      works="yes", tp_notes="Maintainer says this image works for TP without the deadlock.", flags="none", source_url=V, date="2026-04-28"),
 dict(card="AMD Radeon AI PRO R9700", count=2, engine="vLLM", version="0.25.1 (vllm/vllm-openai-rocm:v0.25.1)", backend="ROCm",
      works="yes", tp_notes="TP=2 runs granite-4.1-30b-fp8 per maintainer. No official AITER support on gfx1201.",
      flags="NCCL_PROTO=Simple, --attention-backend TRITON_ATTN", source_url=V, date="2026-07-22"),
 dict(card="AMD Radeon AI PRO R9700", count=2, engine="vLLM", version="0.20.2 (vllm/vllm-openai-rocm:v0.20.2)", backend="ROCm",
      works="yes", tp_notes="Bare metal: stock TP=2 FP8 works; RCCL init via P2P/IPC over PCIe in 0.12 s. Inside KVM/VFIO passthrough, multi-GPU RCCL init hangs.",
      flags="Bare metal required for multi-GPU; cards bound to amdgpu at boot",
      source_url="https://www.pugetsystems.com/labs/articles/amd-radeon-ai-pro-r9700-dual-gpu-ai-inference-performance/", date="2026-09-10"),
 dict(card="AMD Radeon AI PRO R9700", count=2, engine="llama.cpp", version="ghcr.io/ggml-org/llama.cpp:server-rocm (version not stated)", backend="ROCm",
      works="partial", tp_notes="--split-mode layer works. --split-mode row aborts on Qwen3.6-27B under concurrent decode (GGML_ASSERT); row worked on Qwen2.5-32B.",
      flags="Use --split-mode layer for Qwen3.6-class models",
      source_url="https://www.pugetsystems.com/labs/articles/amd-radeon-ai-pro-r9700-dual-gpu-ai-inference-performance/", date="2026-09-10"),
 dict(card="AMD Radeon AI PRO R9700", count=4, engine="vLLM", version="0.21.0 (vllm/vllm-openai-rocm:latest at the time)", backend="ROCm",
      works="no", tp_notes="Additional shm_broadcast hang on larger models (Qwen3.6, gpt-oss-120B).", flags="Use v0.20.2 + NCCL_PROTO=Simple or the vllm-dev image",
      source_url="https://forum.level1techs.com/t/amd-radeon-r9700-linux-tp2-and-tp4-the-definitive-guide/250504", date="2026-05-22"),
 dict(card="AMD Radeon AI PRO R9700", count=4, engine="vLLM", version="0.17.0-dev (rocm/vllm-dev:upstream_preview_releases_v0.17.0_20260303)", backend="ROCm (7.0 pre-release in image)",
      works="yes", tp_notes="TP=4 Qwen3.5-122B-A10B-GPTQ-Int4 at 39.9 tok/s; no NCCL_PROTO needed.",
      flags="VLLM_ROCM_USE_AITER=1, HSA_OVERRIDE_GFX_VERSION=12.0.1, VLLM_ROCM_USE_AITER_MOE=1, FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE, HSA_ENABLE_SDMA=0; kernel args amd_iommu=on iommu=pt pcie_aspm=off",
      source_url="https://forum.level1techs.com/t/amd-radeon-r9700-linux-tp2-and-tp4-the-definitive-guide/250504", date="2026-05-22"),
 dict(card="AMD Radeon AI PRO R9700 + RX 9070", count=2, engine="llama.cpp", version="llamacpp-rocm b1294", backend="ROCm",
      works="no", tp_notes="Layer split segfaults in libamdhip64; row split aborts on first matmul. Single GPU works. (R9700 on OCuLink, RX 9070 on TB4 eGPU.)",
      flags="NCCL_PROTO=Simple has no effect (RCCL not used by default GGML/HIP builds)",
      source_url="https://github.com/ROCm/rocm-systems/issues/5480", date="2026-09-13"),
 dict(card="RTX 3090 (7x) + RTX 3090 Ti", count=8, engine="vLLM", version="not stated (driver 580.126.20)", backend="CUDA",
      works="partial", tp_notes="No NVLink; 4 PCIe root complexes. P2P via patched open driver gave corrupt data and hangs; stock driver with P2P off is stable.",
      flags="NCCL_P2P_DISABLE=1, NCCL_CUMEM_ENABLE=0, VLLM_ALLREDUCE_USE_SYMM_MEM=0, --disable-custom-all-reduce",
      source_url="https://www.lyth.de/en/gpu-fallen-off-the-bus/", date="2026-08-05"),
 dict(card="RTX 3090", count=4, engine="vLLM", version="0.17 (driver 580, CUDA 13.0)", backend="CUDA",
      works="yes", tp_notes="TP=4 in production on PLX-fed PCIe 3.0 x16 slots.", flags=None,
      source_url="https://ollama.linkworksinc.com/hardware/hydra", date=None),
 dict(card="AMD Radeon AI PRO R9700", count=None, engine="ROCm", version="7.14 system requirements", backend="ROCm",
      works="yes", tp_notes="Officially supported (gfx1201) on Ubuntu 24.04.4 / 22.04.5, RHEL 10.1 / 9.7. Multi-GPU systems may need iommu=pt to prevent hangs.",
      flags="iommu=pt", source_url="https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html", date="2026-07-15"),
 dict(card="Radeon RX 7900 XTX / RX 9000 series / MI200-MI350", count=None, engine="vLLM", version="docs latest (prebuilt ROCm wheels 7.0 and 7.2.1)", backend="ROCm",
      works="yes", tp_notes="Listed as supported GPU targets: gfx90a, gfx942, gfx950, gfx1100/1101, gfx1200/1201, gfx1150/1151. ROCm 6.3+; ROCm wheels need Python 3.12.",
      flags=None, source_url="https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html", date=OPENED),
 dict(card="Radeon Instinct MI50 / Radeon VII (gfx906)", count=None, engine="vLLM", version="0.30.0", backend="ROCm",
      works="no", tp_notes="Not in vLLM's supported AMD target list.", flags=None,
      source_url="https://gpucompat.com/library-support/vllm/", date="2026-09-27"),
 dict(card="NVIDIA Pascal/Volta (P40, P100, V100, 1080 Ti)", count=None, engine="vLLM", version="0.30.0", backend="CUDA",
      works="no", tp_notes="vLLM needs compute capability 7.5+.", flags=None,
      source_url="https://gpucompat.com/library-support/vllm/", date="2026-09-27"),
]
_prev = {}
if os.path.exists(f"{D}/software.json"):
    _prev = {e["id"]: e for e in json.load(open(f"{D}/software.json"))}
for i,s in enumerate(SOFT):
    s.update(id=f"sw-{i+1:02d}", verified=OPENED)
    old = _prev.get(s["id"], {})  # keep flags set by scripts/watch_releases.py
    s["needs_retest"] = old.get("needs_retest", False)
    if old.get("retest_reason"): s["retest_reason"] = old["retest_reason"]

for name, data in (("power", POWER), ("software", SOFT)):
    json.dump(data, open(f"{D}/{name}.json","w"), indent=1)
    open(f"{D}/{name}.js","w").write(f"window.{name.upper()}=" + json.dumps(data) + ";\n")
print(len(POWER), "power,", len(SOFT), "software")
