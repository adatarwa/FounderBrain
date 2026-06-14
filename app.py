"""
app.py
FounderBrain web interface.
Paste your startup description, watch 7 agents run in real time,
get the full report in your browser.

Run: python app.py
Open: http://localhost:5000
"""

import os
import json
import threading
import queue
from flask import Flask, render_template_string, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv

load_dotenv()

from orchestrator import Orchestrator
from output.report import generate_report, print_summary
from output.exporters import JSONExporter

app = Flask(__name__)

# Store active runs
active_runs = {}

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FounderBrain</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0a0a14;color:#e0d8f0;min-height:100vh;}
.wrap{max-width:800px;margin:0 auto;padding:3rem 1.5rem;}
h1{font-size:2rem;font-weight:600;color:#c4a8ff;margin-bottom:.4rem;}
.sub{font-size:14px;color:#555;margin-bottom:2.5rem;line-height:1.6;}
.input-card{background:#111126;border:1px solid #2a2a4a;border-radius:14px;padding:1.5rem;}
label{font-size:13px;color:#888;display:block;margin-bottom:6px;}
textarea{width:100%;background:#0d0d1a;border:1px solid #2a2a4a;border-radius:8px;color:#e0d8f0;padding:12px;font-size:14px;line-height:1.6;resize:vertical;outline:none;transition:border-color .2s;min-height:100px;}
textarea:focus{border-color:#6a3adf;}
input[type=text]{width:100%;background:#0d0d1a;border:1px solid #2a2a4a;border-radius:8px;color:#e0d8f0;padding:10px 12px;font-size:14px;outline:none;transition:border-color .2s;margin-top:.75rem;}
input[type=text]:focus{border-color:#6a3adf;}
.run-btn{background:#5a2aba;color:#fff;border:none;padding:12px 32px;border-radius:8px;font-size:15px;cursor:pointer;width:100%;margin-top:1rem;transition:background .15s;font-weight:500;}
.run-btn:hover{background:#7a4ade;}
.run-btn:disabled{opacity:.4;cursor:not-allowed;}
.agents{margin-top:2rem;display:none;}
.agent-row{display:flex;align-items:flex-start;gap:12px;padding:.75rem 0;border-bottom:1px solid #1a1a2a;}
.agent-row:last-child{border-bottom:none;}
.agent-icon{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;margin-top:2px;}
.icon-waiting{background:#1a1a2a;color:#444;}
.icon-running{background:#1a1a3a;color:#7a4ade;animation:pulse 1.5s ease-in-out infinite;}
.icon-done{background:#0a2a1a;color:#2aba7a;}
.icon-failed{background:#2a0a0a;color:#ba2a2a;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
.agent-name{font-size:14px;font-weight:500;color:#c4a8ff;}
.agent-status{font-size:12px;color:#555;margin-top:2px;}
.agent-summary{font-size:13px;color:#aaa;margin-top:4px;line-height:1.5;}
.wave-label{font-size:11px;color:#5a3aba;text-transform:uppercase;letter-spacing:.06em;margin:.75rem 0 .25rem;font-weight:500;}
.report{margin-top:2rem;display:none;}
.report-card{background:#111126;border:1px solid #2a2a4a;border-radius:14px;padding:1.5rem;}
.report-title{font-size:16px;font-weight:500;color:#c4a8ff;margin-bottom:1rem;}
.section-card{background:#0d0d1a;border-radius:10px;padding:1rem 1.25rem;margin-bottom:.75rem;}
.section-title{font-size:13px;font-weight:500;color:#7a5adf;margin-bottom:.5rem;}
.section-summary{font-size:13px;color:#aaa;line-height:1.6;}
.section-facts{margin-top:.5rem;}
.fact{font-size:12px;color:#888;padding:2px 0;}
.fact::before{content:"→ ";color:#5a3aba;}
.dl-btn{display:inline-flex;align-items:center;gap:6px;background:transparent;border:1px solid #2a2a4a;border-radius:8px;padding:8px 16px;font-size:13px;color:#888;cursor:pointer;margin-top:1rem;margin-right:.5rem;transition:all .15s;text-decoration:none;}
.dl-btn:hover{border-color:#6a3adf;color:#c4a8ff;}
.progress-bar{height:3px;background:#1a1a2a;border-radius:2px;margin:1rem 0;overflow:hidden;display:none;}
.progress-fill{height:100%;background:#5a2aba;border-radius:2px;width:0%;transition:width .5s;}
</style>
</head>
<body>
<div class="wrap">
  <h1>🧠 FounderBrain</h1>
  <p class="sub">7 specialist AI agents. One cohesive startup OS.<br>Market · Legal · Customer · GTM · Hiring · Fundraising · Ops</p>

  <div class="input-card">
    <label>What are you building?</label>
    <textarea id="desc" placeholder="Be specific — industry, who you sell to, what problem you solve.&#10;&#10;Example: AI tool for procurement teams in manufacturing companies to automate RFQ processing and supplier communication"></textarea>
    <input type="text" id="name" placeholder="Startup name (optional)">
    <button class="run-btn" id="run-btn" onclick="startRun()">Run FounderBrain →</button>
  </div>

  <div class="progress-bar" id="progress-bar">
    <div class="progress-fill" id="progress-fill"></div>
  </div>

  <div class="agents" id="agents">
    <div class="wave-label">Wave 1 — parallel</div>
    <div class="agent-row" id="row-market"><div class="agent-icon icon-waiting" id="icon-market">📊</div><div><div class="agent-name">Market</div><div class="agent-status" id="status-market">Waiting...</div><div class="agent-summary" id="summary-market"></div></div></div>
    <div class="agent-row" id="row-legal"><div class="agent-icon icon-waiting" id="icon-legal">⚖️</div><div><div class="agent-name">Legal</div><div class="agent-status" id="status-legal">Waiting...</div><div class="agent-summary" id="summary-legal"></div></div></div>
    <div class="wave-label">Wave 2 — parallel</div>
    <div class="agent-row" id="row-customer"><div class="agent-icon icon-waiting" id="icon-customer">🎯</div><div><div class="agent-name">Customer</div><div class="agent-status" id="status-customer">Waiting...</div><div class="agent-summary" id="summary-customer"></div></div></div>
    <div class="agent-row" id="row-gtm"><div class="agent-icon icon-waiting" id="icon-gtm">🚀</div><div><div class="agent-name">GTM</div><div class="agent-status" id="status-gtm">Waiting...</div><div class="agent-summary" id="summary-gtm"></div></div></div>
    <div class="wave-label">Wave 3 — parallel</div>
    <div class="agent-row" id="row-hiring"><div class="agent-icon icon-waiting" id="icon-hiring">👥</div><div><div class="agent-name">Hiring</div><div class="agent-status" id="status-hiring">Waiting...</div><div class="agent-summary" id="summary-hiring"></div></div></div>
    <div class="agent-row" id="row-fundraising"><div class="agent-icon icon-waiting" id="icon-fundraising">💰</div><div><div class="agent-name">Fundraising</div><div class="agent-status" id="status-fundraising">Waiting...</div><div class="agent-summary" id="summary-fundraising"></div></div></div>
    <div class="wave-label">Wave 4</div>
    <div class="agent-row" id="row-ops"><div class="agent-icon icon-waiting" id="icon-ops">📅</div><div><div class="agent-name">Ops</div><div class="agent-status" id="status-ops">Waiting...</div><div class="agent-summary" id="summary-ops"></div></div></div>
  </div>

  <div class="report" id="report">
    <div class="report-card">
      <div class="report-title" id="report-title">Report ready</div>
      <div id="report-sections"></div>
      <a class="dl-btn" id="dl-md" href="#" download>⬇ Download Markdown</a>
      <a class="dl-btn" id="dl-json" href="#" download>⬇ Download JSON</a>
    </div>
  </div>
</div>

<script>
let runId = null;
let pollInterval = null;

async function startRun() {
  const desc = document.getElementById('desc').value.trim();
  const name = document.getElementById('name').value.trim() || 'My Startup';
  if (!desc) return;

  document.getElementById('run-btn').disabled = true;
  document.getElementById('agents').style.display = 'block';
  document.getElementById('report').style.display = 'none';
  document.getElementById('progress-bar').style.display = 'block';

  const r = await fetch('/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({description: desc, startup_name: name})
  });
  const data = await r.json();
  runId = data.run_id;

  pollInterval = setInterval(poll, 2000);
}

async function poll() {
  if (!runId) return;
  const r = await fetch(`/status/${runId}`);
  const data = await r.json();

  // Update agent statuses
  const agents = ['market', 'legal', 'customer', 'gtm', 'hiring', 'fundraising', 'ops'];
  let done = 0;
  agents.forEach(name => {
    const agent = data.agents[name];
    if (!agent) return;
    setAgent(name, agent.status, agent.summary || '');
    if (agent.status === 'complete' || agent.status === 'failed') done++;
  });

  // Update progress
  document.getElementById('progress-fill').style.width = Math.round((done / agents.length) * 100) + '%';

  if (data.complete) {
    clearInterval(pollInterval);
    showReport(data);
    document.getElementById('run-btn').disabled = false;
  }
}

function setAgent(name, status, summary) {
  const icon = document.getElementById(`icon-${name}`);
  const statusEl = document.getElementById(`status-${name}`);
  const summaryEl = document.getElementById(`summary-${name}`);

  icon.className = 'agent-icon';
  if (status === 'running') {
    icon.classList.add('icon-running');
    statusEl.textContent = 'Running...';
  } else if (status === 'complete') {
    icon.classList.add('icon-done');
    statusEl.textContent = 'Complete';
    summaryEl.textContent = summary;
  } else if (status === 'failed') {
    icon.classList.add('icon-failed');
    statusEl.textContent = 'Failed';
  } else {
    icon.classList.add('icon-waiting');
    statusEl.textContent = 'Waiting...';
  }
}

function showReport(data) {
  document.getElementById('report').style.display = 'block';
  document.getElementById('report-title').textContent = `${data.startup_name} — FounderBrain Report`;

  const labels = {
    market: '📊 Market Analysis', legal: '⚖️ Legal',
    customer: '🎯 Customer & ICP', gtm: '🚀 GTM Strategy',
    hiring: '👥 Hiring Plan', fundraising: '💰 Fundraising',
    ops: '📅 90-Day Ops Plan'
  };

  const container = document.getElementById('report-sections');
  container.innerHTML = '';

  Object.entries(data.agents).forEach(([name, agent]) => {
    if (agent.status !== 'complete') return;
    const facts = (agent.key_facts || []).slice(0, 3)
      .map(f => `<div class="fact">${f}</div>`).join('');
    container.innerHTML += `
      <div class="section-card">
        <div class="section-title">${labels[name] || name}</div>
        <div class="section-summary">${agent.summary || ''}</div>
        <div class="section-facts">${facts}</div>
      </div>`;
  });

  if (data.report_url) {
    document.getElementById('dl-md').href = `/download/${data.run_id}/md`;
    document.getElementById('dl-json').href = `/download/${data.run_id}/json`;
  }
}
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/run", methods=["POST"])
def run():
    data = request.json
    description = data.get("description", "")
    startup_name = data.get("startup_name", "My Startup")

    import uuid
    run_id = str(uuid.uuid4())[:8]
    active_runs[run_id] = {
        "startup_name": startup_name,
        "description": description,
        "complete": False,
        "agents": {},
        "memory": None,
        "report_path": None,
    }

    def run_in_background():
        orchestrator = Orchestrator()

        # Monkey-patch to capture status updates
        original_run_single = orchestrator._run_single
        original_run_parallel = orchestrator._run_parallel

        def tracked_run_single(agent_name, memory):
            active_runs[run_id]["agents"][agent_name] = {"status": "running", "summary": ""}
            original_run_single(agent_name, memory)
            out = getattr(memory, f"{agent_name}_output", None)
            if out:
                active_runs[run_id]["agents"][agent_name] = {
                    "status": out.status,
                    "summary": out.summary,
                    "key_facts": out.key_facts or [],
                }

        def tracked_run_parallel(agent_names, memory):
            for name in agent_names:
                active_runs[run_id]["agents"][name] = {"status": "running", "summary": ""}
            original_run_parallel(agent_names, memory)
            for name in agent_names:
                out = getattr(memory, f"{name}_output", None)
                if out:
                    active_runs[run_id]["agents"][name] = {
                        "status": out.status,
                        "summary": out.summary,
                        "key_facts": out.key_facts or [],
                    }

        orchestrator._run_single = tracked_run_single
        orchestrator._run_parallel = tracked_run_parallel

        memory = orchestrator.run(description, startup_name)
        report_path = generate_report(memory)

        active_runs[run_id]["complete"] = True
        active_runs[run_id]["memory"] = memory
        active_runs[run_id]["report_path"] = report_path

    thread = threading.Thread(target=run_in_background, daemon=True)
    thread.start()

    return jsonify({"run_id": run_id})


@app.route("/status/<run_id>")
def status(run_id):
    run = active_runs.get(run_id, {})
    return jsonify({
        "run_id": run_id,
        "startup_name": run.get("startup_name", ""),
        "complete": run.get("complete", False),
        "agents": run.get("agents", {}),
        "report_url": run.get("report_path"),
    })


@app.route("/download/<run_id>/<fmt>")
def download(run_id, fmt):
    run = active_runs.get(run_id, {})
    memory = run.get("memory")
    if not memory:
        return "Run not found", 404

    if fmt == "json":
        exporter = JSONExporter()
        path = exporter.export(memory)
        return open(path).read(), 200, {
            "Content-Type": "application/json",
            "Content-Disposition": f"attachment; filename=founderbrain_{run_id}.json"
        }
    else:
        path = run.get("report_path")
        if path:
            return open(path).read(), 200, {
                "Content-Type": "text/markdown",
                "Content-Disposition": f"attachment; filename=founderbrain_{run_id}.md"
            }

    return "Not found", 404


if __name__ == "__main__":
    print("\n🧠 FounderBrain web app")
    print("   Open: http://localhost:5000\n")
    app.run(debug=False, port=5000, threaded=True)
