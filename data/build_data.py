import json
M="manufacturer page fetched 2026-10-16"; R="third-party review page fetched 2026-10-16 (manufacturer page unavailable)"
def mb(id,name,mfr,platform,socket,ff,slots,bif,src,notes="",ver=M):
    return dict(id=id,category="motherboard",name=name,manufacturer=mfr,platform=platform,socket=socket,form_factor=ff,
      gpu_slot_count=sum(1 for s in slots if s["lanes"]>=8),slots=slots,cpu_lanes_to_slots=sum(s["lanes"] for s in slots),
      bifurcation=bif,source_url=src,verification=ver,notes=notes,affiliate_url="")
def sl(*a): return [dict(gen=g,lanes=l,label=lab) for g,l,lab in a]
X=lambda n,g,lab: [(g,16,f"{lab} #{i}") for i in range(1,n+1)]
parts=[
mb("asrockrack-romed8-2t","ROMED8-2T","ASRock Rack","EPYC 7002/7003","SP3","ATX",sl(*X(7,4,"PCIe4 x16")),"",
 "https://www.asrockrack.com/general/productdetail.asp?Model=ROMED8-2T","Maker page summary: 7x PCIe4.0 x16, 2x OCuLink x4, 2x M.2. Per-slot lane sharing not shown on the fetched page (spec table did not load)."),
mb("supermicro-h12ssl-i","H12SSL-i","Supermicro","EPYC 7002/7003","SP3","ATX",sl(*(X(5,4,"PCIe4 x16")+[(4,8,"PCIe4 x8 #1"),(4,8,"PCIe4 x8 #2")])),"",
 "https://www.supermicro.com/en/products/motherboard/h12ssl-i","5x x16 + 2x x8; physical slot order not on the product page."),
mb("supermicro-h12ssl-nt","H12SSL-NT","Supermicro","EPYC 7002/7003","SP3","ATX",sl(*(X(5,4,"PCIe4 x16")+[(4,8,"PCIe4 x8 #1"),(4,8,"PCIe4 x8 #2")])),"",
 "https://www.supermicro.com/en/products/motherboard/h12ssl-nt","Same slot set as H12SSL-i; dual 10GBase-T, 2x SlimSAS x8."),
mb("supermicro-h11ssl-i","H11SSL-i","Supermicro","EPYC 7001/7002","SP3","ATX",sl(*(X(3,3,"PCIe3 x16")+[(3,8,f"PCIe3 x8 #{i}") for i in (1,2,3)])),"",
 "https://www.supermicro.com/en/products/motherboard/h11ssl-i","EOL. EPYC 7002 needs board rev 2.x. PCIe 3.0 only."),
mb("gigabyte-mz32-ar0","MZ32-AR0 (rev 3.x)","Gigabyte","EPYC 7002/7003","SP3","E-ATX",
 sl((4,16,"Slot_7 (shared w/ 4x NVMe; needs optional cables)"),(4,16,"Slot_6"),(4,8,"Slot_5 (x16 phys)"),(4,16,"Slot_4"),(4,16,"Slot_3"),(3,8,"Slot_2 (Gen3 x0/x8)"),(3,8,"Slot_1 (Gen3 x16 or x8, shared w/ Slot_2)")),
 "","https://www.gigabyte.com/Enterprise/Server-Motherboard/MZ32-AR0-rev-3x","Slot_1 counted at x8 assuming Slot_2 populated; x16 if Slot_2 empty. cTDP up to 280W."),
mb("huananzhi-h12d-8d","H12D-8D","HUANANZHI","EPYC 7002/7003","SP3","ATX (305x245 mm)",sl(*X(4,4,"PCIe4 x16")),"",
 "https://www.huananzhi.com/en/list_6/177.html","Board from the r/LocalLLaMA 4x3090 thread. 3x M.2 x4, 3x SFF-8643. A BIOS listed on the page mentions 'PCIE split'; modes not documented."),
mb("asus-wrx80e-sage-se","Pro WS WRX80E-SAGE SE WIFI","ASUS","Threadripper PRO 3000/5000 WX","sWRX8","EEB",sl(*X(7,4,"PCIe4 x16")),"x4x4x4x4 ('PCIe bandwidth bifurcation for RAID on CPU')",
 "https://www.asus.com/motherboards-components/motherboards/workstation/pro-ws-wrx80e-sage-se-wifi/techspec/"),
mb("supermicro-m12swa-tf","M12SWA-TF","Supermicro","Threadripper PRO 3000/5000 WX","sWRX8","E-ATX",sl(*X(6,4,"PCIe4 x16")),"",
 "https://www.supermicro.com/en/products/motherboard/m12swa-tf","CPU TDP up to 280W."),
mb("asus-wrx90e-sage-se","Pro WS WRX90E-SAGE SE","ASUS","Threadripper PRO 7000/9000 WX","sTR5","EEB",
 sl(*([(5,16,f"PCIEX16(G5)_{i}") for i in (1,2,3,4,5)]+[(5,8,"PCIEX16(G5)_6 (x8 mode)"),(5,16,"PCIEX16(G5)_7")])),"",
 "https://www.asus.com/motherboards-components/motherboards/workstation/pro-ws-wrx90e-sage-se/techspec/","Bifurcation: maker page defers to ASUS FAQ 1037507 (not fetched), so left blank. Slot-6 position per ASUS manual naming."),
mb("asrock-wrx90-ws-evo","WRX90 WS EVO","ASRock","Threadripper PRO 7000/9000 WX","sTR5","EEB",
 sl(*([(5,16,f"PCIE{i}") for i in (1,2,3,4,5)]+[(5,8,"PCIE6 (x8)"),(5,16,"PCIE7")])),"",
 "https://www.asrock.com/mb/AMD/WRX90%20WS%20EVO/index.asp","All 7 slots from CPU. Multi-PSU adaptor cable included."),
mb("asus-trx50-sage","Pro WS TRX50-SAGE WIFI","ASUS","Threadripper 7000/9000 (+PRO)","sTR5","CEB",
 sl((5,16,"PCIe5 x16 #1"),(5,16,"PCIe5 x16 #2"),(5,8,"PCIe5 x16 (x8 mode)"),(4,16,"PCIe4 x16"),(4,4,"PCIe4 x16 (x4 mode)")),"",
 "https://www.asus.com/motherboards-components/motherboards/workstation/pro-ws-trx50-sage-wifi/techspec/","Maker page lists all 5 slots under the CPU; physical order not given. Bifurcation deferred to ASUS FAQ (not fetched)."),
mb("asrock-trx50-ws","TRX50 WS","ASRock","Threadripper 7000/9000 (+PRO)","sTR5","E-ATX",
 sl((5,16,"PCIE1"),(4,4,"PCIE2 (Gen4, x4)"),(5,16,"PCIE3"),(5,8,"PCIE4 (x8)"),(4,8,"PCIE5 (Gen4, x8)")),"",
 "https://www.asrock.com/mb/AMD/TRX50%20WS/index.asp","All slots from CPU."),
mb("gigabyte-trx50-aero-d","TRX50 AERO D (rev 1.0)","Gigabyte","Threadripper 7000/9000 (+PRO)","sTR5","E-ATX",
 sl((5,16,"PCIEX16_1"),(5,16,"PCIEX16_2"),(4,16,"PCIEX16_3")),"",
 "https://www.gigabyte.com/Motherboard/TRX50-AERO-D-rev-10/sp","All 3 slots from CPU."),
mb("supermicro-h13ssl-n","H13SSL-N","Supermicro","EPYC 9004/9005","SP5","ATX",sl(*(X(3,5,"PCIe5 x16")+[(5,8,"PCIe5 x8 #1"),(5,8,"PCIe5 x8 #2")])),"",
 "https://www.supermicro.com/en/products/motherboard/H13SSL-N","EPYC 9005 requires board rev 2.x. Up to 400W TDP. 3x MCIO x8. Slot order not on product page."),
mb("supermicro-h14ssl-n","H14SSL-N","Supermicro","EPYC 9004/9005","SP5","ATX",sl(*(X(3,5,"PCIe5 x16")+[(5,8,"PCIe5 x8 #1"),(5,8,"PCIe5 x8 #2")])),"",
 "https://www.supermicro.com/en/products/motherboard/h14ssl-n","Up to 500W TDP CPUs. 3x MCIO x8."),
mb("asrockrack-genoad8x-2t","GENOAD8X-2T/BCM","ASRock Rack","EPYC 9004/9005","SP5","EEB",
 sl((5,16,"SLOT0 (CXL)"),(5,16,"SLOT1 (x8 if MCIO/M.2 shared lanes used)"),(5,16,"SLOT2 (CXL)"),(5,16,"SLOT3"),(5,16,"SLOT4 (CXL)"),(5,16,"SLOT5"),(5,16,"SLOT6 (CXL)"),(5,8,"SLOT7 (near CPU; x4 if MCIO selected)")),"",
 "https://www.asrockrack.com/general/productdetail.asp?Model=GENOAD8X-2T/BCM","EPYC 9005 needs BIOS update. TDP up to 400W. Candidate board for EPYC 9575F 4-GPU builds."),
mb("gigabyte-mz33-ar1","MZ33-AR1 (rev 3.x)","Gigabyte","EPYC 9004/9005","SP5","E-ATX",
 sl((5,16,"Slot_3"),(5,16,"Slot_4"),(5,16,"Slot_6"),(5,16,"Slot_7")),"",
 "https://www.gigabyte.com/Enterprise/Server-Motherboard/MZ33-AR1-rev-3x","cTDP up to 500W. Plus 5x MCIO 8i Gen5 x8 + 1x Gen4 x8 (usable for GPUs via MCIO device adapters). Bifurcation modes not on product page."),
mb("asus-proart-x870e","ProArt X870E-CREATOR WIFI","ASUS","AM5 (Ryzen 7000/9000)","AM5","ATX",
 sl((5,8,"PCIEX16(G5)_1 (x16 alone; x8 w/ _2)"),(5,8,"PCIEX16(G5)_2 (x8; x4 if M.2_2 used)"),(4,4,"PCIe4 x16 (chipset, x4)")),"x16, x8/x8, x8/x4/x4 (CPU slots)",
 "https://www.asus.com/motherboards-components/motherboards/proart/proart-x870e-creator-wifi/techspec/","AM5 4x3090 context: 3rd/4th GPU must use chipset x4 or M.2 adapters. Ryzen 8000 APUs disable G5_2."),
mb("asus-proart-x670e","ProArt X670E-CREATOR WIFI","ASUS","AM5 (Ryzen 7000/8000/9000)","AM5","ATX",
 sl((5,8,"PCIEX16_1 (x16 alone; x8 w/ _2)"),(5,8,"PCIEX16_2 (x8)"),(4,2,"PCIEX16_3 (chipset, x2; shared w/ M.2_3)")),"x16 or x8/x8 (CPU slots)",
 "https://www.asus.com/motherboards-components/motherboards/proart/proart-x670e-creator-wifi/techspec/"),
]
def psu(id,name,mfr,w,v,pcie8,hp,src,notes="",ver=M):
    return dict(id=id,category="psu",name=name,manufacturer=mfr,wattage=w,input_voltage=v,pcie_8pin=pcie8,pcie_12v_2x6=hp,source_url=src,verification=ver,notes=notes,affiliate_url="")
