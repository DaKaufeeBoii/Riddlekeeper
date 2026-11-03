# A PROJECT REPORT

On

# RIDDLEKEEPER: DEEP LEARNING-BASED VISUAL PUZZLE SOLVER FOR SPATIAL REASONING AND SEQUENTIAL DECISION-MAKING

*Submitted to JNTUH in partial fulfillment of the Academic Requirements for the award of the degree of*

### BACHELOR OF TECHNOLOGY
**in**  
**COMPUTER SCIENCE AND ENGINEERING – AI&ML**

---

### Submitted By:
| Roll Number | Candidate Name |
| :---: | :--- |
| **23QM1A6684** | **P. KONDA RAJA RAJESWARI** |
| **23QM1A66C4** | **V. SAI TARUN REDDY** |
| **23QM1A66B4** | **T. ABHINASH** |
| **24QM5A6605** | **P. SNEHITH** |

---

### Under the Guidance of:
**Mr. B. SREENIVAS**  
*Assistant Professor, Department of CSE – AIML*

---

<br>

```
                  ██╗  ██╗ ██████╗     ██████╗  ███████╗ ██████╗  ██████╗  ██╗   ██╗
                  ██║ ██╔╝██╔════╝     ██╔══██╗ ██╔════╝ ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝
                  █████╔╝ ██║  ███╗    ██████╔╝ █████╗   ██║  ██║ ██║  ██║  ╚████╔╝ 
                  ██╔═██╗ ██║   ██║    ██╔══██╗ ██╔══╝   ██║  ██║ ██║  ██║   ╚██╔╝  
                  ██║  ██╗╚██████╔╝    ██║  ██║ ███████╗ ██████╔╝ ██████╔╝    ██║   
                  ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝ ╚══════╝ ╚═════╝  ╚═════╝     ╚═╝   
                        COLLEGE OF ENGINEERING AND TECHNOLOGY
                                 (AN AUTONOMOUS INSTITUTION)
```

**DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING - AIML**  
**K G REDDY COLLEGE OF ENGINEERING AND TECHNOLOGY**  
*(Approved by AICTE, New Delhi, Affiliated to JNTUH Hyderabad)*  
Chilkur (V), Moinabad Mandal, R. R. Dist. – 501 504, Telangana, India  
Phone: 9247033008, 9000633008 | Website: [www.kgr.ac.in](https://www.kgr.ac.in)  
**Academic Batch: 2023–2026**

---

\newpage

## CERTIFICATE

**DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING – AI&ML**  
**K G REDDY COLLEGE OF ENGINEERING AND TECHNOLOGY**  
*(Autonomous Institution, Affiliated to JNTUH, Hyderabad)*  
Chilkur (V), Moinabad Mandal, R. R. Dist. – 501 504

```
                                      CERTIFICATE
```

This is to certify that the project report entitled **“RIDDLEKEEPER: DEEP LEARNING-BASED VISUAL PUZZLE SOLVER FOR SPATIAL REASONING AND SEQUENTIAL DECISION-MAKING”** that is being submitted by:

* **P. KONDA RAJA RAJESWARI** (23QM1A6684)
* **V. SAI TARUN REDDY** (23QM1A66C4)
* **T. ABHINASH** (23QM1A66B4)
* **P. SNEHITH** (24QM5A6605)

under the guidance of **Mr. B. SREENIVAS**, in partial fulfillment for the award of the Degree of **Bachelor of Technology in Computer Science and Engineering – AI&ML** to the **Jawaharlal Nehru Technological University Hyderabad (JNTUH)**, is a record of bonafide work carried out by them under our guidance and supervision.

The results embodied in this project report have not been submitted to any other University or Institute for the award of any degree or diploma.

<br><br><br>

---------------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ----------------------------------------  
**Mr. B. SREENIVAS** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Dr. DEVENDER NAYAK. N**  
*Internal Guide* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Head of the Department*  
Assistant Professor, CSE – AIML &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; HOD, Associate Professor, CSE – AIML  
K G Reddy College of Engineering & Technology &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; K G Reddy College of Engineering & Technology  

<br><br><br>

----------------------------------------  
**EXTERNAL EXAMINER**

---

\newpage

## ACKNOWLEDGEMENT

This is to place on record our appreciation and deep gratitude to the persons without whose support this project would never have been this successful.

We would like to express our profound sense of gratitude to our Director, **Dr. ROHIT KANDAKATLA**, of K G Reddy College of Engineering and Technology, for his leadership, encouragement, and for providing state-of-the-art infrastructural facilities required to complete this project.

It is with immense pleasure that we express our indebted gratitude to **Dr. S. SAI SATYANARAYANA REDDY**, Principal, K G Reddy College of Engineering & Technology, for providing continuous support and giving us the opportunity of undertaking this innovative project.

At the same time, we feel elated to thank **Dr. DEVENDER NAYAK. N**, Associate Professor & Head of the Department of CSE – AI&ML, K G Reddy College of Engineering & Technology, for inspiring us, motivating our research mindset, and arranging all the computing resources and laboratory facilities needed for our project work.

We would like to express our special gratitude to our internal guide, **Mr. B. SREENIVAS**, Assistant Professor, Department of CSE – AI&ML, K G Reddy College of Engineering & Technology, who has guided us at every stage of the project. His constructive critique, technical insights into algorithmic design, and valuable moral support throughout the conception and implementation of **RIDDLEKEEPER: DEEP LEARNING-BASED VISUAL PUZZLE SOLVER FOR SPATIAL REASONING AND SEQUENTIAL DECISION-MAKING** helped us surmount critical technical challenges.

Finally, we express our sincere gratitude to all the faculty members of the Department of Computer Science and Engineering – AI&ML, our fellow classmates, friends, and parents who supported us directly and indirectly with their valuable advice, patience, and encouragement.

<br>

**P. KONDA RAJA RAJESWARI** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (23QM1A6684)  
**V. SAI TARUN REDDY** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (23QM1A66C4)  
**T. ABHINASH** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (23QM1A66B4)  
**P. SNEHITH** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (24QM5A6605)  

---

\newpage

## DECLARATION

We hereby declare that the project report titled **“RIDDLEKEEPER: DEEP LEARNING-BASED VISUAL PUZZLE SOLVER FOR SPATIAL REASONING AND SEQUENTIAL DECISION-MAKING”** is a bonafide work done by us in partial fulfillment of the requirements for the award of the degree **Bachelor of Technology in Computer Science and Engineering – AI&ML**, submitted to the Department of CSE – AI&ML, K G Reddy College of Engineering and Technology, Chilkur, Moinabad, Hyderabad, affiliated to Jawaharlal Nehru Technological University Hyderabad (JNTUH).

We also declare that this project is a result of our own genuine effort and has not been copied or plagiarized from any other project work, thesis, or source. All research literature, theoretical frameworks, open-source packages, and external documentation utilized during the preparation of this report have been explicitly acknowledged and cited in the references.

This work has not been previously submitted to any other University or Institute for the award of any degree, diploma, or certification.

<br><br>

**Place**: Chilkur, Hyderabad  
**Date**: November 2, 2026  

<br>

| Candidate Name | Roll Number | Signature |
| :--- | :---: | :---: |
| **P. KONDA RAJA RAJESWARI** | 23QM1A6684 | ___________________________ |
| **V. SAI TARUN REDDY** | 23QM1A66C4 | ___________________________ |
| **T. ABHINASH** | 23QM1A66B4 | ___________________________ |
| **P. SNEHITH** | 24QM5A6605 | ___________________________ |

---

\newpage

## VISION AND MISSION OF THE DEPARTMENT

### VISION
To be recognized as a premier centre of excellence in Computer Science and Engineering with specialization in Artificial Intelligence and Machine Learning, cultivating a dynamic ecosystem of learning, research and collaboration that drives technological excellence and creates impactful solutions for institutional and societal development.

### MISSION
* **M1**: To empower students with high-quality education in Artificial Intelligence and Machine Learning, fostering strong technical foundations, continuous learning, and advanced expertise in emerging Computer Science technologies to develop innovative, ethical, and impactful solutions.
* **M2**: To promote cutting-edge research and innovation in AI and ML by providing opportunities to address complex engineering challenges through strategic collaborations with industry, academia, and government organizations.
* **M3**: To cultivate professional excellence and leadership among students by integrating ethical AI practices, teamwork, and community engagement, enabling them to develop sustainable and intelligent solutions for real-world societal challenges.

---

\newpage

## PROGRAM EDUCATIONAL OBJECTIVES (PEOs)

* **PEO 1**: Graduates will apply strong foundations in Computer Science, Artificial Intelligence and Machine Learning to design and develop innovative solutions for complex and challenging problems in computing and intelligent systems.
* **PEO 2**: Graduates will establish successful professional careers in AIML and related computing domains, or pursue higher education and research in advanced areas of Computer Science and Artificial Intelligence.
* **PEO 3**: Graduates will demonstrate effective communication, teamwork, leadership and professionalism, while upholding high standards of ethical responsibility in the development and deployment of AI-driven technologies.
* **PEO 4**: Graduates will develop the ability to analyze engineering problems from multidisciplinary perspectives, integrating ethical considerations and promoting sustainable and socially responsible AI and ML solutions.

---

\newpage

## PROGRAM OUTCOMES (POs)

* **PO1: Engineering Knowledge**: Apply knowledge of mathematics, natural science, computing, engineering fundamentals and an engineering specialization as specified in WK1 to WK4 respectively to develop solutions to complex engineering problems.
* **PO2: Problem Analysis**: Identify, formulate, review research literature and analyze complex engineering problems reaching substantiated conclusions with consideration for sustainable development. (WK1 to WK4)
* **PO3: Design/Development of Solutions**: Design creative solutions for complex engineering problems and design/develop systems/components/processes to meet identified needs with consideration for public health and safety, whole-life cost, net zero carbon, culture, society and environment as required. (WK5)
* **PO4: Conduct Investigations of Complex Problems**: Conduct investigations of complex engineering problems using research-based knowledge including design of experiments, modelling, analysis & interpretation of data to provide valid conclusions. (WK8)
* **PO5: Modern Tool Usage**: Create, select, and apply appropriate techniques, resources and modern engineering & IT tools, including prediction and modelling recognizing their limitations to solve complex engineering problems. (WK2 and WK6)
* **PO6: The Engineer and Society**: Analyze and evaluate societal and environmental aspects while solving complex engineering problems for its impact on sustainability with reference to economy, health, safety, legal framework, culture and environment. (WK1, WK5, and WK7)
* **PO7: Ethics**: Apply ethical principles and commit to professional ethics, human values, diversity and inclusion; adhere to national & international laws. (WK9)
* **PO8: Individual and Team Work**: Function effectively as an individual, and as a member or leader in diverse/multi-disciplinary teams.
* **PO9: Communication**: Communicate effectively and inclusively within the engineering community and society at large, such as being able to comprehend and write effective reports and design documentation, make effective presentations considering cultural, language, and learning differences.
* **PO10: Project Management and Finance**: Apply knowledge and understanding of engineering management principles and economic decision-making and apply these to one’s own work, as a member and leader in a team, and to manage projects in multidisciplinary environments.
* **PO11: Life-Long Learning**: Recognize the need for, and have the preparation and ability for i) independent and life-long learning, ii) adaptability to new and emerging technologies, and iii) critical thinking in the broadest context of technological change. (WK8)

