#!/usr/bin/env python3
"""Convert OpenCLAW m*.md skills to Hermes SKILL.md format and install them."""
import os, re, shutil

SKILLS_DIR = "/root/.hermes/skills"
SRC_DIR = "/root/.hermes/openclaw/openclaw/skills"

SKILL_META = {
    "m1": {
        "name": "monetize",
        "description": "Monetization & value generation specialist. Digital asset distribution, service packaging, pipeline architecture, leverage-first income systems. Trigger: monetize, pricing, jual, jualan, cuan, funnel, business, income."
    },
    "m2": {
        "name": "vps-deploy",
        "description": "Infrastructure & deployment specialist. VPS setup, SSH, nginx, Docker, systemd, Linux server management. Trigger: VPS, deploy, SSH, nginx, docker, systemd, server, linux, bash, sysadmin, host, install."
    },
    "m3": {
        "name": "content",
        "description": "Content creation & distribution specialist. Viral hooks, captions, threads, copywriting in Indonesian voice. Trigger: viral, hook, caption, thread, naskah, konten, content, post, copywriting."
    },
    "m4": {
        "name": "automation",
        "description": "Process orchestration & automation specialist. Production-grade Telegram bots, cron jobs, webhooks, n8n workflows. Trigger: telegram bot, cron, webhook, n8n, automate, otomatis, bot, schedule, jadwal."
    },
    "m5": {
        "name": "data-spreadsheet",
        "description": "Data transformation & insight specialist. Spreadsheets, Excel, CSV, datasets, snapshots, analytics reports. Trigger: spreadsheet, excel, csv, dataset, snapshot, laporan, data, analytics, report, numbers, stats."
    },
    "m6": {
        "name": "integrations",
        "description": "Protocol binding & service bridge specialist. API integrations, REST endpoints, webhooks, payment gateways (Midtrans), third-party SDKs. Trigger: API, REST, webhook, midtrans, integrasi, endpoint, SDK, integration, connect, call."
    },
    "m7": {
        "name": "ai-llm",
        "description": "Inference systems & AI builder specialist. LLM prompts, Claude API, OpenRouter, Kimi, multi-LLM fallback, streaming. Trigger: LLM, prompt, claude API, openrouter, kimi, AI, agent, model, GPT, inference."
    },
    "m8": {
        "name": "documents",
        "description": "File & artifact production specialist. Generate PDF, DOCX, XLSX, PPTX documents programmatically. Trigger: PDF, DOCX, XLSX, PPTX, generate file, dokumen, export, file, format, save."
    },
    "m9": {
        "name": "frontend",
        "description": "Interface construction specialist. Landing pages, React, Tailwind CSS, Web3 UIs. Trigger: landing page, react, tailwind, frontend, UI, website, HTML, CSS, web, design."
    },
    "m10": {
        "name": "web3-crypto",
        "description": "Web3 & crypto operations specialist. On-chain operations, wallet management, airdrop farming, RPC, ethers/viem. Trigger: wallet, airdrop, on-chain, RPC, ethers, viem, mint, crypto, web3, token, blockchain, ETH."
    },
    "m11": {
        "name": "security-audit",
        "description": "Security audit & review specialist. Vulnerability scanning, exploit detection, scam checks, smart contract auditing. Trigger: audit, vulnerability, exploit, scam check, malicious, security, review, safe, check, verify."
    },
    "m12": {
        "name": "batch-parallel",
        "description": "Batch & parallel operations specialist. Concurrent execution, bulk operations, queue workers, snapshot processing. Trigger: batch, parallel, bulk, mass, queue, worker, snapshot, concurrent, throughput, many, multi."
    },
    "m13": {
        "name": "nft-minter",
        "description": "Universal NFT minter. OpenSea, Manifold, Zora, SeaDrop, any contract. Auto-gas optimization. Trigger: mint, opensea, manifold, zora, seadrop, NFT, claim, drop, collect, art."
    },
    "x1": {
        "name": "self-audit",
        "description": "Internal capability refinement. Self-audit, system improvement, brain refactoring. Trigger: improve system, self-audit, upgrade brain, audit me, review agent, optimize."
    },
    "x2": {
        "name": "strategy",
        "description": "Deep decomposition & strategy. Complex multi-step planning, architecture design. Trigger: strategy, architecture, decompose, plan, design system, complex, multi-step."
    },
    "x3": {
        "name": "debug",
        "description": "Fault diagnosis & resolution. Debug errors, bugs, stack traces, failed operations. Trigger: error, bug, debug, gagal, rusak, stack trace, failed, broken, fix, crash, issue."
    },
}

for skill_id, meta in SKILL_META.items():
    src = os.path.join(SRC_DIR, f"{skill_id}.md")
    dest_dir = os.path.join(SKILLS_DIR, meta["name"])

    if not os.path.exists(src):
        print(f"⚠️  {skill_id}.md not found, skipping")
        continue

    # Read source content
    with open(src, "r") as f:
        content = f.read()

    # Remove the first line title if it has the format "# skills/m1.md — ..."
    content = re.sub(r'^#.*?[-—]\s*.*?\n', '', content, count=1)

    # Build SKILL.md with frontmatter
    frontmatter = f"""---
name: {meta["name"]}
description: "{meta["description"]}"
---

"""

    skill_content = frontmatter + content

    # Create destination directory
    os.makedirs(dest_dir, exist_ok=True)

    # Write SKILL.md
    dest_file = os.path.join(dest_dir, "SKILL.md")
    with open(dest_file, "w") as f:
        f.write(skill_content)

    print(f"✅ {skill_id} → {meta['name']}/SKILL.md")

print("\n🎉 All skills installed!")
print("Restart Hermes to load the new skills.")