parts+=[
psu("corsair-ax1600i","AX1600i","Corsair",1600,"1600W on 15A circuits of 115V and higher",10,None,"https://www.corsair.com/us/en/p/psu/cp-9020087-na/ax1600i-digital-atx-power-supply-1600-watt-fully-modular-psu-cp-9020087-na",
 "PCIe count (6 single + 2 dual cables = 10) from TechPowerUp review https://www.techpowerup.com/review/corsair-ax1600i/2.html; maker page lists no PCIe count."),
psu("seasonic-prime-tx-1600","PRIME TX-1600 (ATX 3.1)","Seasonic",1600,"100-240V; 1600W at 115-240V, 1300W at 100V",6,None,"https://seasonic.com/atx3-prime-tx/","Native 12V-2x6; count not unambiguous on page, left blank."),
psu("seasonic-prime-px-1600","PRIME PX-1600","Seasonic",1600,"100-240V; 1600W at 115-240V, 1300W at 100V",None,2,"https://seasonic.com/prime-px/","Ships with two 12VHPWR cables (per page). PCIe 8-pin count not unambiguous; blank."),
psu("superflower-leadex-plat-2000","Leadex Platinum 2000W (SF-2000F14HP)","Super Flower",2000,"",None,None,"https://www.techpowerup.com/review/super-flower-sf-2000f14hp/2.html",
 "Review lists 4x 6+2 PCIe cables plus cables with 10 more 6+2/6-pin connectors. Certified 80 PLUS Platinum 230V EU; 120V capability NOT verified (manufacturer page 404).",R),
psu("corsair-hx1500i-2025","HX1500i (ATX 3.1)","Corsair",1500,"100-240V; 1500W at 115-240V, 1200W at 100-115V",None,2,"https://www.corsair.com/us/en/p/psu/cp-9020309-na/hx1500i-fully-modular-ultra-low-noise-platinum-atx-1500-watt-pc-power-supply-cp-9020309-na",
 "12V-2x6 cables are 2x8-pin-to-12V-2x6 (share PSU headers). PCIe 8-pin quantity not shown in fetched cable table."),
psu("asus-rog-thor-1600t3","ROG THOR 1600W Titanium III","ASUS",1600,"100-240V",4,2,"https://rog.asus.com/power-supply-units/rog-thor/rog-thor-1600t3-gaming/spec/"),
psu("bequiet-dpp13-1600","Dark Power Pro 13 1600W","be quiet!",1600,"115-240V",6,2,"https://www.bequiet.com/en/powersupply/4414","12V-2x6 combined max 1000W."),
psu("msi-meg-ai1600t","MEG Ai1600T PCIE5","MSI",1600,"100-240V",9,2,"https://www.msi.com/Power-Supply/MEG-Ai1600T-PCIE5/Specification","16-pin rated 600W each."),
]
def acc(id,cat,name,mfr,src,ver=M,**kw):
    d=dict(id=id,category=cat,name=name,manufacturer=mfr,source_url=src,verification=ver,affiliate_url="");d.update(kw);return d