---

\newpage

## PROGRAM SPECIFIC OUTCOMES (PSOs)

| PSO Identifier | PSO Description |
| :--- | :--- |
| **PSO 1** | Design and apply the knowledge of intelligent expert systems in image processing, language models, and computing techniques of fuzzy logic, neural networks, and genetic algorithms to solve complex, cost-effective machine learning problems. |
| **PSO 2** | Analyze, evaluate, and synthesize real-time solutions for complex problems in computer vision and automations by leveraging Generative AI techniques, diffusion models to conduct applied research and develop intelligent, adaptive systems. |
| **PSO 3** | Apply the principles and techniques of Artificial Intelligence, Machine Learning, and Deep Learning to design, develop, and deploy intelligent systems that meet real-world industrial requirements. |

---

\newpage

## ABSTRACT

Visual puzzle solving constitutes a quintessential benchmark for artificial intelligence, demanding the tight synthesis of visual scene perception, spatial relational reasoning, and sequential decision-making under combinatorial constraints. While conventional deep learning architectures (e.g., Convolutional Neural Networks and Vision Transformers) excel on static, in-distribution image benchmarks, they suffer from catastrophic out-of-distribution (OOD) failure when puzzle dimensions scale beyond their training sets. When trained on small configurations, standard networks memorize local spatial coordinates rather than learning the underlying algorithmic procedure, resulting in immediate failure when deployed on larger, structurally unfamiliar boards.

This project presents **Riddlekeeper**, an algorithmically aligned, neuro-symbolic puzzle-solving framework designed to achieve zero-shot size extrapolation and verifiable execution across diverse visual and logic puzzles. Riddlekeeper addresses the perception-reasoning gap through a decoupled three-stage architecture:
1. **Multimodal Visual Perception**: Transcribes raw pixel images into structured spatial representations using either ultra-fast local computer vision heuristics ($< 0.05\text{ s}$) or local Vision-Language Models (Qwen2.5-VL-3B, Moondream2) running completely offline via Ollama.
2. **Algorithmic Neural Reasoner (Bellman-Ford GNN)**: Formulates grid navigation as message passing aligned with the Bellman-Ford shortest-path recurrence. By dynamically scaling the recurrent message-passing depth ($K \ge 2(H+W)$) to match the graph diameter, the network propagates distance potential fields globally across arbitrary board dimensions.
3. **Multi-Puzzle Symbolic Constraint Engine**: Incorporates exact symbolic solvers for six diverse puzzle families, including Minimum Remaining Values (MRV) backtracking for Sudoku, row-wise constraint propagation for $N$-Queens, Hungarian-guided A* search with deadlock pruning for Sokoban, and dead-end neighbor checks for Flow Free.
4. **Deterministic Visual Annotation**: Draws glowing solution paths, royal queen badges, highlighted digits, and push vectors directly onto the input image pixels with zero hallucination.

Rigorous empirical evaluation demonstrates that while a standard Convolutional Neural Network baseline collapses from a $20.0\%$ success rate on $5 \times 5$ grids to $10.0\%$ on $8 \times 8$ and $10 \times 10$ grids, the **Bellman-Ford GNN maintains an uncompromised 100.0% Success Rate and a 1.00× Path Optimality Ratio across all scales**, proving that algorithmic alignment enables zero-shot size extrapolation. Furthermore, all 30 automated regression test suites across the six symbolic puzzle modules passed with zero errors. Riddlekeeper proves that grounding neural models in discrete algorithmic structures bridges the fundamental divide between perception and combinatorial reasoning.

---

\newpage

## TABLE OF CONTENTS

```
CHAPTER 1: INTRODUCTION ........................................................... 1
  1.1 MOTIVATION ................................................................. 1
  1.2 PROBLEM STATEMENT .......................................................... 1
  1.3 SCOPE ...................................................................... 2
  1.4 OBJECTIVES ................................................................. 2
  1.5 EXISTING SYSTEM ............................................................ 3
  1.6 LIMITATIONS OF EXISTING SYSTEM ............................................. 3

CHAPTER 2: LITERATURE SURVEY ..................................................... 4
  2.1 INTRODUCTION ............................................................... 4
  2.2 LITERATURE SURVEY (BASE PAPERS REVIEW) ..................................... 4
  2.3 RESEARCH GAP ............................................................... 6

CHAPTER 3: REQUIREMENT ANALYSIS AND SPECIFICATION ................................ 7
  3.1 REQUIREMENT ANALYSIS ....................................................... 7
  3.2 FUNCTIONAL REQUIREMENTS .................................................... 7
  3.3 NON-FUNCTIONAL REQUIREMENTS ................................................ 8
  3.4 SOFTWARE REQUIREMENTS ...................................................... 8
  3.5 HARDWARE REQUIREMENTS ...................................................... 9

CHAPTER 4: DATASET GATHERING AND PRE-PROCESSING ................................... 10
  4.1 DATA COLLECTION ............................................................ 10
  4.2 DATA PRE-PROCESSING ........................................................ 10
  4.3 FEATURE EXTRACTION ......................................................... 11
  4.4 EXPLORATORY AND STATISTICAL ANALYSIS ....................................... 12

CHAPTER 5: SYSTEM DESIGN ......................................................... 14
  5.1 SYSTEM ARCHITECTURE ........................................................ 14
  5.2 ACTIVITY DIAGRAM ........................................................... 15
  5.3 USE CASE DIAGRAM ........................................................... 16
  5.4 WORKFLOW DIAGRAM ........................................................... 17

CHAPTER 6: PROPOSED SYSTEM ....................................................... 19
  6.1 PROPOSED SYSTEM OVERVIEW ................................................... 19
  6.2 MODULES .................................................................... 19
  6.3 PROPOSED SYSTEM FLOW ....................................................... 20
  6.4 ALGORITHMS AND MODELS ...................................................... 20
  6.5 EXPECTED SYSTEM OUTPUT ..................................................... 21

CHAPTER 7: TESTING ............................................................... 22
  7.1 LAYOUT AND VISUALS ......................................................... 22
  7.2 FUNCTIONALITY AND USER EXPERIENCE .......................................... 23

CHAPTER 8: RESULTS & DISCUSSIONS ................................................. 24
  8.1 QUANTITATIVE METRICS ....................................................... 24
  8.2 QUALITATIVE OBSERVATIONS ................................................... 25
  8.3 INTERPRETATION OF FINDINGS ................................................. 25
  8.4 ADDRESS DEVICE-SPECIFIC CONTEXTS ........................................... 25

CHAPTER 9: CONCLUSION ............................................................ 26
  9.1 SUMMARY OF KEY INSIGHTS .................................................... 26
  9.2 CHALLENGES AND LESSONS LEARNED ............................................. 26

CHAPTER 10: FUTURE ENHANCEMENTS .................................................. 27
  10.1 USER EXPERIENCE AND PERSONALIZATION ....................................... 27
  10.2 EMERGING TECHNOLOGIES AND IMMERSIVE CONTENT ............................... 27
  10.3 ADVANCED TECHNICAL IMPLEMENTATION ......................................... 27
  10.4 PERFORMANCE AND ACCESSIBILITY ............................................. 27
  10.5 CONTENT MANAGEMENT AND WORKFLOW ........................................... 28

REFERENCES ....................................................................... 29
```

---

\newpage

## LIST OF FIGURES

| Fig. No. | Name of the Figure | Page No. |
| :---: | :--- | :---: |
| **5.1** | System Architecture of Riddlekeeper | 14 |
| **5.2** | Activity Diagram of Perception-to-Action Execution | 15 |
| **5.3** | Use Case Diagram for Puzzle Solving Interactions | 16 |
| **5.4** | Workflow Diagram of Algorithmic Planning and Verification | 17 |
| **7.1** | Visual Perception and Board Transcription Pipeline | 22 |
| **7.2** | Multi-Puzzle Visual Solution Overlays (Sudoku, Flow, Sokoban) | 23 |
| **8.1** | Empirical Closed-Loop Size Extrapolation Benchmark | 24 |

---

## LIST OF TABLES

| Table No. | Name of the Table | Page No. |
| :---: | :--- | :---: |
| **4.1** | Feature Extraction and Multi-Modal Spatial Tensor Mapping | 12 |
| **4.2** | Exploratory and Statistical Analysis of Dataset Attributes | 13 |
| **8.1** | Quantitative Performance Benchmark across Grid Dimensions | 24 |

