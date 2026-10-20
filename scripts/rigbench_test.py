#!/usr/bin/env python3
"""RigBench standard test: hold one GPU at a fixed power limit for N minutes, log temp/fan/power to JSON.
Usage: sudo python3 rigbench_test.py --gpu 0 --watts 250 --minutes 30 --part pr-1421067 --load "gpu-burn 1800"
Requires nvidia-smi (NVIDIA) or rocm-smi (AMD). Load command is user-supplied (e.g. gpu-burn, llama-bench loop).
Setting a power limit needs root and changes GPU state; it is reset at the end. Run only on your own hardware."""
import argparse,json,shutil,subprocess,time,datetime,sys,signal
a=argparse.ArgumentParser()
a.add_argument("--gpu",type=int,default=0);a.add_argument("--watts",type=int,required=True)
a.add_argument("--minutes",type=float,default=30);a.add_argument("--interval",type=float,default=5)
a.add_argument("--part",required=True);a.add_argument("--load",required=True,help="shell command that loads the GPU")
a.add_argument("--ambient-c",type=float);a.add_argument("--noise-dba",type=float);a.add_argument("--out")
o=a.parse_args()
nv=shutil.which("nvidia-smi");rocm=shutil.which("rocm-smi")
if not (nv or rocm): sys.exit("need nvidia-smi or rocm-smi")
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True).stdout
def setpl(w):
    if nv: return sh(f"nvidia-smi -i {o.gpu} -pl {w}")
    return sh(f"rocm-smi -d {o.gpu} --setpoweroverdrive {w} --autorespond yes")
def sample():
    t=time.time()
    if nv:
        r=sh(f"nvidia-smi -i {o.gpu} --query-gpu=temperature.gpu,fan.speed,power.draw,clocks.sm --format=csv,noheader,nounits").strip().split(",")
        f=lambda s:(None if "N/A" in s or "[" in s else float(s))
        return dict(t=t,temp_c=f(r[0]),fan_pct=f(r[1]),power_w=f(r[2]),sm_mhz=f(r[3]))
    j=json.loads(sh(f"rocm-smi -d {o.gpu} --showtemp --showfan --showpower --json") or "{}")
    return dict(t=t,raw=j)
orig=None
if nv: orig=sh(f"nvidia-smi -i {o.gpu} --query-gpu=power.default_limit --format=csv,noheader,nounits").strip()
print(setpl(o.watts))
idle=[sample() for _ in range(3)]
p=subprocess.Popen(o.load,shell=True)
log=[];end=time.time()+o.minutes*60
try:
    while time.time()<end:
        log.append(sample());time.sleep(o.interval)
finally:
    p.send_signal(signal.SIGINT);time.sleep(2);p.kill()
    if orig: print(setpl(int(float(orig))))
temps=[s.get("temp_c") for s in log if s.get("temp_c") is not None]
res=dict(part_id=o.part,gpu_index=o.gpu,power_limit_w=o.watts,minutes=o.minutes,ambient_c=o.ambient_c,noise_dba=o.noise_dba,
 started=datetime.datetime.now().isoformat(),tool="nvidia-smi" if nv else "rocm-smi",idle=idle,samples=log,
 summary=dict(max_temp_c=max(temps) if temps else None,last5min_avg_c=(sum(temps[-int(300/o.interval):])/len(temps[-int(300/o.interval):])) if temps else None,
 delta_t_c=(max(temps)-o.ambient_c) if temps and o.ambient_c is not None else None))
out=o.out or f"results/{o.part}-{int(time.time())}.json"
import os;os.makedirs(os.path.dirname(out) or ".",exist_ok=True);json.dump(res,open(out,"w"),indent=1);print("wrote",out,res["summary"])
