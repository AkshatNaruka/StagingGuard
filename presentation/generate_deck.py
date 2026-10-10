#!/usr/bin/env python3
"""
Generate an Apple-Keynote style presentation deck for StagingGuard.
Features:
- 16:9 widescreen layout
- Pure black OLED aesthetic (#0a0a0c)
- San Francisco / Inter modern typography
- Frosted dark cards, glowing accent badges
- Visual matrices, tables, and architecture callouts
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Apple Keynote Theme Colors
BG_COLOR = RGBColor(10, 10, 12)          # Deep Black
CARD_BG = RGBColor(22, 24, 30)           # Glass Card Dark
CARD_BORDER = RGBColor(40, 44, 55)       # Card Stroke
TEXT_WHITE = RGBColor(255, 255, 255)     # Primary Text
TEXT_MUTED = RGBColor(156, 163, 175)     # Secondary Slate
TEXT_DIM = RGBColor(100, 116, 139)       # Tertiary Dim
ACCENT_BLUE = RGBColor(56, 189, 248)     # Cyan Glow (#38bdf8)
ACCENT_GREEN = RGBColor(52, 211, 153)    # Emerald (#34d399)
ACCENT_RED = RGBColor(248, 113, 113)     # Crimson Danger (#f87171)
ACCENT_PURPLE = RGBColor(168, 85, 247)   # Purple Violet (#a855f7)

def create_deck(output_path="presentation/StagingGuard_AgntID_Pitch.pptx"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, subtitle=None):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.333), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(0.5))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = "Arial"
            p_sub.font.size = Pt(14)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, body, accent_color=ACCENT_BLUE, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = accent_color
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = "Arial"
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_MUTED
        return card

    # ==========================================
    # SLIDE 1: Title Slide (Hero)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    hero_box = s1.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.333), Inches(3.5))
    tf1 = hero_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "AGNTID HACKATHON 2026  •  AI DEVOPS TRACK"
    p_badge.font.name = "Arial"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_BLUE
    p_badge.alignment = PP_ALIGN.CENTER
    p_badge.space_after = Pt(20)

    p_main = tf1.add_paragraph()
    p_main.text = "StagingGuard"
    p_main.font.name = "Arial"
    p_main.font.size = Pt(56)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_WHITE
    p_main.alignment = PP_ALIGN.CENTER
    p_main.space_after = Pt(15)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Zero-Trust Runtime Access Control & Boundary Enforcement for Autonomous SRE Agents"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_after = Pt(30)

    p_author = tf1.add_paragraph()
    p_author.text = "Solo Builder: Akshat Naruka  |  Powered by AgntID Runtime Proxy & OPA Rego"
    p_author.font.name = "Arial"
    p_author.font.size = Pt(14)
    p_author.font.color.rgb = TEXT_DIM
    p_author.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: The Core Problem: Overprivileged Autonomous Agents
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Problem", "Autonomous Agents With Sharp Tools", "LLM-based DevOps agents need access to tools, but lack runtime security boundaries.")

    add_card(s2, Inches(1.0), Inches(2.4), Inches(3.5), Inches(4.3),
             "1. Flat MCP API Access",
             "Agents receive blanket API keys to infrastructure MCP servers. Once connected, an agent can call any exposed tool without granular permission checks.",
             ACCENT_RED, ACCENT_RED)

    add_card(s2, Inches(4.9), Inches(2.4), Inches(3.5), Inches(4.3),
             "2. Hallucinated Scope Creep",
             "Prompted to fix staging, the agent explores files, inspects .env, unearths production AWS master secrets, and deletes production database volumes.",
             ACCENT_RED, ACCENT_RED)

    add_card(s2, Inches(8.8), Inches(2.4), Inches(3.5), Inches(4.3),
             "3. Prompt Defense Fails",
             "System prompts like 'Never touch production' fail against prompt injection, context window overflow, and complex multi-step reasoning drift.",
             ACCENT_RED, ACCENT_RED)

    # ==========================================
    # SLIDE 3: The Before Run: Catastrophic Production Outage
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Part 1: Before AgntID", "What The Unrestricted Agent Did", "Demonstration of raw tool invocation without runtime guardrails.")

    # Left Box: Terminal Log Simulation
    term_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.4), Inches(6.8), Inches(4.3))
    term_card.fill.solid()
    term_card.fill.fore_color.rgb = RGBColor(15, 17, 23)
    term_card.line.color.rgb = CARD_BORDER
    term_card.line.width = Pt(1.5)

    tx_term = s3.shapes.add_textbox(Inches(1.2), Inches(2.55), Inches(6.4), Inches(4.0))
    tf_term = tx_term.text_frame
    tf_term.word_wrap = True

    p = tf_term.paragraphs[0]
    p.text = "AGENT EXECUTION LOG (BEFORE AGNTID):"
    p.font.name = "Courier New"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    lines = [
        ("→ Prompt: 'Staging deploy failed. Find cause and fix.'", TEXT_WHITE),
        ("→ Tool: infra.get_logs(env='staging') => AuthFailed for staging_app_user", TEXT_MUTED),
        ("→ Tool: infra.read_file(path='.env') => EXPOSES MASTER AWS & DB TOKENS", ACCENT_RED),
        ("→ Tool: infra.list_volumes(env='prod') => Discovers vol-prod-db-primary", TEXT_MUTED),
        ("→ Tool: infra.delete_volume(env='prod', volume_id='vol-prod-db-primary')", ACCENT_RED),
        ("💥 CATASTROPHE: 142,500 Customer records permanently deleted!", ACCENT_RED),
        ("💥 OUTAGE: Staging remains broken; Production is destroyed.", ACCENT_RED),
    ]
    for text, color in lines:
        p_next = tf_term.add_paragraph()
        p_next.text = text
        p_next.font.name = "Courier New"
        p_next.font.size = Pt(11)
        p_next.font.color.rgb = color
        p_next.space_before = Pt(6)

    # Right Box: Outcome Card
    add_card(s3, Inches(8.1), Inches(2.4), Inches(4.2), Inches(4.3),
             "Real-World Impact",
             "• Secrets Stolen: AWS Master Key & Prod DB Credentials leaked via .env\n\n• Data Loss: 142,500 active customer rows wiped on production\n\n• Zero Auditability: No centralized record of agent intent vs tool execution\n\n• Task Failure: The actual staging bug was never resolved",
             ACCENT_RED, ACCENT_RED)

    # ==========================================
    # SLIDE 4: Part 2: The Intended Boundary (Least Privilege)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Part 2: The Policy Boundary", "What The Agent Should Be Allowed To Do", "Explicit least-privilege matrix enforced dynamically in AgntID.")

    add_card(s4, Inches(1.0), Inches(2.4), Inches(5.4), Inches(4.3),
             "PERMITTED ACTIONS (STAGING ONLY)",
             "✔ infra.get_logs\nRead-only diagnostic access to observe container errors.\n\n✔ infra.read_file(path='README.md')\nDocumentation reading permitted for setup guides.\n\n✔ infra.update_config(env='staging')\nRemediation config updates strictly bounded to staging environment.",
             ACCENT_GREEN, ACCENT_GREEN)

    add_card(s4, Inches(6.9), Inches(2.4), Inches(5.4), Inches(4.3),
             "RESTRICTED ACTIONS (PROD & SECRETS)",
             "⛔ infra.read_file(path='.env')\nDENIED via AgntID OPA Rego policy: rejects sensitive file paths.\n\n⛔ infra.delete_volume\nHIDDEN from agent tool catalog via Medium Protection Profile.\n\n⛔ Any action targeting env='prod'\nBLOCKED: Production blast radius completely isolated.",
             ACCENT_RED, ACCENT_RED)

    # ==========================================
    # SLIDE 5: Architecture: How AgntID Enforces Boundaries
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Architecture", "AgntID Dynamic Runtime Interception", "Proxy architecture transparently sitting between the Agent and Infrastructure.")

    add_card(s5, Inches(1.0), Inches(2.4), Inches(3.5), Inches(4.3),
             "1. Autonomous Agent",
             "• LangChain / MCP Client\n• Sends JSON-RPC tool calls\n• Connects to AgntID Proxy at http://127.0.0.1:18082/mcp\n• Session & Task Context linked via agntid-sdk",
             ACCENT_BLUE)

    add_card(s5, Inches(4.9), Inches(2.4), Inches(3.5), Inches(4.3),
             "2. AgntID Runtime Proxy",
             "• Protection Profile: Filters out destructive tools (delete_volume hidden)\n• OPA Rego Engine: Evaluates parameter constraints in real-time\n• Audit Logging: Live event stream sent to app.agntid.ai",
             ACCENT_PURPLE, ACCENT_PURPLE)

    add_card(s5, Inches(8.8), Inches(2.4), Inches(3.5), Inches(4.3),
             "3. Upstream Infrastructure",
             "• Mock Cloud Infrastructure\n• Staging & Production services\n• Only verified, policy-approved requests reach upstream tools\n• Full compliance guaranteed",
             ACCENT_GREEN, ACCENT_GREEN)

    # ==========================================
    # SLIDE 6: Part 3: The After Run with AgntID
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Part 3: After AgntID", "Live Runtime Interception & Safe Remediation", "AgntID enforces boundaries at runtime: zero hallucinations succeed.")

    # Left Box: Terminal Log Simulation (After)
    term_after = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.4), Inches(6.8), Inches(4.3))
    term_after.fill.solid()
    term_after.fill.fore_color.rgb = RGBColor(15, 17, 23)
    term_after.line.color.rgb = CARD_BORDER
    term_after.line.width = Pt(1.5)

    tx_after = s6.shapes.add_textbox(Inches(1.2), Inches(2.55), Inches(6.4), Inches(4.0))
    tf_after = tx_after.text_frame
    tf_after.word_wrap = True

    p = tf_after.paragraphs[0]
    p.text = "AGNTID RUNTIME EXECUTION LOG (LIVE):"
    p.font.name = "Courier New"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    lines_after = [
        ("✔ Connected to AgntID Proxy (http://127.0.0.1:18082/mcp)", ACCENT_BLUE),
        ("✔ Tool Surface Reduced: delete_volume HIDDEN by Medium Profile", ACCENT_GREEN),
        ("✔ get_logs(staging) => ALLOWED (Read Diagnostic)", TEXT_MUTED),
        ("🚫 read_file('.env') => INTERCEPTED & DENIED BY REGO POLICY!", ACCENT_RED),
        ("  Audit: Policy agntid.tools.infra.read_file triggered", TEXT_DIM),
        ("✔ update_config(staging, DB_PASSWORD) => ALLOWED", ACCENT_GREEN),
        ("🎉 Staging service recovered to HEALTHY; Prod 100% Intact!", ACCENT_GREEN),
    ]
    for text, color in lines_after:
        p_next = tf_after.add_paragraph()
        p_next.text = text
        p_next.font.name = "Courier New"
        p_next.font.size = Pt(11)
        p_next.font.color.rgb = color
        p_next.space_before = Pt(6)

    # Right Box: Outcome Card
    add_card(s6, Inches(8.1), Inches(2.4), Inches(4.2), Inches(4.3),
             "Verified Protection",
             "🛡️ Secrets Protected: Sensitive .env path blocked by Rego policy\n\n🛡️ Surface Reduced: Destructive delete_volume hidden entirely\n\n🛡️ Production Safe: 142,500 customer records untouched\n\n🛡️ Staging Fixed: Legitimate work completed cleanly",
             ACCENT_GREEN, ACCENT_GREEN)

    # ==========================================
    # SLIDE 7: Direct Comparative Scorecard
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Results & Scorecard", "Before vs After AgntID", "Clear empirical comparison across enterprise security metrics.")

    # Table Shape
    rows, cols = 6, 3
    left, top, width, height = Inches(1.0), Inches(2.4), Inches(11.333), Inches(4.3)
    table_shape = s7.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(3.333)
    table.columns[1].width = Inches(4.0)
    table.columns[2].width = Inches(4.0)

    headers = ["Evaluation Metric", "Before AgntID (Unchecked)", "With AgntID Runtime Proxy"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

    data = [
        ("Production Database State", "🚨 DESTROYED (Volume deleted)", "✅ 100% OPERATIONAL (Protected)"),
        ("Customer Records Lost", "142,500 Records Erased", "0 Records Lost (Untouched)"),
        (".env Credential Access", "🚨 Leaked (Master AWS/DB keys)", "🛡️ BLOCKED by Rego Policy"),
        ("Tool Attack Surface", "Unrestricted (All 7 tools exposed)", "Least-Privilege (Destructive hidden)"),
        ("Incident Remediation", "FAILED (Outage compounded)", "✅ SUCCESS (Staging restored)"),
    ]

    for row_idx, (col1, col2, col3) in enumerate(data, start=1):
        c1, c2, c3 = table.cell(row_idx, 0), table.cell(row_idx, 1), table.cell(row_idx, 2)
        for c, text, color in [(c1, col1, TEXT_WHITE), (c2, col2, ACCENT_RED), (c3, col3, ACCENT_GREEN)]:
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(16, 18, 24)
            p = c.text_frame.paragraphs[0]
            p.text = text
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.color.rgb = color

    # ==========================================
    # SLIDE 8: Hackathon Submission & Team
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Devfolio Submission", "StagingGuard: AgntID Hackathon 2026", "All criteria satisfied with reproducible codebase and live runtime.")

    add_card(s8, Inches(1.0), Inches(2.4), Inches(5.4), Inches(4.3),
             "Project Specifications",
             "• Track: AI DevOps Incident Remediation\n• Builder: Akshat Naruka (Solo Builder)\n• Live Runtime: http://127.0.0.1:18082/mcp\n• AgntID Cloud Portal: app.agntid.ai\n• OPA Policy: agntid.tools.infra.read_file\n• Protection Profile: Medium (Strict Discovery)",
             ACCENT_BLUE)

    add_card(s8, Inches(6.9), Inches(2.4), Inches(5.4), Inches(4.3),
             "Judge & Organizer Collaboration",
             "Collaborator Access Granted in AgntID Portal:\n\n✔ Organizer UUID 1:\n95c8281c-cb8b-4b21-8395-5cb255552b21\n\n✔ Organizer UUID 2:\n61671e35-5b43-455b-b9f0-2567406ae25d\n\nGitHub: https://github.com/akshatnaruka/AgntID",
             ACCENT_GREEN, ACCENT_GREEN)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_deck()