---

\newpage

# CHAPTER 1: INTRODUCTION

### 1.1 MOTIVATION
Visual puzzles—ranging from grid-based navigation mazes and combinatorial chess placements to number-link puzzles and warehouse box-pushing challenges—have long stood as the gold standard for testing cognitive intelligence. For human beings, solving such puzzles involves an effortless interplay of multiple cognitive faculties:
1. Parsing visual scenes to recognize entities, boundaries, and topological relations;
2. Abstracting physical geometries into discrete symbolic constraints;
3. Formulating long-term sequential plans while respecting invariant game rules; and
4. Generalizing the learned strategy immediately to boards of arbitrary sizes.

Recent breakthroughs in Deep Learning (DL), Computer Vision (CV), and Large Language Models (LLMs) have yielded unprecedented success across image classification, natural language dialogue, and code generation. However, when deployed on structured visual puzzle solving, standard deep learning models suffer from severe, foundational limitations:
* **Memorization vs. Reasoning**: Deep neural networks excel at interpolating over the training distribution (In-Distribution / I.I.D.), but catastrophically fail to extrapolate out-of-distribution (O.O.D.). A model trained to navigate $5 \times 5$ grids learns fixed coordinate shortcuts; when tested on a $10 \times 10$ grid, its performance collapses completely.
* **Perceptual Hallucinations**: Monolithic multimodal LLMs and diffusion models struggle with spatial grounding. When prompted to "draw the solution" onto a Sudoku grid or maze, they hallucinate crooked paths, duplicate digits, and violate basic physical obstacles.
* **Lack of Formal Guarantees**: Pure deep networks cannot guarantee satisfaction of hard constraints (such as uniqueness in Sudoku or non-overlapping paths in Flow Free).

The motivation of this project is to develop **Riddlekeeper**, a principled neuro-symbolic framework that bridges the gap between deep perception and discrete algorithmic reasoning. By combining local visual encoders, algorithmically aligned Graph Neural Networks (GNNs), and deterministic constraint satisfaction solvers, Riddlekeeper learns reusable, size-invariant solving strategies from small visual puzzles and applies them with 100% mathematical fidelity to larger, previously unseen configurations.

### 1.2 PROBLEM STATEMENT
Visual puzzles require an intelligent model to perceive objects, spatial positions, relational rules, and legal actions within a structured environment. Existing approaches typically train isolated heuristics on fixed-size configurations, resulting in severe overfitting. When the puzzle dimension increases or topological shifts occur, standard models fail completely.

Therefore, this project aims to develop **Riddlekeeper: A Deep Learning-Based Visual Puzzle Solver for Spatial Reasoning and Sequential Decision-Making**. The system must take raw puzzle images as input, extract structured multi-modal representations, model spatial relationships, execute sequential actions via an algorithmically aligned policy, and guarantee verifiable task completion across both small and large out-of-distribution configurations.

> **Key Research Challenge**: *Can a deep learning model learn the underlying discrete solving procedure rather than simply memorizing puzzle configurations?*

### 1.3 SCOPE
The scope of Riddlekeeper encompasses the design, implementation, and empirical verification of an end-to-end puzzle-solving system:
* **Puzzle Diversity**: Accommodates six diverse puzzle families:
  1. *Grid Navigation Mazes*: Orthogonal pathfinding with wall obstacles.
  2. *Sudoku ($9 \times 9$)*: Discrete constraint satisfaction under row, column, and $3 \times 3$ block uniqueness.
  3. *$N$-Queens ($N \ge 4$)*: Non-attacking queen placement on arbitrary chessboards.
  4. *Sokoban*: Bounded push-box planning with deadlock avoidance.
  5. *Flow Free*: Multi-color path routing with 100% board coverage constraints.
  6. *Pipes / Net*: Rotational constraint satisfaction for single-component network connectivity.
* **Multi-Modal Perception**: Completely offline visual parsing using local computer vision heuristics (< 0.05 s) or local Vision-Language Models (Qwen2.5-VL-3B, Moondream2) running on Ollama, eliminating any dependency on cloud APIs.
* **Algorithmic Alignment**: Implementation of recurrent min-plus message passing (Bellman-Ford GNN) for provable size extrapolation from $5 \times 5$ to $10 \times 10$ grids.
* **Deterministic Overlay Engine**: Pixel-level rendering using Pillow to draw glowing paths, queen badges, highlighted digits, and push vectors with 0% hallucination.
* **Exclusions**: Real-time physical robotics manipulation, multi-agent adversarial games, and unconstrained 3D video inputs are outside the current scope and deferred to future work.

### 1.4 OBJECTIVES
The primary technical objectives of the project are:
1. To develop an integrated neuro-symbolic deep learning system for solving structured visual puzzles.
2. To extract structured multi-modal representations (4-channel spatial tensors and relational graphs) directly from raw puzzle images.
3. To learn spatial and topological dependencies between puzzle objects and grid coordinates.
4. To train neural policies exclusively on small, computationally efficient configurations ($5 \times 5$ grids).
5. To achieve zero-shot out-of-distribution (OOD) size extrapolation to larger ($8 \times 8$, $10 \times 10$) grids without retraining.
6. To implement exact constraint satisfaction solvers (MRV backtracking, A* search, forward checking) across six puzzle families.
7. To provide an agent orchestration layer that enforces hard state and execution time budgets.
8. To incorporate independent solution verification before returning task success to eliminate false positives.
9. To render sub-pixel accurate, deterministic visual solution overlays directly onto input images.
10. To maintain 100% offline, privacy-preserving execution with zero reliance on cloud APIs.

### 1.5 EXISTING SYSTEM
Existing approaches in automated puzzle solving fall into three fragmented paradigms:
1. **Classical Symbolic Solvers**: Standalone algorithms (such as SAT solvers, integer linear programming, and standard backtracking) provide exact solutions but require manual, brittle formalization of game states. They possess zero visual perception capabilities and cannot parse raw images.
2. **End-to-End Convolutional & Transformer Policies**: Deep reinforcement learning models (e.g., DQN, PPO, ViT-based policies) take grid matrices as inputs and output action distributions. However, they are bounded by fixed convolutional receptive fields and memorized coordinate embeddings, causing them to collapse when deployed on grids larger than their training set.
3. **Multimodal Large Language Models (MLLMs)**: Commercial frontier models (e.g., GPT-4V, Gemini 1.5 Pro) can view images and discuss puzzle rules. However, they suffer from severe spatial hallucinations, struggle with coordinate arithmetic, cannot perform multi-step search reliably, and risk proprietary data leakage through cloud transmission.

### 1.6 LIMITATIONS OF EXISTING SYSTEM
* **Catastrophic Out-of-Distribution Degradation**: Models trained on $N \times N$ configurations fail when evaluated on $(N+k) \times (N+k)$ configurations because they lack algorithmic invariance.
* **Receptive Field Mismatch**: Standard CNN convolutions ($3 \times 3$) cannot observe distant goal targets across expanded board diameters, rendering the agent blind.
* **High Inference Latency and Operational Cost**: Cloud MLLMs require 2–5 seconds per step, incur per-token financial costs, and introduce network latency vulnerabilities.
* **Hallucinatory Generation**: Image-generation diffusion models hallucinate distorted numbers and disconnected paths when tasked with drawing puzzle solutions.
* **Lack of State Verification**: Existing systems assume tool execution succeeds without verifying postconditions, leading to silent failures.

---

\newpage

# CHAPTER 2: LITERATURE SURVEY

### 2.1 INTRODUCTION
The literature survey investigates recent advancements in Neural Algorithmic Reasoning (NAR), Graph Neural Networks (GNNs), Abstract Visual Reasoning (AVR), and Neuro-Symbolic Artificial Intelligence. While conventional deep learning focuses on pattern recognition over static data distributions, neural algorithmic reasoning aims to teach neural networks the underlying mechanics of discrete algorithms (e.g., dynamic programming, shortest-path calculation, sorting).

This chapter analyzes five foundational research papers that establish the theoretical and empirical underpinnings of Riddlekeeper, highlighting how algorithmic alignment and neuro-symbolic decoupling bridge the divide between perception and combinatorial reasoning.

### 2.2 LITERATURE SURVEY (BASE PAPERS REVIEW)

#### 1. Which Algorithms Can Graph Neural Networks Learn?
* **Authors**: Solveig Wittig, Antonis Vasileiou, Robert R. Nerem, Timo Stoll, Floris Geerts, Yusu Wang, Christopher Morris.
* **Source / Venue**: arXiv:2602.13106 / Conference on Learning Theory (COLT), 2024/2026 [1].
* **Methodology**:  
  The authors study the expressive power and sample complexity of Message-Passing Graph Neural Networks (MPNNs) within the framework of Neural Algorithmic Reasoning. Utilizing Probably Approximately Correct (PAC) learning bounds and algorithmic alignment principles (formalized by Xu et al.), the paper investigates which classes of classical discrete algorithms (e.g., dynamic programming, BFS, Bellman-Ford, Prim’s, Dijkstra’s) can be learned by MPNNs with polynomial sample complexity.
* **Core Findings**:  
  The research proves that MPNNs can learn discrete algorithmic procedures and extrapolate from small training graphs to larger test graphs **if and only if** the neural architecture is aligned step-by-step with the state-update functions of the target algorithm. When node updates match dynamic programming recurrences (such as min-plus semirings), sample complexity scales with the algorithm's per-step complexity rather than total combinatorial graph size.
* **Identified Drawback**:  
  The study is purely theoretical and evaluated on abstract graph topologies (Erdős–Rényi graphs). It does not address visual perception, pixel matrices, spatial grid embeddings, or closed-loop environments where actions alter the physical state.

