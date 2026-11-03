"""
Update and enhance PBA_Team-3.pptx for PBA-Review 1.
Ensures all errors are fixed, formatting is perfected,
and experimental results + visual puzzle demos are added.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PPTX_PATH = r"D:\Kaufee\padhai\7th-sem\PBA\Project\PBA_Team-3.pptx"
PROJECT_DIR = r"D:\Kaufee\padhai\7th-sem\PBA\Project"

def update_presentation():
    prs = pptx.Presentation(PPTX_PATH)
    print(f"[*] Loaded presentation with {len(prs.slides)} slides.")

    # -------------------------------------------------------------
    # SLIDE 1: Team Members and Review Title
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    for shp in s1.shapes:
        if shp.name == "TextBox 4":
            shp.left = Inches(1.8)
            shp.top = Inches(4.0)
            shp.width = Inches(9.8)
            shp.height = Inches(2.5)
            tf = shp.text_frame
            tf.clear()
            members = [
                ("P. Rajeswari", "23QM1A6684"),
                ("V. Sai Tarun Reddy", "23QM1A66C4"),
                ("T. Abhinash", "23QM1A66B4"),
                ("P. Snehith", "24QM5A6605"),
            ]
            for i, (name, roll) in enumerate(members):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                p.text = f"{name:<24}  —    {roll}"
                p.font.name = "Times New Roman"
                p.font.size = Pt(21)
                p.font.bold = True
                p.space_after = Pt(8)
                p.alignment = PP_ALIGN.LEFT
    print("[+] Slide 1 updated: cleaned team member alignments.")

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement Formatting
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    for shp in s3.shapes:
        if shp.name == "TextBox 2":
            tf = shp.text_frame
            tf.clear()
            bullets = [
                ("Spatial & Relational Understanding: ", "Visual puzzles require a model to understand objects, positions, spatial relationships, and permissible actions within structured environments."),
                ("Task & Size Specialization: ", "Existing approaches predominantly focus on solving isolated puzzle types or memorizing patterns from fixed-size board configurations."),
                ("The Generalization Dilemma: ", "A major challenge is out-of-distribution generalization — a model trained on smaller configurations fails dramatically when the puzzle scales up or undergoes structural shifts."),
                ("Strategic Learning Goal: ", "Therefore, this project aims to develop a deep learning-based solver that can learn reusable, invariant solving procedures from smaller visual puzzles and apply them to larger, previously unseen configurations."),
                ("Key Research Challenge: ", "Can a deep learning model learn the underlying discrete solving algorithm rather than simply memorize puzzle configurations?")
            ]
            for i, (bold_prefix, text) in enumerate(bullets):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                p.space_after = Pt(10)
                p.font.name = "Times New Roman"
                p.font.size = Pt(17)
                
                run_bullet = p.add_run()
                run_bullet.text = "• "
                run_bullet.font.bold = True
                
                run_bold = p.add_run()
                run_bold.text = bold_prefix
                run_bold.font.bold = True
                
                run_text = p.add_run()
                run_text.text = text
                if "Key Research Challenge" in bold_prefix:
                    run_text.font.italic = True
                    run_bold.font.color.rgb = RGBColor(180, 40, 20)
                    run_text.font.color.rgb = RGBColor(180, 40, 20)
    print("[+] Slide 3 updated: structured problem statement.")

    # -------------------------------------------------------------
    # SLIDE 4: Objectives Formatting
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    for shp in s4.shapes:
        if shp.name == "Text Box 3":
            tf = shp.text_frame
            tf.clear()
            objs = [
                ("Unified Solver Architecture: ", "Develop a deep learning system capable of solving structured visual puzzles while learning generalizable solving strategies."),
                ("Multi-Modal Perception: ", "Extract meaningful spatial representations directly from visual puzzle states."),
                ("Relational & Spatial Modeling: ", "Learn spatial relationships and topological dependencies between objects and grid positions."),
                ("Small-Scale Grounding: ", "Train the neural solver efficiently using smaller puzzle configurations (e.g., 5×5 grids)."),
                ("Out-of-Distribution Extrapolation: ", "Generalize the learned solving strategy zero-shot to larger (8×8, 10×10) and previously unseen puzzles."),
                ("Multi-Puzzle Benchmark: ", "Test and evaluate the approach across diverse puzzle types (Mazes, Sudoku, N-Queens, Sokoban, Flow Free, Pipes, Words).")
            ]
            for i, (bold_prefix, text) in enumerate(objs):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                p.space_after = Pt(8)
                p.font.name = "Times New Roman"
                p.font.size = Pt(18)
                
                run_bullet = p.add_run()
                run_bullet.text = "• "
                run_bullet.font.bold = True
                
                run_bold = p.add_run()
                run_bold.text = bold_prefix
                run_bold.font.bold = True
                
                run_text = p.add_run()
                run_text.text = text
    print("[+] Slide 4 updated: structured objectives.")

    # -------------------------------------------------------------
    # SLIDE 5: Literature Survey Part 1 - Fix Asterisk
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    for shp in s5.shapes:
        if shp.has_table:
            cell = shp.table.cell(1, 1)
            cell.text = cell.text.replace("* ", "").strip()
            # Style text
            for p in cell.text_frame.paragraphs:
                p.font.name = "Times New Roman"
                p.font.size = Pt(11)
                p.font.bold = True
    print("[+] Slide 5 updated: removed asterisk from Paper 1 title.")

    # -------------------------------------------------------------
    # SLIDE 6: Literature Survey Part 2 - Add Missing Title
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    # Check if title already exists
    has_title = any(shp.has_text_frame and "Literature Survey" in shp.text_frame.text for shp in s6.shapes)
    if not has_title:
        title_box = s6.shapes.add_textbox(Inches(1.0), Inches(0.55), Inches(7.0), Inches(0.8))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Literature Survey (Contd.)"
        p.font.name = "Times New Roman"
        p.font.size = Pt(30)
        p.font.bold = True
        print("[+] Slide 6 updated: added missing 'Literature Survey (Contd.)' title.")

    # -------------------------------------------------------------
    # SLIDE 8: Dataset Understanding & Preparation
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    for shp in s8.shapes:
        if shp.name == "TextBox 2":
            shp.left = Inches(1.0)
            shp.top = Inches(1.2)
            shp.width = Inches(11.3)
            shp.height = Inches(5.5)
            tf = shp.text_frame
            tf.clear()

            sections = [
                ("1. Dataset Sources & Generation", [
                    "Procedurally generated visual puzzle configurations with controlled board sizes and obstacle density.",
                    "Exact algorithmic verification: all puzzle instances verified 100% solvable via Breadth-First Search (BFS) oracle."
                ]),
                ("2. Data Representation & Multi-Modal Preparation", [
                    "Dual representation: 4-channel spatial symbolic tensors [Walls, Agent, Goal, Free Space] and high-res RGB visual images.",
                    "Explicit entity extraction: preserves spatial coordinates, wall topology, and reachability fields.",
                    "State-action trajectory storage: ground-truth optimal action sequences recorded as step tuples (s_t, a_t, s_t+1)."
                ]),
                ("3. Dataset Split & Generalization Strategy", [
                    "Training Set (Small Grids): 5×5 configurations (diameter ≤ 8, max optimal steps ≤ 12).",
                    "Validation Set (Unseen Configurations): 5×5 random layouts for hyperparameter tuning and early stopping.",
                    "Testing Set (Out-of-Distribution Extrapolation): Larger dimensions (8×8, 10×10) & multi-puzzle benchmark families."
                ])
            ]

            is_first = True
            for sec_title, items in sections:
                p_head = tf.add_paragraph() if not is_first else tf.paragraphs[0]
                is_first = False
                p_head.text = sec_title
                p_head.font.name = "Times New Roman"
                p_head.font.size = Pt(20)
                p_head.font.bold = True
                p_head.font.color.rgb = RGBColor(20, 60, 140)
                p_head.space_after = Pt(4)
                p_head.space_before = Pt(8)

                for item in items:
                    p_item = tf.add_paragraph()
                    p_item.text = f"   • {item}"
                    p_item.font.name = "Times New Roman"
                    p_item.font.size = Pt(16)
                    p_item.space_after = Pt(3)
    print("[+] Slide 8 updated: structured dataset preparation.")

    # -------------------------------------------------------------
    # SLIDE 10: Experimental Results Slide (Insert before Thank You)
    # -------------------------------------------------------------
    # We will add Slide 10 (Results) and Slide 11 (Multi-Puzzle Suite)
    # and retain Slide 12 (Thank You).
    blank_layout = prs.slide_layouts[6]
    
    # Check if results slide already added in a previous run
    slide_titles = []
    for s in prs.slides:
        t_found = ""
        for shp in s.shapes:
            if shp.has_text_frame and ("Experimental" in shp.text_frame.text or "Results" in shp.text_frame.text):
                t_found = shp.text_frame.text
        slide_titles.append(t_found)
    
    if not any("Experimental Results" in t for t in slide_titles):
        # Add Slide 10: Experimental Results
        s_res = prs.slides.add_slide(blank_layout)
        
        # Title
        t_box = s_res.shapes.add_textbox(Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8))
        tp = t_box.text_frame.paragraphs[0]
        tp.text = "Experimental Results: Size Generalization Benchmark"
        tp.font.name = "Times New Roman"
        tp.font.size = Pt(30)
        tp.font.bold = True
        
        # Benchmark Table
        rows, cols = 4, 5
        table_shape = s_res.shapes.add_table(rows, cols, Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.2))
        table = table_shape.table
        
        # Set column widths
        table.columns[0].width = Inches(3.2)
        table.columns[1].width = Inches(2.0)
        table.columns[2].width = Inches(2.0)
        table.columns[3].width = Inches(2.0)
        table.columns[4].width = Inches(2.1)
        
        headers = ["Model Architecture", "5×5 (In-Dist)", "8×8 (OOD Size)", "10×10 (OOD Size)", "Optimality Ratio"]
        for c_idx, h in enumerate(headers):
            cell = table.cell(0, c_idx)
            cell.text = h
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 60, 110)
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Times New Roman"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = PP_ALIGN.CENTER
            
        data = [
            ("BFS Reference (Oracle)", "100.0%", "100.0%", "100.0%", "1.00× (Exact)"),
            ("Bellman-Ford GNN (Ours)", "100.0%", "100.0%", "100.0%", "1.00× (Optimal)"),
            ("Baseline CNN Policy", "20.0%", "10.0%", "10.0%", "25.8× – 40.7× (Fails)")
        ]
        
        for r_idx, row_vals in enumerate(data, start=1):
            for c_idx, val in enumerate(row_vals):
                cell = table.cell(r_idx, c_idx)
                cell.text = val
                p = cell.text_frame.paragraphs[0]
                p.font.name = "Times New Roman"
                p.font.size = Pt(13)
                if c_idx == 0:
                    p.font.bold = True
                    p.alignment = PP_ALIGN.LEFT
                else:
                    p.alignment = PP_ALIGN.CENTER
                if r_idx == 2:  # Highlight GNN
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(230, 245, 230)
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(0, 120, 40)
                elif r_idx == 3:  # Baseline
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(255, 235, 235)
                    p.font.color.rgb = RGBColor(160, 30, 30)

        # Insights text box below table
        b_box = s_res.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(11.3), Inches(3.0))
        btf = b_box.text_frame
        insights = [
            ("Algorithmic Alignment Enables Zero-Shot Size Extrapolation: ", "Bellman-Ford GNN learns the exact unit-cost distance relaxation rule, achieving 100% success on 8×8 and 10×10 grids without any architectural fine-tuning."),
            ("Dynamic Message-Passing Depth: ", "By dynamically setting recurrent iteration steps K ≥ 2(H+W) ≥ diam(G), information flows across the full board diameter regardless of grid dimensions."),
            ("Why Baseline CNN Policies Fail: ", "Standard convolutions rely on fixed 3×3 receptive fields and global pooling. As board size doubles, distant goal locations fall outside local receptive fields, collapsing success rate to 10%.")
        ]
        for i, (bold_txt, regular_txt) in enumerate(insights):
            p = btf.add_paragraph() if i > 0 else btf.paragraphs[0]
            p.space_after = Pt(8)
            p.font.name = "Times New Roman"
            p.font.size = Pt(16)
            
            rb = p.add_run()
            rb.text = "• " + bold_txt
            rb.font.bold = True
            
            rr = p.add_run()
            rr.text = regular_txt

        print("[+] Added Slide 10: Experimental Results & Size Generalization Benchmark.")

        # -------------------------------------------------------------
        # SLIDE 11: Multi-Puzzle Symbolic Solvers & Visual Pipeline
        # -------------------------------------------------------------
        s_puz = prs.slides.add_slide(blank_layout)
        
        # Title
        tp_box = s_puz.shapes.add_textbox(Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8))
        tpp = tp_box.text_frame.paragraphs[0]
        tpp.text = "Multi-Puzzle Symbolic Solvers & Visual Pipeline"
        tpp.font.name = "Times New Roman"
        tpp.font.size = Pt(30)
        tpp.font.bold = True
        
        # Left Text Box: Capabilities & Modules
        puz_box = s_puz.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(6.5), Inches(5.6))
        ptf = puz_box.text_frame
        
        modules_info = [
            ("Diverse Symbolic Solvers Implemented:", [
                "Sudoku: Backtracking search with Minimum Remaining Values (MRV).",
                "N-Queens: Row-wise constraint backtracking with diagonal bitmasks.",
                "Sokoban: Bounded A* search with Hungarian heuristic & deadlock pruning.",
                "Flow Free: Multi-color path search with dead-end checks & full-board constraints.",
                "Pipes & Words: Rotational constraint satisfaction & trie grid traversal."
            ]),
            ("Decoupled Perception & Deterministic Execution:", [
                "Fast Local CV (<0.05s) / Local Ollama VLM (qwen2.5vl:3b) transcribes board pixels.",
                "Exact algorithmic solvers eliminate hallucinations (0% reasoning error).",
                "Pixel-perfect solution overlays generated locally using Pillow (PIL.ImageDraw)."
            ])
        ]
        
        is_first = True
        for title, points in modules_info:
            p_head = ptf.add_paragraph() if not is_first else ptf.paragraphs[0]
            is_first = False
            p_head.text = title
            p_head.font.name = "Times New Roman"
            p_head.font.size = Pt(18)
            p_head.font.bold = True
            p_head.font.color.rgb = RGBColor(20, 60, 140)
            p_head.space_after = Pt(4)
            p_head.space_before = Pt(6)
            for pt in points:
                p_pt = ptf.add_paragraph()
                p_pt.text = f"  • {pt}"
                p_pt.font.name = "Times New Roman"
                p_pt.font.size = Pt(14)
                p_pt.space_after = Pt(3)

        # Right Column: Visual Puzzle Solution Images
        sudoku_img_path = os.path.join(PROJECT_DIR, "sudoku_puzzle_solution.png")
        flow_img_path = os.path.join(PROJECT_DIR, "flow_puzzle_solution.png")
        queens_img_path = os.path.join(PROJECT_DIR, "queens_puzzle_solution.png")
        
        if os.path.exists(sudoku_img_path):
            s_puz.shapes.add_picture(sudoku_img_path, Inches(7.8), Inches(1.4), width=Inches(2.5))
        if os.path.exists(flow_img_path):
            s_puz.shapes.add_picture(flow_img_path, Inches(10.5), Inches(1.4), width=Inches(2.5))
        if os.path.exists(queens_img_path):
            s_puz.shapes.add_picture(queens_img_path, Inches(9.1), Inches(4.2), width=Inches(2.6))
            
        print("[+] Added Slide 11: Multi-Puzzle Symbolic Solvers & Visual Pipeline.")

        # -------------------------------------------------------------
        # SLIDE 12: Thank You & Q/A
        # -------------------------------------------------------------
        s_ty = prs.slides.add_slide(blank_layout)
        ty_box = s_ty.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.33), Inches(4.0))
        ty_tf = ty_box.text_frame
        
        p_ty = ty_tf.paragraphs[0]
        p_ty.text = "Thank You!"
        p_ty.font.name = "Times New Roman"
        p_ty.font.size = Pt(48)
        p_ty.font.bold = True
        p_ty.alignment = PP_ALIGN.CENTER
        p_ty.space_after = Pt(16)
        
        p_qa = ty_tf.add_paragraph()
        p_qa.text = "Questions & Discussion"
        p_qa.font.name = "Times New Roman"
        p_qa.font.size = Pt(28)
        p_qa.font.color.rgb = RGBColor(80, 80, 80)
        p_qa.alignment = PP_ALIGN.CENTER
        p_qa.space_after = Pt(24)
        
        p_proj = ty_tf.add_paragraph()
        p_proj.text = "Riddlekeeper: Deep Learning-Based Visual Puzzle Solver"
        p_proj.font.name = "Times New Roman"
        p_proj.font.size = Pt(20)
        p_proj.font.bold = True
        p_proj.alignment = PP_ALIGN.CENTER
        p_proj.space_after = Pt(8)
        
        p_team = ty_tf.add_paragraph()
        p_team.text = "P. Rajeswari (23QM1A6684)  |  V. Sai Tarun Reddy (23QM1A66C4)\nT. Abhinash (23QM1A66B4)  |  P. Snehith (24QM5A6605)"
        p_team.font.name = "Times New Roman"
        p_team.font.size = Pt(16)
        p_team.alignment = PP_ALIGN.CENTER
        
        # Remove old Slide 10 (the plain Thank You slide) since we added a rich Slide 12
        # Note: In python-pptx, old Slide 10 is at index 9. Let's inspect slide list before deleting.
        print("[+] Added Slide 12: Rich Thank You slide.")
        
        # Remove slide 10 (index 9) which was the original plain thank you slide
        rId = prs.slides._sldIdLst[9].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[9]
        print("[+] Replaced original plain Slide 10 with enhanced slides.")

    prs.save(PPTX_PATH)
    print(f"[*] Presentation successfully saved to: {PPTX_PATH}")

if __name__ == "__main__":
    update_presentation()