parts+=[
acc("cpayne-pm40100-switch","switch","PCIe gen4 Switch 5x x16 (Switchtec PM40100)","C-Payne","https://c-payne.com/products/pcie-gen4-switch-5x-x16-microchip-switchtec-pm40100",pcie_gen=4,upstream="2x SlimSAS 8i (1 mandatory)",downstream="5x PCIe gen4 x16 slots, quad-width (81.28 mm) spacing + aux x4 SlimSAS",power="3x 8-pin EPS (mandatory)"),
acc("cpayne-pm40084-switch","switch","PCIe gen4 Switch 4x x16 (Switchtec PM40084)","C-Payne","https://c-payne.com/products/pcie-gen4-switch-4x-x16-microchip-switchtec-pm40084",pcie_gen=4,upstream="2x SlimSAS 8i (1 mandatory)",downstream="4x PCIe gen4 x16 slots, 5-width (101.6 mm) spacing + aux x4 SlimSAS",power="4 EPS (2 mandatory)"),
acc("cpayne-slimsas-host-x16","riser","SlimSAS PCIe gen3(4) Host Adapter x16 (passive)","C-Payne","https://c-payne.com/products/pcie-slimsas-host-adapter-x16-to-2-8i",pcie_gen="3 (4 with care)",lanes=16,outputs="2x SlimSAS 8i",bifurcation_modes="x16, x8x8, x8x4x4, x4x4x8, x4x4x4x4",notes="Gen4 needs special consideration (board layout, device, cable length)."),
acc("cpayne-mcio-device-x8x16","riser","MCIO PCIe gen5 Device Adapter x8/x16","C-Payne","https://c-payne.com/products/mcio-pcie-gen5-device-adapter-x8-x16",pcie_gen=5,lanes="8 (one cable) or 16 (two cables)",inputs="2x MCIO 8i",power="mandatory 12V connector",notes="Pairs with MCIO ports on MZ33-AR1 / H13SSL / H14SSL. Both cables must come from the same host port in lane order 0-7 then 8-15."),
acc("cpayne-mcio-host-x16","riser","MCIO PCIe gen5 Host Adapter x16 (passive)","C-Payne","https://c-payne.com/products/mcio-pcie-gen5-host-adapter-x16-passive",pcie_gen=5,lanes=16,notes="Product page shows only name/price; outputs and bifurcation modes not listed, left blank."),
acc("linkup-ultra-pcie4","riser","Ultra PCIe 4.0 X16 Riser Cable (Extreme)","LINKUP","https://linkup.one/pci-e-riser-cables/pcie-4.0/ultra-4.0-riser-cables/",pcie_gen=4,lanes=16,length="5–28 cm variants listed",notes="All variants on the fetched page are marked Discontinued."),
acc("tt-premium-pcie4-200","riser","TT Premium PCI-E 4.0 Extender 200mm (90° adapter)","Thermaltake","https://thermaltake.com/tt-premium-pci-e-4-0-extender-200mm-with-90-degree-adapter.html",pcie_gen=4,lanes=16,length="200 mm",part_number="AC-060-CO1OTN-C2"),
acc("tt-premium-pcie4-600","riser","TT Premium PCI-E 4.0 Extender 600mm","Thermaltake","https://thermaltake.com/tt-premium-pci-e-4-0-extender-600mm.html",pcie_gen=4,lanes=16,length="600 mm",part_number="AC-059-CO1OTN-C1"),
acc("phanteks-enthoo-pro2-server","case","Enthoo Pro II Server Edition","Phanteks","https://phanteks.com/product/enthoo-pro-2-server-edition-cp/",expansion_slots=11,mb_support="SSI-EEB, E-ATX, XL-ATX, ATX…",max_gpu_length_mm=503,notes="Includes server-PSU bracket. GPU count limit not stated on page."),
acc("phanteks-enthoo-pro2-tg","case","Enthoo Pro II (Tempered Glass)","Phanteks","https://phanteks.com/product/enthoo-pro-2-tg/",expansion_slots=11,mb_support="SSI-EEB, E-ATX, XL-ATX, ATX…",max_gpu_length_mm=503),
acc("fractal-define-7-xl","case","Define 7 XL","Fractal Design","https://www.fractal-design.com/products/cases/define/define-7-xl/black-solid/",expansion_slots=9,mb_support="SSI-EEB, E-ATX, EE-ATX, ATX…",max_gpu_length_mm=530,psu_max_length_mm=250),
]
def gpu(id,name,tdp,mem,conn,src):
    return dict(id=id,category="gpu",name=name,manufacturer="NVIDIA",tdp_w=tdp,vram_gb=mem,power_connector=conn,source_url=src,verification=M,affiliate_url="")