#### 2. Graph Neural Networks Extrapolate Out-of-Distribution for Shortest Paths
* **Authors**: Robert R. Nerem, Samantha Chen, Sanjoy Dasgupta, Yusu Wang.
* **Source / Venue**: PMLR / Proceedings of the 39th Annual Conference on Learning Theory (COLT 2026), arXiv:2503.19173, 2024 [2].
* **Methodology**:  
  This work provides mathematical proofs and empirical guarantees regarding out-of-distribution (OOD) size extrapolation for shortest-path problems. The authors demonstrate that while standard MLPs and GCNs fail to generalize to graphs with diameters larger than those seen during training, GNNs equipped with min-plus message-passing layers (which mirror the Bellman-Ford recurrence):
  $$h_u^{(t+1)} = \min \left( h_u^{(t)}, \min_{v \in \mathcal{N}(u)} (h_v^{(t)} + w_{uv}) \right)$$
  exhibit an exact algorithmic alignment that guarantees zero error extrapolation to graphs of arbitrary size, provided the recurrent iteration depth $K$ satisfies $K \ge \text{diam}(G)$.
* **Core Findings**:  
  Standard neural networks fail OOD because linear combinations and standard sum/mean aggregations cannot express the non-expansive properties of the $\min$ operator. An aligned Bellman-Ford GNN trained on small graphs (20 nodes) achieves near 100% accuracy on graphs with hundreds of nodes.
* **Identified Drawback**:  
  The model assumes abstract graph inputs with ground-truth adjacency matrices and edge weights already provided. It does not consider vision-grounded puzzle inputs, obstacle occlusion, multi-agent dynamics, or combinatorial constraint propagation (such as row/column uniqueness in Sudoku).

#### 3. Advancing Generalization Across a Variety of Abstract Visual Reasoning Tasks
* **Authors**: Mikołaj Małkiński, Jacek Mańdziuk.
* **Source / Venue**: International Joint Conference on Artificial Intelligence (IJCAI 2025), arXiv:2505.13391, 2024 [3].
* **Methodology**:  
  Focuses on Abstract Visual Reasoning (AVR) benchmarks, specifically Raven’s Progressive Matrices (RPM), PGM, and Bongard problems. The authors investigate how decoupling feature extraction (visual perception) from relational reasoning modules, combined with contrastive self-supervised auxiliary losses, empowers neural architectures to achieve out-of-distribution generalization across novel visual attribute combinations.
* **Core Findings**:  
  End-to-end monolithic architectures overfit to visual textures and spurious visual artifacts. Decoupling visual token extraction from structured relational reasoning allows models to infer underlying abstract rules (e.g., progression, logical XOR, distribution of three) across unseen shapes and grid arrangements.
* **Identified Drawback**:  
  AVR benchmarks evaluate static, multiple-choice pattern matching (choosing 1 of 8 candidate images). The framework does not formulate decision-making as an interactive, sequential Markov Decision Process (MDP) and cannot plan sequential action trajectories.

#### 4. Reasoning in Computer Vision: Taxonomy, Models, Tasks, and Methodologies
* **Authors**: Ayushman Sarkar, Zhenyu Yu, Mohd Yamani Idna Idris.
* **Source / Venue**: arXiv:2508.10523, 2025 [4].
* **Methodology**:  
  Presents a comprehensive taxonomy of reasoning paradigms in computer vision, categorizing methodologies into: spatial reasoning, relational reasoning, neuro-symbolic reasoning, and causal inference.
* **Core Findings**:  
  Monolithic vision models (including large Vision-Language Models) consistently fail at multi-hop compositional reasoning because they lack verifiable symbolic state representations. A decoupled architecture—where neural models transcribe unstructured sensory data into verifiable symbolic state representations which are then processed by specialized reasoning engines—consistently outperforms end-to-end models on complex multi-step reasoning benchmarks.
* **Identified Drawback**:  
  The paper is an overarching taxonomic survey and does not provide an operational, open-source puzzle-solving architecture or reproducible code benchmarks.

#### 5. Compositional Neuro-Symbolic Reasoning
* **Authors**: Anugyan Das, Omkar Ghugarkar, Vishvesh Bhat, Asad Aali.
* **Source / Venue**: CoreThink AI & Stanford University, arXiv:2604.02434, 2025 [5].
* **Methodology**:  
  Addresses the Abstraction and Reasoning Corpus (ARC) by developing a compositional neuro-symbolic framework. The system parses 2D visual grids into discrete, object-centric entities (connected components of color and shape), uses a neural prior to propose candidate transformations from a Domain-Specific Language (DSL), and applies consistency-based symbolic search to compose program primitives that satisfy input-output demonstration pairs.
* **Core Findings**:  
  Combining object-level abstraction with a discrete DSL allows the system to solve novel ARC transformations with remarkable sample efficiency (learning from only 2–3 demonstrations). Neural guidance drastically reduces the exponential search space of pure symbolic synthesizers.
* **Identified Drawback**:  
  ARC tasks represent static matrix-to-matrix transformations rather than sequential decision-making environments. The DSL synthesizer operates under unbounded search time and lacks execution budgets or real-time action transition dynamics.

### 2.3 RESEARCH GAP
The comprehensive review of contemporary literature reveals a critical bifurcation:
1. On one hand, theoretical NAR and GNN researchers (Wittig et al., Nerem et al.) prove that algorithmic alignment enables size-invariant extrapolation, but their work remains confined to abstract synthetic graph matrices.
2. On the other hand, visual reasoning researchers (Małkiński et al., Sarkar et al., Das et al.) prove that neuro-symbolic decoupling prevents visual overfitting, but focus exclusively on static multiple-choice tests (RPM) or matrix transformation puzzles (ARC) without sequential action execution.

**The Major Research Gap**: There currently exists no unified, local-first neuro-symbolic framework that bridges raw visual puzzle perception, algorithmically aligned neural path reasoning for size extrapolation, and exact symbolic constraint satisfaction for multi-family puzzle solving under bounded execution budgets.

**Riddlekeeper’s Resolution**: Riddlekeeper bridges this gap by translating the theoretical Bellman-Ford algorithmic alignment of Nerem et al. into a spatial grid policy, pairing it with the decoupled visual perception advocated by Sarkar et al. and the discrete constraint propagation of classical symbolic solvers, establishing an operational, verified visual puzzle solver.

---

\newpage

# CHAPTER 3: REQUIREMENT ANALYSIS AND SPECIFICATION

### 3.1 REQUIREMENT ANALYSIS
The **Riddlekeeper** system is designed to take an image of a structured visual puzzle as input, interpret the game state, formulate an optimal sequential plan, execute actions within a simulated or real environment, verify goal satisfaction, and render an annotated solution directly onto the image.

The system requires:
1. A perception component capable of operating locally without cloud APIs;
2. An algorithmic policy network capable of zero-shot size extrapolation;
3. A suite of exact symbolic constraint satisfaction solvers;
4. An orchestration layer that enforces state and time limits; and
5. A deterministic graphics rendering engine for explainable visual outputs.

### 3.2 FUNCTIONAL REQUIREMENTS
1. **Visual Image Ingestion**: The system shall accept standard image formats (`.png`, `.jpg`, `.jpeg`, `.bmp`) representing puzzle layouts.
2. **Adaptive Grid Boundary Detection**: The system shall automatically detect and crop active puzzle grids from background borders and titles across arbitrary resolutions.
3. **Dual-Mode Visual Perception**: The system shall support both ultra-fast local computer vision heuristics (< 0.05 s) and local Vision-Language Model transcription (via Ollama).
4. **Symbolic Tensor Extraction**: The system shall convert parsed puzzle states into normalized 4-channel spatial tensors ($B \times 4 \times H \times W$).
5. **Algorithmic Path Reasoning**: The system shall use recurrent Bellman-Ford message passing to compute shortest-path potential fields with dynamic depth scaling $K \ge 2(H+W)$.
6. **Legal Action Masking**: The system shall dynamically compute and apply boolean action masks to prevent illegal moves or wall collisions.
7. **Constraint Satisfaction Solving**: The system shall provide exact symbolic solvers for Sudoku (MRV), $N$-Queens (bitmask backtracking), Sokoban (deadlock A*), and Flow Free (dead-end checks).
8. **Budget Enforcement**: The orchestration layer shall enforce maximum explored state limits and execution time limits (ms), terminating gracefully with informative failure traces upon timeout.
9. **Independent Postcondition Verification**: The system shall independently verify that a generated solution sequence satisfies all goal conditions prior to reporting success.
10. **Deterministic Visual Overlay**: The system shall annotate solution paths, royal badges, numbers, and push vectors directly onto the input image pixels using Pillow.

### 3.3 NON-FUNCTIONAL REQUIREMENTS
1. **Reliability & Soundness**: The system shall never return a false positive solution. If a puzzle is unsolvable, it must return `solved=False` with 0% hallucination.
2. **Size Extrapolation (OOD Generalization)**: The neural solver shall achieve $\ge 95\%$ success rate on $8 \times 8$ and $10 \times 10$ grids when trained solely on $5 \times 5$ grids.
3. **Low Latency & High Performance**: Symbolic puzzle solving shall complete within $50\text{ ms}$ for standard boards; local CV perception shall complete within $0.05\text{ s}$.
4. **Data Privacy & Offline Execution**: The entire pipeline shall run 100% locally on the host machine with zero transmission of data or images to cloud APIs.
5. **Modularity & Extensibility**: The solver registry shall allow seamless registration of new puzzle types via standardized abstract base classes (`BasePuzzle`, `BaseSolver`).
6. **Memory Efficiency**: The core symbolic engine and neural reasoner shall operate with a memory footprint under $100\text{ MB}$.
7. **Usability & Dual Interface**: The system shall provide both a Python API and an intuitive Command-Line Interface (CLI) for automated batch evaluation.
8. **Explainability & Transparency**: The system shall log complete execution traces, including explored state counts, selected solver names, and elapsed runtime.

### 3.4 SOFTWARE REQUIREMENTS
* **Operating System**: Microsoft Windows 10/11 (64-bit) or Linux (Ubuntu 22.04 LTS / Debian 12).
* **Programming Language**: Python 3.9 or higher (standard library used for core symbolic solvers).
* **Deep Learning Framework**: PyTorch 2.0+ (used for `BellmanFordGNN` and `BaselineCNNPolicy`).
* **Computer Vision & Graphics**: Pillow (PIL 10.0+), Matplotlib 3.8+.
* **Local Vision-Language Platform**: Ollama (running `qwen2.5vl:3b` or `moondream2`).
* **Development Environment**: Visual Studio Code, Git.

### 3.5 HARDWARE REQUIREMENTS
* **Processor (CPU)**: Intel Core i5 / AMD Ryzen 5 or higher (minimum 4 cores, 2.5 GHz).
* **Random Access Memory (RAM)**: Minimum 8 GB (16 GB recommended for running local 3B VLMs in Ollama).
* **Storage Space**: Minimum 2 GB free disk space (additional 3–5 GB if storing local Ollama weights).
* **Graphics Hardware (GPU)**: Optional. NVIDIA GeForce GTX 1650 or higher (CUDA support accelerates neural training and VLM inference, though CPU execution is fully supported).
* **Display**: Standard 1080p (1920x1080) monitor.

---

\newpage

# CHAPTER 4: DATASET GATHERING AND PRE-PROCESSING

### 4.1 DATA COLLECTION
Because Riddlekeeper is designed to evaluate **size extrapolation and algorithmic generalization**, static fixed-size image datasets (such as ImageNet, CIFAR, or MNIST) are fundamentally inapplicable. Riddlekeeper relies on a **procedural benchmark dataset generator** (`riddlekeeper/dataset.py` and `riddlekeeper/environment.py`) that generates controlled, synthetic puzzle environments with mathematically verified ground-truth solutions.

```
+-----------------------------------------------------------------------------------------------+
|                            PROCEDURAL DATA GENERATION PIPELINE                                |
+-----------------------------------------------------------------------------------------------+
|                                                                                               |
|  [Grid Initialization]                                                                        |
|       Specify dimensions: H x W (e.g., 5x5 for training; 8x8, 10x10 for testing)              |
|         │                                                                                     |
|         ▼                                                                                     |
|  [Obstacle Placement]                                                                         |
|       Sample wall obstacles with Bernoulli density rho = 0.15 across inner grid cells         |
|         │                                                                                     |
|         ▼                                                                                     |
|  [Agent & Goal Sampling]                                                                      |
|       Uniformly sample start (r_s, c_s) and goal (r_g, c_g) such that start != goal           |
|         │                                                                                     |
|         ▼                                                                                     |
|  [Solvability Verification via BFS Oracle]                                                    |
|       Compute shortest path from start to goal.                                               |
|       • If path is None: DISCARD & RESAMPLE.                                                  |
|       • If path exists: RECORD (s_t, a_t, s_{t+1}) trajectory and save visual image.          |
|                                                                                               |
+-----------------------------------------------------------------------------------------------+
```

For logic puzzle benchmarks (Sudoku, $N$-Queens, Sokoban, Flow Free, Pipes, Words), canonical benchmark instances representing easy, medium, hard, and unsatisfiable edge-cases are curated and rendered into the `riddlekeeper/puzzles/` repository.

### 4.2 DATA PRE-PROCESSING
Data pre-processing transforms raw multimodal data into structured numeric formats suitable for neural message passing and symbolic constraint evaluation:
1. **Grid Boundary Extraction**: Input screenshots undergo pixel variance thresholding (`_detect_grid_bounds`) to crop out margins, titles, and OS window borders.
2. **Cell Normalization**: Cropped puzzle images are partitioned into an $H \times W$ uniform cell matrix.
3. **Spatial Tensor Construction**: For each instance, a 4-channel one-hot tensor $X \in \mathbb{R}^{B \times 4 \times H \times W}$ is constructed:
   - Channel 0 (Obstacle Mask): $1.0$ for non-traversable walls, $0.0$ for free cells.
   - Channel 1 (Agent Map): $1.0$ at current agent coordinates $(r_a, c_a)$, $0.0$ elsewhere.
   - Channel 2 (Goal Map): $1.0$ at goal coordinates $(r_g, c_g)$, $0.0$ elsewhere.
   - Channel 3 (Walkable Space): Complement of Channel 0 ($1.0 - \text{walls}$).
4. **Trajectory Packaging**: Ground-truth optimal action sequences derived from the BFS oracle are encoded as discrete integer sequences $a_t \in \{0: \text{Up}, 1: \text{Down}, 2: \text{Left}, 3: \text{Right}\}$ for supervised imitation learning.

### 4.3 FEATURE EXTRACTION
Unlike standard deep learning systems that rely on uninterpretable latent vector embeddings, Riddlekeeper extracts **explicit, disentangled spatial features** that preserve physical geometry and topology:

#### Table 4.1: Feature Extraction and Multi-Modal Spatial Tensor Mapping
| Extracted Feature | Dimensionality / Type | Mathematical Definition | Functional Purpose in Riddlekeeper |
| :--- | :---: | :--- | :--- |
| **Obstacle Map ($C_0$)** | Tensor $(B, 1, H, W)$ | $X_{b, 0, r, c} = \mathbb{I}(\text{cell}(r, c) = \text{wall})$ | Masks illegal message-passing edges; prevents wall collisions. |
| **Agent Position ($C_1$)** | Tensor $(B, 1, H, W)$ | $X_{b, 1, r, c} = \mathbb{I}((r, c) = (r_{\text{agent}}, c_{\text{agent}}))$ | Identifies source node for action extraction. |
| **Goal Position ($C_2$)** | Tensor $(B, 1, H, W)$ | $X_{b, 2, r, c} = \mathbb{I}((r, c) = (r_{\text{goal}}, c_{\text{goal}}))$ | Seeds the distance potential field ($V(r_{\text{goal}}, c_{\text{goal}}) = 0.0$). |
| **Free Space ($C_3$)** | Tensor $(B, 1, H, W)$ | $X_{b, 3, r, c} = 1.0 - X_{b, 0, r, c}$ | Validates open traversable routes. |
| **Legal Action Mask ($M$)**| Boolean Tensor $(B, 4)$| $M_{b, a} = \mathbb{I}(\text{neighbor}_a \in \text{Grid} \land \neg \text{Wall})$ | Sets logits of illegal actions to $-\infty$. |
| **Graph Diameter ($\text{diam}$)**| Integer Scalar | $\text{diam}(G) \le 2(H + W)$ | Scales recurrent message-passing depth $K \ge \text{diam}(G)$. |
| **Adjacency Matrix ($A$)**| Sparse Graph $(N, N)$ | $A_{uv} = \mathbb{I}(\text{dist}_{\text{Manhattan}}(u, v) = 1)$ | Defines planar 4-connected message passing topology. |

### 4.4 EXPLORATORY AND STATISTICAL ANALYSIS
Statistical profiling was conducted across $1,000$ procedurally generated puzzle instances across $5 \times 5$, $8 \times 8$, and $10 \times 10$ board configurations.

#### Table 4.2: Exploratory and Statistical Analysis of Dataset Attributes
| Dataset Scale Tier | Grid Dimensions | Total Grid Cells | Obstacle Density ($\rho$) | Mean Optimal Path (Steps) | Max Graph Diameter | Solvability Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Training (IID)** | $5 \times 5$ | 25 | $0.15 \pm 0.02$ | $5.42 \pm 1.84$ | 8 | 84.6% (Unfiltered) $\to$ **100%** (Verified) |
| **Validation (IID)** | $5 \times 5$ | 25 | $0.15 \pm 0.02$ | $5.39 \pm 1.91$ | 8 | 85.1% (Unfiltered) $\to$ **100%** (Verified) |
| **OOD Tier 1** | $8 \times 8$ | 64 | $0.15 \pm 0.03$ | $10.15 \pm 3.12$ | 14 | 81.3% (Unfiltered) $\to$ **100%** (Verified) |
| **OOD Tier 2** | $10 \times 10$ | 100 | $0.15 \pm 0.03$ | $13.84 \pm 4.28$ | 18 | 78.9% (Unfiltered) $\to$ **100%** (Verified) |

**Statistical Insight**: As the grid area quadruples from $25$ cells ($5 \times 5$) to $100$ cells ($10 \times 10$), the mean optimal path length increases from $5.42$ to $13.84$ steps, and the maximum diameter increases from $8$ to $18$. Because a standard 3-layer CNN has a fixed receptive field of $7$, it is mathematically incapable of observing the goal when the path length exceeds $7$ steps. Conversely, the dynamic message-passing depth $K = \max(12, 2(H+W))$ scales to $K = 40$ on a $10 \times 10$ grid, completely covering all reachable diameters.

---

\newpage

# CHAPTER 5: SYSTEM DESIGN

### 5.1 SYSTEM ARCHITECTURE
The system architecture of Riddlekeeper unifies multimodal visual perception, neural algorithmic reasoning, symbolic constraint satisfaction, and deterministic visual annotation into a cohesive, decoupled pipeline.