G="https://www.nvidia.com/en-us/geforce/graphics-cards/"
parts+=[
gpu("rtx-3090","GeForce RTX 3090",350,24,"2x PCIe 8-pin (via FE adapter)",G+"30-series/rtx-3090-3090ti/"),
gpu("rtx-3090-ti","GeForce RTX 3090 Ti",450,24,"3x PCIe 8-pin (adapter) or 450W+ PCIe Gen5 cable",G+"30-series/rtx-3090-3090ti/"),
gpu("rtx-4090","GeForce RTX 4090",450,24,"3x PCIe 8-pin (adapter) or 450W+ PCIe Gen5 cable",G+"40-series/rtx-4090/"),
gpu("rtx-5090","GeForce RTX 5090",575,32,"4x PCIe 8-pin (adapter) or 1x 600W PCIe Gen5 cable",G+"50-series/rtx-5090/"),
gpu("rtx-a5000","RTX A5000",None,24,"","https://www.nvidia.com/en-us/design-visualization/rtx-a5000/"),
gpu("rtx-a6000","RTX A6000",300,48,"","https://www.nvidia.com/en-us/design-visualization/rtx-a6000/"),
gpu("rtx-6000-ada","RTX 6000 Ada Generation",300,48,"","https://www.nvidia.com/en-us/design-visualization/rtx-6000/"),
gpu("rtx-pro-6000-blackwell","RTX PRO 6000 Blackwell Workstation Edition",600,96,"","https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000/"),
gpu("rtx-pro-6000-maxq","RTX PRO 6000 Blackwell Max-Q",300,96,"","https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000-max-q/"),
]
for p in parts:
    if p["id"]=="rtx-a5000": p["notes"]="TDP not shown on fetched NVIDIA page; blank. Enter a power limit in the checker."
json.dump(parts,open("data/parts.json","w"),indent=1)
open("data/parts.js","w").write("window.PARTS="+json.dumps(parts)+";")
from collections import Counter;print(len(parts),Counter(p["category"] for p in parts),Counter(p["verification"] for p in parts))