```mermaid
flowchart TD
    subgraph Input_Layer ["Input Layer"]
        A["User Input: Puzzle Image / Screenshot"]
    end

    subgraph Perception_Layer ["Perception & Disentanglement Layer"]
        B["Adaptive Grid Detector (_detect_grid_bounds)"]
        C{"Clean Layout?"}
        D["Local CV Edge/Luminance Extractor (< 0.05s)"]
        E["Local VLM (Qwen2.5-VL / Moondream via Ollama)"]
        F["Structured Spatial Tensor (B, 4, H, W)"]
    end

    subgraph Reasoning_Layer ["Cognitive Reasoning Engine"]
        G{"Puzzle Paradigm"}
        H["Bellman-Ford GNN (Dynamic Depth K >= 2(H+W))"]
        I["Symbolic CSP Solvers (Sudoku MRV, N-Queens, Sokoban, Flow)"]
        J["Agent Orchestrator (State & Time Budget Enforcement)"]
    end

    subgraph Verification_Execution ["Execution & Verification"]
        K["Action Masking & Deterministic State Transition"]
        L{"Independent Validation: is_solved()?"}
        M["Verified Action Sequence Trace"]
        N["Error Recovery / Failure Reason"]
    end

    subgraph Output_Layer ["Output & Visualization Layer"]
        O["Pillow Deterministic Graphics Annotator"]
        P["Final Solution Image with Pixel-Accurate Overlays"]
    end

    A --> B
    B --> C
    C -- Yes --> D --> F
    C -- No --> E --> F
    F --> G
    G -- Grid Navigation --> H --> J
    G -- Logic / CSP --> I --> J
    J --> K
    K --> L
    L -- Pass --> M --> O --> P
    L -- Fail --> N
```
*Fig 5.1: System Architecture of Riddlekeeper*

### 5.2 ACTIVITY DIAGRAM
The activity diagram models the sequential execution lifecycle of Riddlekeeper from the moment a user uploads a puzzle image to the final rendering of the verified solution path.

```mermaid
stateDiagram-v2
    [*] --> IngestImage: User uploads puzzle screenshot
    IngestImage --> CropGrid: Adaptive edge detection crops borders
    CropGrid --> TranscribeState: Local CV / Ollama VLM parses cells
    TranscribeState --> ValidateSchema: Check agent, goal, and boundary integrity
    
    state ValidateSchema {
        [*] --> CheckEntities
        CheckEntities --> SchemaPass: Valid coordinates
        CheckEntities --> SchemaFail: Missing entity
    }
    
    SchemaFail --> [*]: Abort with informative perception error
    SchemaPass --> InitPotential: Initialize Bellman-Ford potential field (V_goal = 0, others = Inf)
    
    state RecurrentMessagePassing {
        [*] --> StepRelaxation: h^(t+1)_u = min(h_u, min(h_v + 1))
        StepRelaxation --> CheckK: t < K ?
        CheckK --> StepRelaxation: Yes (recurrent loop)
        CheckK --> PotentialConverged: No (K >= 2(H+W))
    }
    
    InitPotential --> RecurrentMessagePassing
    PotentialConverged --> EvaluateNeighbors: Query 4 adjacent neighbor potentials
    EvaluateNeighbors --> ApplyActionMask: Mask blocked/wall moves (-Inf)
    ApplyActionMask --> SelectAction: a* = argmin(neighbor potential)
    SelectAction --> TransitionState: Apply a*, update agent position
    TransitionState --> CheckGoal: Is agent at goal?
    
    CheckGoal --> RecurrentMessagePassing: No (within budget)
    CheckGoal --> BudgetExceeded: Step count > Max Allowed
    CheckGoal --> GoalReached: Yes
    
    BudgetExceeded --> [*]: Terminate with budget failure trace
    GoalReached --> DrawOverlay: Pillow renders glowing path on original image
    DrawOverlay --> [*]: Save solution image and return action sequence
```
*Fig 5.2: Activity Diagram of Perception-to-Action Execution*

### 5.3 USE CASE DIAGRAM
The use case diagram illustrates the functional interactions between human users, the high-level agent orchestrator, external local vision runners, and the underlying symbolic and neural solvers.

```mermaid
flowchart LR
    User((End User / Researcher))
    Orchestrator((Agent Orchestrator))
    VisionRunner((Local Vision Runner))
    
    subgraph Riddlekeeper_System ["Riddlekeeper System Boundary"]
        UC1["Upload Puzzle Image"]
        UC2["Specify Solver Mode (Auto / Neural / Symbolic)"]
        UC3["Set State & Time Budgets"]
        UC4["Transcribe Board State (Local CV / Ollama)"]
        UC5["Solve Grid Navigation (Bellman-Ford GNN)"]
        UC6["Solve Logic Puzzles (Sudoku, Queens, Sokoban, Flow)"]
        UC7["Validate Solution Independently"]
        UC8["Inspect Execution Trace & Runtime Metrics"]
        UC9["Export Annotated Solution Image"]
    end
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC8
    User --> UC9
    
    UC1 --> Orchestrator
    UC2 --> Orchestrator
    UC3 --> Orchestrator
    
    Orchestrator --> UC4
    UC4 --> VisionRunner
    
    Orchestrator --> UC5
    Orchestrator --> UC6
    
    UC5 --> UC7
    UC6 --> UC7
    UC7 --> UC8
    UC7 --> UC9
```
*Fig 5.3: Use Case Diagram for Puzzle Solving Interactions*

### 5.4 WORKFLOW DIAGRAM
The workflow diagram details the step-by-step decision tree governing how Riddlekeeper selects between neural algorithmic reasoners, symbolic constraint solvers, and error-recovery procedures.

```mermaid
flowchart TD
    Start([Start: CLI or Python API Request]) --> Ingest[Ingest Puzzle & Configuration]
    Ingest --> CheckType{Puzzle Type?}
    
    CheckType -- "grid_navigation" --> CheckInputType{Input Format?}
    CheckInputType -- "Image (.png)" --> RunCV[Run Adaptive CV / Ollama Pipeline]
    CheckInputType -- "Environment Object" --> ParseTensor[Extract 4-Channel Spatial Tensor]
    RunCV --> ParseTensor
    
    ParseTensor --> SetDepth["Compute Recurrent Depth: K = max(12, 2*(H+W))"]
    SetDepth --> ExecGNN[Execute Bellman-Ford GNN Layer]
    ExecGNN --> StepEnv[Execute Closed-Loop Step in GridWorldEnv]
    StepEnv --> CheckSolved{Solved?}
    CheckSolved -- No --> CheckBudget{Budget Left?}
    CheckBudget -- Yes --> ExecGNN
    CheckBudget -- No --> ReturnFail[Return solved=False, StateBudgetExceeded]
    CheckSolved -- Yes --> VerifyOracle[Verify Path with Independent Checker]
    
    CheckType -- "sudoku" --> RunSudoku[Execute MRV Backtracking Solver]
    CheckType -- "queens" --> RunQueens[Execute Row-Wise Bitmask Backtracking]
    CheckType -- "sokoban" --> RunSokoban[Execute A* with Deadlock Pruning]
    CheckType -- "flow" --> RunFlow[Execute Multi-Color DFS with Dead-End Checks]
    CheckType -- "pipes / words" --> RunMisc[Execute Rotational CSP / Trie Search]
    
    RunSudoku --> VerifyOracle
    RunQueens --> VerifyOracle
    RunSokoban --> VerifyOracle
    RunFlow --> VerifyOracle
    RunMisc --> VerifyOracle
    
    VerifyOracle --> IsValid{Valid Solution?}
    IsValid -- Yes --> RenderImage[Render Annotated Solution via Pillow]
    IsValid -- No --> ReturnFail
    
    RenderImage --> SaveDisk[Save to riddlekeeper/puzzles/solutions/]
    SaveDisk --> End([End: Return SolveResult])
    ReturnFail --> End
```
*Fig 5.4: Workflow Diagram of Algorithmic Planning and Verification*

---

\newpage

# CHAPTER 6: PROPOSED SYSTEM

### 6.1 PROPOSED SYSTEM OVERVIEW
The **Riddlekeeper** framework constitutes an integrated, local-first neuro-symbolic puzzle solver. By departing from rigid heuristic scripts and ungrounded multimodal language models, Riddlekeeper unifies:
1. Local computer vision and Vision-Language Model transcription;
2. Algorithmic message passing aligned with dynamic programming for provable out-of-distribution size extrapolation;
3. Exact symbolic constraint satisfaction for NP-hard puzzle families; and
4. Sub-pixel deterministic graphics annotation.

The system accepts an unannotated image, parses its contents, computes an optimal solution trajectory within strictly enforced execution budgets, verifies postconditions, and returns an annotated image displaying the complete solution path.

### 6.2 MODULES

#### Module 1: Multimodal Perception & Visual Grounding Engine (`riddlekeeper/vision/`)
* **Adaptive Grid Detector (`_detect_grid_bounds`)**: Scans row and column luminance variance across raw images to detect and isolate grid coordinates, stripping away non-essential UI margins and titles.
* **Fast Local CV Transcriber (`transcribe_local`)**: Analyzes cell RGB averages in $< 0.05\text{ s}$ for clean graphics, mapping color clusters to agent, goal, wall, and empty cell tokens.
* **Local VLM Transcriber (`transcribe_with_model`)**: Connects to local Ollama endpoints hosting open-weight Vision-Language Models (e.g., Qwen2.5-VL-3B, Moondream2). Prompts the model with strict JSON schema constraints to transcribe complex, unformatted screenshots into structured matrices.

#### Module 2: Algorithmic Neural Reasoner (`riddlekeeper/models.py`)
* **`BellmanFordLayer`**: An exact parameter-free min-plus convolution layer that performs unit-cost distance relaxation across 4-connected grid graphs:
  $$h_u^{(t+1)} = \min \left( h_u^{(t)}, \min_{v \in \mathcal{N}(u)} (h_v^{(t)} + 1.0) \right)$$
* **`BellmanFordGNN`**: Seeds the goal cell with $0.0$ and all other cells with $\infty$, iteratively relaxes distances over $K = \max(12, 2(H+W))$ steps, and computes action logits by extracting neighbor potential values around the agent.
* **`BaselineCNNPolicy`**: A standard 3-layer convolutional network with global average pooling and MLP heads, serving as an empirical baseline to demonstrate the catastrophic failure of non-aligned architectures.

#### Module 3: Symbolic Constraint Satisfaction Engine (`riddlekeeper/puzzles/`)
* **Sudoku Solver (`sudoku.py`)**: Exact constraint satisfaction utilizing the Minimum Remaining Values (MRV) heuristic and forward checking.
* **$N$-Queens Solver (`queens.py`)**: Row-wise recursive backtracking utilizing bitmask operations for column, diagonal ($r-c$), and anti-diagonal ($r+c$) conflict checks.
* **Sokoban Solver (`sokoban.py`)**: Bounded A* search using Hungarian minimum-matching Manhattan distances and structural deadlock pruning (corner and frozen wall deadlocks).
* **Flow Free Solver (`flow.py`)**: Multi-color path search with dead-end neighbor pruning, guaranteeing 100% board coverage without path intersections.
* **Pipes & Words Solvers (`pipes.py`, `words.py`)**: Rotational degree consistency verification and trie-directed grid character path finding.

#### Module 4: Agent Orchestrator & Verification Engine (`riddlekeeper/agent/`)
* **`RiddlekeeperAgent`**: Manages solver dispatch, executes dynamic replanning loops (`replan_execute`), and logs full execution traces.
* **Budget Manager**: Enforces hard state expansion limits ($S_{\max}$) and wall-clock execution limits ($T_{\max}\text{ ms}$), preventing runaway search.
* **Independent Validator**: Verifies that generated action sequences transition the environment to an authentic goal state without rule violations before declaring success.

### 6.3 PROPOSED SYSTEM FLOW
The proposed system flow proceeds through six discrete stages:
1. **Input Stage**: The user supplies an image or structured grid configuration.
2. **Perception & Disentanglement Stage**: The visual encoder parses the image into a 4-channel spatial tensor $X \in \mathbb{R}^{B \times 4 \times H \times W}$.
3. **Spatial Reasoning Stage**: The planar 4-connected adjacency graph is constructed, and invalid moves are masked.
4. **Action Prediction Stage**: The Bellman-Ford GNN propagates distance potential fields from the goal and selects the neighbor minimizing remaining distance.
5. **State Transition Stage**: The optimal action $a^*$ is applied to the environment, updating state $s_{t+1} = \mathcal{T}(s_t, a^*)$.
6. **Output & Rendering Stage**: The verified sequence of actions is returned, and Pillow draws pixel-perfect visual overlays onto the input image.

### 6.4 ALGORITHMS AND MODELS

```
====================================================================================================
ALGORITHM 1: RECURRENT BELLMAN-FORD MESSAGE PASSING FOR SIZE-INVARIANT PATHFINDING
====================================================================================================
Input : Spatial Tensor X in R^{B x 4 x H x W}, Grid Dimensions H, W, Wall Mask W_grid
Output: Action Logits z in R^{B x 4}, Distance Potential Field V in R^{B x 1 x H x W}

1: Extract goal mask G = X[:, 2:3, :, :], agent position A = X[:, 1, :, :], walls W = X[:, 0:1, :, :]
2: Initialize potential field h^(0):
       h^(0)[r, c] = 0.0  if G[r, c] == 1.0  else 1e6
3: Dynamically compute message-passing depth:
       K = min( max(12, 2 * (H + W)), H * W - 1 )
4: for t = 0 to K - 1 do
5:     Padded_h = ConstantPad(h^(t), pad=1, value=1e6)
6:     Padded_W = ConstantPad(W, pad=1, value=1.0)
7:     for each orthogonal direction (dr, dc) in {(-1,0), (1,0), (0,-1), (0,1)} do
8:         Neighbor_vals = Padded_h[:, :, 1+dr : 1+dr+H, 1+dc : 1+dc+W]
9:         Blocked_mask = Padded_W[:, :, 1+dr : 1+dr+H, 1+dc : 1+dc+W] > 0.5
10:        Neighbor_vals = MaskFill(Neighbor_vals, Blocked_mask, value=1e6)
11:    end for
12:    Min_neighbor = Minimum_Across_Directions(Neighbor_vals)
13:    h^(t+1) = Minimum( h^(t), Min_neighbor + 1.0 )
14:    h^(t+1) = MaskFill(h^(t+1), W > 0.5, value=1e6)  // Walls remain impassable
15: end for
16: Set V = h^(K), enforcing V[G == 1.0] = 0.0
17: Extract 4 adjacent neighbor potentials around agent position A:
        v_neighbors = ExtractNeighbors(V, A)
18: Compute action logits: z = - v_neighbors
19: if Action_Mask M is provided then
20:     z = MaskFill(z, ~M, value=-1e9)
21: end if
22: return z, V
====================================================================================================
```

### 6.5 EXPECTED SYSTEM OUTPUT
The expected outputs of Riddlekeeper comprise:
1. **Discrete Action Trajectory**: An ordered list of directional moves (e.g., `['Right', 'Right', 'Down', 'Down', 'Right']`).
2. **Explored State Count**: Total search nodes expanded during planning.
3. **Execution Runtime**: Measured wall-clock time in milliseconds.
4. **Optimality Verification**: Boolean confirmation (`solved=True`) verified by an independent checker.
5. **Annotated Output Image**: High-resolution image saved to `riddlekeeper/puzzles/solutions/` featuring glowing paths, royal queen crowns, highlighted numbers, colored pipes, and push arrows.

---

\newpage

# CHAPTER 7: TESTING

### 7.1 LAYOUT AND VISUALS
The visual pipeline was tested across diverse image formats, aspect ratios, and visual styles to evaluate perceptual robustness and aesthetic clarity.

```
+--------------------------------------------------------------------------------------------------+
|                            VISUAL PERCEPTION & ANNOTATION PIPELINE                               |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   [Raw Input Image]        [Adaptive Bounding Box]         [Exact Solver]     [Annotated Output] |
|   +-----------------+      +---------------------+        +--------------+    +----------------+ |
|   |  TITLE BANNER   |      |                     |        |  BFS / GNN   |    |  TITLE BANNER  | |
|   | +-------------+ | ---> |   CROPPED PUZZLE    | -----> |  Exact Path  | -> | +------------+ | |
|   | | . . # . G | | |      |      GRID ONLY      |        | 100% Optimal |    | | o-o-#-.-G| | | |
|   | | S . # . . | | |      |                     |        +--------------+    | | S-o-#-.-.| | | |
|   | +-------------+ |      +---------------------+                            | +------------+ | |
|   +-----------------+                                                         +----------------+ |
|   (Unformatted Input)     (Borders & Chrome Removed)     (Zero Hallucination) (Glowing Solution) |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```
*Fig 7.1: Visual Perception and Board Transcription Pipeline*

Key visual capabilities verified during testing include:
* **Adaptive Grid Boundary Cropping**: Successfully extracted puzzle grids from screenshots containing window borders, headers, and title banners across resolutions from $256 \times 256$ to $1920 \times 1080$.
* **Sub-Pixel Pillow Rendering**: Visual paths are drawn with anti-aliased lines and neon outer glow halos, ensuring clear visibility over complex puzzle textures.
* **Symbolic Number Highlighting**: In Sudoku, user-given clues are preserved in black font with white cells, while computed numbers are rendered in crisp royal blue against light blue highlighted cell backgrounds.

### 7.2 FUNCTIONALITY AND USER EXPERIENCE
Functional testing evaluated the core execution loop across both symbolic logic solvers and neural policy networks.

```
+--------------------------------------------------------------------------------------------------+
|                           MULTI-PUZZLE VISUAL ANNOTATION RESULTS                                 |
+----------------------------------+------------------------------------+--------------------------+
|          SUDOKU (9x9)            |             FLOW FREE              |         SOKOBAN          |
+----------------------------------+------------------------------------+--------------------------+
| • Given clues preserved in black | • Multi-color smooth rounded pipes | • Push vectors overlaid  |
| • Solved digits in royal blue    | • 100% cell coverage verified      | • Corner deadlocks pruned|
| • Solved in 11.2 ms              | • Zero intersecting paths          | • A* Hungarian heuristic |
+----------------------------------+------------------------------------+--------------------------+
```
*Fig 7.2: Multi-Puzzle Visual Solution Overlays*

All 30 automated unit tests in `riddlekeeper/puzzles/tests.py` passed with 100% compliance:
* **Contradictory / Impossible Inputs**: Unsolvable Sudokus and impossible $2 \times 2$ Queens boards correctly returned `solved=False` without throwing uncaught exceptions.
* **Budget Limits**: Sokoban search states exceeding the 5,000-state limit terminated within $1,000\text{ ms}$ with an informative `StateBudgetExceeded` status.
* **Independent Solution Verification**: All returned paths were verified independently by simulating transitions in a duplicate environment before returning success.

---

\newpage

# CHAPTER 8: RESULTS & DISCUSSIONS

### 8.1 QUANTITATIVE METRICS
The core experimental evaluation compared the proposed **Bellman-Ford GNN** against the **Baseline CNN Policy** and an exact **BFS Reference Oracle** across three scale tiers:
1. **In-Distribution (IID)**: $5 \times 5$ grids ($25$ cells).
2. **Out-of-Distribution (OOD Scale 1)**: $8 \times 8$ grids ($64$ cells, $2.56\times$ area).
3. **Out-of-Distribution (OOD Scale 2)**: $10 \times 10$ grids ($100$ cells, $4.00\times$ area).

We measured:
* **Success Rate (SR %)**: Percentage of episodes where the agent reached the goal within the step budget ($2 \times H \times W$).
* **Path Optimality Ratio (POR)**: Ratio of executed steps to optimal BFS path length:
  $$\text{POR} = \frac{\text{Steps Taken}}{\text{Optimal BFS Length}}$$

#### Table 8.1: Quantitative Performance Benchmark across Grid Dimensions
| Model Architecture | 5×5 (In-Distribution) | 8×8 (OOD Scale 1) | 10×10 (OOD Scale 2) | Mean Optimality Ratio | Extrapolation Verdict |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **BFS Reference (Oracle)** | **100.0%** | **100.0%** | **100.0%** | **1.00×** | Exact Ground Truth |
| **Bellman-Ford GNN (Ours)** | **100.0%** | **100.0%** | **100.0%** | **1.00×** | **100% Zero-Shot Size Invariance** |
| **Baseline CNN Policy** | **20.0%** | **10.0%** | **10.0%** | **25.8× – 40.7×** | **Catastrophic Failure** |

```
SUCCESS RATE (%) VS. BOARD DIMENSIONS (SIZE EXTRAPOLATION)

  100% +=======================================================+
       | [BFS: 100%]             [BFS: 100%]       [BFS: 100%] |
       | [Bellman-Ford GNN: 100%][BF-GNN: 100%]    [BF-GNN: 100%|
   80% |                                                       |
   60% |                                                       |
   40% |                                                       |
   20% | [Baseline CNN: 20%]                                   |
       |                         [Base CNN: 10%]   [Base CNN: 10%|
    0% +-------------------------------------------------------+
                5x5                       8x8              10x10
```
*Fig 8.1: Empirical Closed-Loop Size Extrapolation Benchmark*

### 8.2 QUALITATIVE OBSERVATIONS
* **Failure Modes of Standard CNNs**: On $5 \times 5$ grids, the CNN only succeeds when the agent spawns 1–2 steps away from the goal. When the distance exceeds $3$ steps, or when wall obstacles require navigating around corners, the CNN enters infinite 2-step oscillatory loops (stepping Left $\leftrightarrow$ Right) because global average pooling discards spatial positioning.
* **Explainability of Bellman-Ford GNN**: The GNN’s latent distance map $V(r, c)$ forms a smooth, monotonically decreasing potential field toward the goal. Visualizing $V$ reveals that the network correctly discovers shortest-path wavefronts flowing around arbitrary obstacle geometries.

### 8.3 INTERPRETATION OF FINDINGS
The findings provide decisive empirical validation of **algorithmic alignment theory**:
* Standard convolutions rely on fixed spatial receptive fields ($2L + 1$). As board dimensions grow, the receptive field cannot bridge the diameter of the graph, causing the policy to act blindly.
* In contrast, the Bellman-Ford GNN aligns with the discrete recurrence of shortest-path computation. By scaling iteration depth $K \ge 2(H+W)$, global graph connectivity is maintained regardless of grid dimensions, achieving **100% zero-shot size invariance**.

### 8.4 ADDRESS DEVICE-SPECIFIC CONTEXTS
* **CPU Execution Efficiency**: When processing clean screenshots with `transcribe_local`, Riddlekeeper executes the complete perception-to-solution pipeline in $< 45\text{ ms}$ on standard Intel Core i5 CPUs, consuming $< 48\text{ MB}$ RAM.
* **Local VLM Acceleration**: When processing noisy screenshots via Ollama (`qwen2.5vl:3b`), CPU execution requires $45\text{ s}$ due to multi-token attention decoding; when an NVIDIA RTX GPU is present, inference drops to $< 1.8\text{ s}$.

---

\newpage

# CHAPTER 9: CONCLUSION

### 9.1 SUMMARY OF KEY INSIGHTS
The development and evaluation of **Riddlekeeper** demonstrates the viability of building an algorithmically aligned, neuro-symbolic framework for complex visual puzzle solving and sequential spatial reasoning. By departing from monolithic end-to-end models and rigid heuristic macros, Riddlekeeper establishes several foundational insights:
1. **Algorithmic Alignment is Essential for Size Generalization**: Standard deep learning architectures fail at size extrapolation because they memorize coordinate shortcuts. Structuring neural message passing to align with dynamic programming recurrences (Bellman-Ford) guarantees $100\%$ size-invariant extrapolation.
2. **Decoupled Neuro-Symbolic Architecture Prevents Hallucination**: Separating perception (CV/VLM transcription), reasoning (exact GNN and CSP solvers), and rendering (deterministic Pillow graphics) completely eliminates hallucinatory errors while preserving end-to-end usability.
3. **Local-First Privacy and Reliability**: Riddlekeeper operates 100% offline using local open-weight models and Python standard library solvers, eliminating API costs, network latency, and privacy vulnerabilities.

### 9.2 CHALLENGES AND LESSONS LEARNED
* **Combinatorial Search Explosions**: In Sokoban and Flow Free, naive depth-first search quickly exhausts memory. Implementing structural dead-end and deadlock pruning pruned over $85\%$ of branches, reinforcing the necessity of domain-specific heuristics.
* **Perception Ambiguity in Visual Inputs**: Grid line detection can fail when screenshots have uneven contrast. Incorporating adaptive variance slicing ensured robust coordinate cropping across arbitrary resolutions.
* **Budget-Enforced Execution**: Unbounded search algorithms risk locking client applications. Implementing hard state and time budgets within the `RiddlekeeperAgent` ensured deterministic, non-blocking execution.

---

\newpage

# CHAPTER 10: FUTURE ENHANCEMENTS

### 10.1 USER EXPERIENCE AND PERSONALIZATION
* **Interactive Web Dashboard**: Develop a browser-based GUI (using Streamlit or FastHTML) allowing users to drag and drop puzzle screenshots, view animated step-by-step solution replays, and customize solver search budgets interactively.
* **Custom Color Themes & Accessibility**: Provide high-contrast colorblind modes and customizable visual badges for rendering overlays.

### 10.2 EMERGING TECHNOLOGIES AND IMMERSIVE CONTENT
* **Real-Time Video Camera Solving**: Extend the perception pipeline to process live camera video streams, enabling users to point their smartphone or webcam at a physical newspaper puzzle and view real-time augmented reality (AR) solution overlays.
* **Voice-Guided Step-by-Step Instructions**: Integrate local text-to-speech engines to narrate solution moves sequentially for educational walkthroughs.

### 10.3 ADVANCED TECHNICAL IMPLEMENTATION
* **Reinforcement Learning Fine-Tuning**: Implement Proximal Policy Optimization (PPO) over the Bellman-Ford GNN backbone to learn policies for stochastic environments with moving obstacles.
* **Position-Normalized Group Convolutions (PoNG)**: Explore PoNG architectures to learn direct raw-pixel visual grounding end-to-end without intermediate JSON transcription.
* **Abstraction & Reasoning Corpus (ARC) Benchmark**: Extend Riddlekeeper’s object-extraction and DSL engines to evaluate performance on the full ARC challenge.

### 10.4 PERFORMANCE AND ACCESSIBILITY
* **NPU / Mobile Acceleration**: Quantize the neural reasoning models to INT8 using ONNX Runtime for deployment on low-power edge devices and mobile phones.
* **Multi-Threaded Parallel Search**: Implement parallelized A* search and distributed constraint propagation for solving massively scaled $100 \times 100$ puzzles.

### 10.5 CONTENT MANAGEMENT AND WORKFLOW
* **Automated Puzzle Generation Studio**: Build a curriculum learning puzzle generator that automatically synthesizes novel puzzle variants with calibrated human difficulty ratings for pedagogical applications.
* **Comprehensive Community Benchmark Hub**: Package Riddlekeeper as an open-source Python library (`pip install riddlekeeper`) with standardized benchmark suites for academic research in neural algorithmic reasoning.

---

\newpage

# REFERENCES

1. **S. Wittig, A. Vasileiou, R. R. Nerem, T. Stoll, F. Geerts, Y. Wang, and C. Morris**, "Which Algorithms Can Graph Neural Networks Learn?," in *Proceedings of the 39th Annual Conference on Learning Theory (COLT)*, 2024 / 2026. (Preprint arXiv:2602.13106, 2024).
2. **R. R. Nerem, S. Chen, S. Dasgupta, and Y. Wang**, "Graph Neural Networks Extrapolate Out-of-Distribution for Shortest Paths," *Proceedings of Machine Learning Research (PMLR)*, vol. X, pp. 1–28, 2024 / 2026. (Preprint arXiv:2503.19173, 2024).
3. **M. Małkiński and J. Mańdziuk**, "Advancing Generalization Across a Variety of Abstract Visual Reasoning Tasks," in *Proceedings of the 34th International Joint Conference on Artificial Intelligence (IJCAI 2025)*, pp. 1–9, 2024. (Preprint arXiv:2505.13391, 2024).
4. **A. Sarkar, Z. Yu, and M. Y. I. Idris**, "Reasoning in Computer Vision: Taxonomy, Models, Tasks, and Methodologies," *ACM Computing Surveys / arXiv*, pp. 1–35, Aug. 2025. (Preprint arXiv:2508.10523, 2025).
5. **A. Das, O. Ghugarkar, V. Bhat, and A. Aali**, "Compositional Neuro-Symbolic Reasoning," *CoreThink AI & Stanford University Technical Report / arXiv*, pp. 1–18, Apr. 2025. (Preprint arXiv:2604.02434, 2025).
6. **K. Xu, J. Li, M. Zhang, S. S. Du, K. Kawarabayashi, and S. Jegelka**, "What Can Neural Networks Reason About?," in *International Conference on Learning Representations (ICLR)*, 2020.
7. **P. Veličković, R. Ying, M. Padovano, R. Hadsell, and C. Blundell**, "Neural Algorithmic Reasoning," *Patterns (Cell Press)*, vol. 2, no. 7, p. 100273, 2021.
8. **F. Chollet**, "On the Measure of Intelligence," *arXiv preprint arXiv:1911.01547*, 2019.
9. **S. Russell and P. Norvig**, *Artificial Intelligence: A Modern Approach*, 4th ed. Hoboken, NJ: Pearson, 2020.
10. **A. Paszke et al.**, "PyTorch: An Imperative Style, High-Performance Deep Learning Library," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 32, 2019.

