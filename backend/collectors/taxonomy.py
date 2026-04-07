"""Applied AI Research Frontier taxonomy — shared by all collectors.

This module defines the search queries, relevance keywords, and classification
logic that ensures we collect APPLIED AI research (how AI is deployed in
production and specific industries), not foundation model announcements.
"""

# ---------------------------------------------------------------------------
# Search queries – grouped by frontier area
# Each tuple: (query_string, frontier_area_tag)
# ---------------------------------------------------------------------------

ARXIV_QUERIES: list[tuple[str, str]] = [
    # 1. Self-improving / continual learning agents
    ("cat:cs.AI AND abs:continual AND abs:agent", "continual_learning_agents"),
    ("cat:cs.AI AND abs:self-improving AND abs:agent", "continual_learning_agents"),
    ("cat:cs.LG AND abs:lifelong AND abs:learning AND abs:agent", "continual_learning_agents"),
    ("cat:cs.AI AND abs:prompt AND abs:optimization AND abs:agent", "continual_learning_agents"),
    # 2. RL in production
    ("cat:cs.AI AND abs:reinforcement AND abs:scheduling", "rl_production"),
    ("cat:cs.AI AND abs:reinforcement AND abs:inventory", "rl_production"),
    ("cat:cs.AI AND abs:reinforcement AND abs:pricing", "rl_production"),
    ("cat:cs.LG AND abs:reinforcement AND abs:manufacturing", "rl_production"),
    ("cat:cs.LG AND abs:reinforcement AND abs:supply AND abs:chain", "rl_production"),
    ("cat:cs.LG AND abs:offline AND abs:reinforcement AND abs:learning", "rl_production"),
    ("cat:cs.LG AND abs:safe AND abs:reinforcement AND abs:learning", "rl_production"),
    ("cat:cs.AI AND abs:reinforcement AND abs:recommendation", "rl_production"),
    # 3. Multi-agent orchestration
    ("cat:cs.AI AND abs:multi-agent AND abs:orchestration", "multi_agent"),
    ("cat:cs.AI AND abs:multi-agent AND abs:enterprise", "multi_agent"),
    ("cat:cs.MA AND abs:coordination AND abs:agent", "multi_agent"),
    # 4. LLM process automation
    ("cat:cs.AI AND abs:workflow AND abs:automation AND abs:LLM", "llm_automation"),
    ("cat:cs.CL AND abs:document AND abs:automation", "llm_automation"),
    ("cat:cs.AI AND abs:process AND abs:automation AND abs:agent", "llm_automation"),
    # 5. AI + operations research / optimization
    ("cat:cs.AI AND abs:combinatorial AND abs:optimization", "ai_operations_research"),
    ("cat:cs.AI AND abs:vehicle AND abs:routing", "ai_operations_research"),
    ("cat:cs.LG AND abs:neural AND abs:combinatorial", "ai_operations_research"),
    ("cat:cs.AI AND abs:scheduling AND abs:optimization", "ai_operations_research"),
    ("cat:math.OC AND abs:machine AND abs:learning", "ai_operations_research"),
    # 6. Human-AI collaboration
    ("cat:cs.HC AND abs:human AND abs:AI AND abs:collaboration", "human_ai_collaboration"),
    ("cat:cs.AI AND abs:human-in-the-loop", "human_ai_collaboration"),
    ("cat:cs.LG AND abs:active AND abs:learning AND abs:annotation", "human_ai_collaboration"),
    # 7. RAG in production
    ("cat:cs.CL AND abs:retrieval AND abs:augmented AND abs:generation", "rag_production"),
    ("cat:cs.IR AND abs:retrieval AND abs:augmented", "rag_production"),
    ("cat:cs.CL AND abs:RAG AND abs:evaluation", "rag_production"),
    # 8. AI reliability / guardrails
    ("cat:cs.AI AND abs:guardrails AND abs:LLM", "ai_reliability"),
    ("cat:cs.CL AND abs:hallucination AND abs:detection", "ai_reliability"),
    ("cat:cs.CR AND abs:prompt AND abs:injection", "ai_reliability"),
    ("cat:cs.AI AND abs:evaluation AND abs:agent AND abs:safety", "ai_reliability"),
    # 9. Domain-specific AI
    ("cat:cs.AI AND abs:clinical AND abs:decision", "domain_healthcare"),
    ("cat:cs.CL AND abs:medical AND abs:LLM", "domain_healthcare"),
    ("cat:cs.AI AND abs:drug AND abs:discovery", "domain_healthcare"),
    ("cat:cs.CL AND abs:legal AND abs:reasoning", "domain_legal"),
    ("cat:cs.AI AND abs:contract AND abs:analysis", "domain_legal"),
    ("cat:cs.AI AND abs:financial AND abs:fraud", "domain_finance"),
    ("cat:q-fin AND abs:machine AND abs:learning", "domain_finance"),
    ("cat:cs.AI AND abs:credit AND abs:scoring", "domain_finance"),
    # 10. Efficient inference
    ("cat:cs.LG AND abs:efficient AND abs:inference", "efficient_inference"),
    ("cat:cs.LG AND abs:quantization AND abs:LLM", "efficient_inference"),
    ("cat:cs.LG AND abs:speculative AND abs:decoding", "efficient_inference"),
    ("cat:cs.DC AND abs:model AND abs:serving", "efficient_inference"),
    # 11. AI for economics / mechanism design
    ("cat:cs.GT AND abs:mechanism AND abs:design AND abs:neural", "ai_economics"),
    ("cat:cs.GT AND abs:auction AND abs:learning", "ai_economics"),
    ("cat:econ.GN AND abs:machine AND abs:learning", "ai_economics"),
    ("cat:cs.AI AND abs:market AND abs:design", "ai_economics"),
    # 12. Causal inference + ML
    ("cat:stat.ML AND abs:causal AND abs:inference", "causal_ml"),
    ("cat:cs.LG AND abs:causal AND abs:discovery", "causal_ml"),
    ("cat:cs.LG AND abs:treatment AND abs:effect", "causal_ml"),
    ("cat:cs.AI AND abs:counterfactual AND abs:reasoning", "causal_ml"),
    # 13. Sim-to-real / digital twins
    ("cat:cs.RO AND abs:sim-to-real", "sim_to_real"),
    ("cat:cs.AI AND abs:digital AND abs:twin", "sim_to_real"),
    ("cat:cs.LG AND abs:synthetic AND abs:data AND abs:simulation", "sim_to_real"),
    # 14. Neurosymbolic AI
    ("cat:cs.AI AND abs:neurosymbolic", "neurosymbolic"),
    ("cat:cs.AI AND abs:neural AND abs:symbolic AND abs:reasoning", "neurosymbolic"),
    ("cat:cs.AI AND abs:knowledge AND abs:graph AND abs:reasoning", "neurosymbolic"),
    # 15. Compound AI systems
    ("cat:cs.AI AND abs:compound AND abs:AI", "compound_ai"),
    ("cat:cs.CL AND abs:pipeline AND abs:LLM AND abs:retrieval", "compound_ai"),
    ("cat:cs.AI AND abs:model AND abs:routing AND abs:cascade", "compound_ai"),
]

SEMANTIC_SCHOLAR_QUERIES: list[tuple[str, str]] = [
    # Self-improving agents
    ("self-improving AI agents continual learning", "continual_learning_agents"),
    ("LLM agent memory management persistent", "continual_learning_agents"),
    ("prompt optimization autonomous agents", "continual_learning_agents"),
    # RL in production
    ("reinforcement learning production scheduling manufacturing", "rl_production"),
    ("reinforcement learning supply chain optimization", "rl_production"),
    ("reinforcement learning dynamic pricing real-world", "rl_production"),
    ("offline reinforcement learning industrial applications", "rl_production"),
    ("safe reinforcement learning deployment", "rl_production"),
    ("reinforcement learning recommendation systems production", "rl_production"),
    # Multi-agent
    ("multi-agent orchestration enterprise workflow", "multi_agent"),
    ("LLM agent coordination task planning", "multi_agent"),
    # LLM automation
    ("LLM workflow automation enterprise", "llm_automation"),
    ("AI agent process automation document", "llm_automation"),
    ("robotic process automation large language model", "llm_automation"),
    # AI + OR
    ("neural combinatorial optimization routing", "ai_operations_research"),
    ("machine learning operations research scheduling", "ai_operations_research"),
    ("AI vehicle routing optimization", "ai_operations_research"),
    ("deep learning combinatorial optimization", "ai_operations_research"),
    # Human-AI
    ("human-AI collaboration decision making", "human_ai_collaboration"),
    ("human-in-the-loop machine learning production", "human_ai_collaboration"),
    ("active learning annotation efficiency", "human_ai_collaboration"),
    # RAG
    ("retrieval augmented generation production evaluation", "rag_production"),
    ("RAG hallucination reduction enterprise", "rag_production"),
    ("GraphRAG knowledge retrieval", "rag_production"),
    # Reliability
    ("LLM guardrails production safety", "ai_reliability"),
    ("hallucination detection large language model", "ai_reliability"),
    ("prompt injection defense LLM", "ai_reliability"),
    ("AI agent evaluation reliability", "ai_reliability"),
    # Domain-specific
    ("clinical decision support AI deployment", "domain_healthcare"),
    ("drug discovery machine learning optimization", "domain_healthcare"),
    ("legal reasoning AI contract analysis", "domain_legal"),
    ("financial fraud detection machine learning", "domain_finance"),
    ("credit scoring interpretable machine learning", "domain_finance"),
    # Efficient inference
    ("LLM inference optimization serving", "efficient_inference"),
    ("model quantization deployment production", "efficient_inference"),
    ("speculative decoding efficient LLM", "efficient_inference"),
    # Economics
    ("automated mechanism design deep learning", "ai_economics"),
    ("auction design neural network", "ai_economics"),
    ("AI market design platform economics", "ai_economics"),
    # Causal
    ("causal inference machine learning decision making", "causal_ml"),
    ("treatment effect estimation heterogeneous", "causal_ml"),
    ("causal discovery industrial process", "causal_ml"),
    # Sim-to-real
    ("sim-to-real transfer industrial", "sim_to_real"),
    ("digital twin machine learning manufacturing", "sim_to_real"),
    # Neurosymbolic
    ("neurosymbolic AI enterprise reasoning", "neurosymbolic"),
    ("knowledge graph neural reasoning", "neurosymbolic"),
    # Compound AI
    ("compound AI systems multi-model pipeline", "compound_ai"),
    ("LLM pipeline orchestration optimization", "compound_ai"),
]

# ---------------------------------------------------------------------------
# Frontier area → human-readable label + suggested domain tag
# ---------------------------------------------------------------------------

FRONTIER_AREAS: dict[str, dict[str, str]] = {
    "continual_learning_agents": {"label": "Self-Improving Agents", "domain": "Continual Learning"},
    "rl_production":             {"label": "RL in Production", "domain": "Reinforcement Learning"},
    "multi_agent":               {"label": "Multi-Agent Systems", "domain": "Agent Orchestration"},
    "llm_automation":            {"label": "LLM Process Automation", "domain": "Automation"},
    "ai_operations_research":    {"label": "AI + Operations Research", "domain": "Operations Research"},
    "human_ai_collaboration":    {"label": "Human-AI Collaboration", "domain": "Decision Making"},
    "rag_production":            {"label": "RAG in Production", "domain": "Search & Retrieval"},
    "ai_reliability":            {"label": "AI Reliability & Guardrails", "domain": "AI Safety"},
    "domain_healthcare":         {"label": "Healthcare AI", "domain": "Healthcare"},
    "domain_legal":              {"label": "Legal AI", "domain": "Legal"},
    "domain_finance":            {"label": "Financial AI", "domain": "Finance"},
    "efficient_inference":       {"label": "Efficient Inference", "domain": "Efficiency"},
    "ai_economics":              {"label": "AI for Economics", "domain": "Economics"},
    "causal_ml":                 {"label": "Causal ML", "domain": "Causal Inference"},
    "sim_to_real":               {"label": "Sim-to-Real & Digital Twins", "domain": "Simulation"},
    "neurosymbolic":             {"label": "Neurosymbolic AI", "domain": "Reasoning"},
    "compound_ai":               {"label": "Compound AI Systems", "domain": "Systems"},
}

# ---------------------------------------------------------------------------
# Relevance filtering — what makes something "applied AI research"
# ---------------------------------------------------------------------------

# Papers/posts containing ANY of these signals are more likely to be applied research
APPLIED_SIGNALS: list[str] = [
    # Deployment / production context
    "production", "deployment", "deployed", "real-world", "real world",
    "in practice", "at scale", "industrial", "enterprise", "industry",
    "case study", "field study", "pilot",
    # Specific applied domains
    "manufacturing", "healthcare", "clinical", "medical", "hospital",
    "financial", "banking", "trading", "credit", "fraud",
    "logistics", "supply chain", "warehouse", "routing", "fleet",
    "retail", "e-commerce", "recommendation",
    "energy", "power grid", "renewable", "smart grid",
    "legal", "contract", "compliance",
    "agriculture", "precision farming",
    "telecom", "network optimization",
    "insurance", "claims", "underwriting",
    "construction", "building",
    # Applied methods
    "reinforcement learning", "RL agent", "reward shaping",
    "continual learning", "lifelong learning", "self-improving",
    "human-in-the-loop", "human-AI", "active learning",
    "retrieval augmented", "RAG",
    "guardrails", "safety filter", "hallucination detection",
    "prompt injection", "red teaming",
    "multi-agent", "agent orchestration", "tool use",
    "workflow automation", "process automation", "RPA",
    "combinatorial optimization", "vehicle routing", "scheduling",
    "mechanism design", "auction", "market design",
    "causal inference", "treatment effect", "counterfactual",
    "digital twin", "sim-to-real", "simulation",
    "neurosymbolic", "knowledge graph reasoning",
    "compound AI", "model routing", "cascade",
    "quantization", "efficient inference", "model serving",
    "speculative decoding", "KV cache",
    # Impact signals
    "cost reduction", "latency reduction", "accuracy improvement",
    "throughput", "efficiency gain", "ROI",
    "A/B test", "online experiment",
]

# Papers/posts with ONLY these signals and nothing else are probably
# foundation-model announcements, NOT applied research — deprioritize
DEPRIORITIZE_SIGNALS: list[str] = [
    "we introduce a new model",
    "we present a new architecture",
    "we release",
    "state-of-the-art on",
    "benchmark results",
    "we train a",
    "pre-training",
    "instruction tuning",
    "MMLU", "HellaSwag", "HumanEval",  # benchmark names
    "scaling law",
]

# ---------------------------------------------------------------------------
# Industry and domain detection — improved from abstract text
# ---------------------------------------------------------------------------

INDUSTRY_KEYWORDS: dict[str, list[str]] = {
    "Healthcare": [
        "healthcare", "medical", "clinical", "hospital", "patient",
        "diagnosis", "drug discovery", "pharmaceutical", "EHR",
        "electronic health record", "radiology", "pathology",
        "clinical trial", "genomics", "biomedical",
    ],
    "Finance": [
        "financial", "banking", "trading", "stock", "portfolio",
        "credit", "fraud detection", "anti-money laundering", "AML",
        "insurance", "underwriting", "risk management", "fintech",
        "algorithmic trading", "credit scoring",
    ],
    "Manufacturing": [
        "manufacturing", "factory", "assembly", "production line",
        "industrial", "quality control", "predictive maintenance",
        "defect detection", "process control", "CNC", "shop floor",
    ],
    "Retail & E-commerce": [
        "retail", "e-commerce", "shopping", "consumer", "merchandise",
        "recommendation system", "product search", "personalization",
        "demand forecasting", "inventory management",
    ],
    "Energy": [
        "energy", "power grid", "renewable", "solar", "wind",
        "electricity", "smart grid", "battery", "oil and gas",
        "carbon", "sustainability", "energy efficiency",
    ],
    "Transportation & Logistics": [
        "transportation", "autonomous driving", "vehicle", "traffic",
        "routing", "logistics", "warehouse", "delivery", "shipping",
        "fleet", "last mile", "freight", "supply chain",
    ],
    "Agriculture": [
        "agriculture", "crop", "farming", "soil", "harvest",
        "precision agriculture", "irrigation", "livestock",
    ],
    "Legal": [
        "legal", "law firm", "contract", "case law", "litigation",
        "compliance", "regulatory", "patent", "intellectual property",
    ],
    "Education": [
        "education", "student", "tutoring", "curriculum",
        "learning analytics", "adaptive learning", "edtech",
    ],
    "Telecommunications": [
        "telecom", "network traffic", "5g", "wireless", "cellular",
        "spectrum", "network optimization",
    ],
    "Construction & Real Estate": [
        "construction", "building", "real estate", "property",
        "architecture", "BIM", "building information",
    ],
}

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "Reinforcement Learning": [
        "reinforcement learning", "RL agent", "reward", "policy gradient",
        "Q-learning", "PPO", "DQN", "DDPG", "actor-critic",
        "multi-armed bandit", "contextual bandit", "offline RL",
        "safe RL", "constrained RL", "reward shaping",
    ],
    "Continual Learning": [
        "continual learning", "lifelong learning", "catastrophic forgetting",
        "self-improving", "skill acquisition", "memory management",
        "experience replay", "knowledge retention",
    ],
    "Operations Research": [
        "operations research", "combinatorial optimization",
        "vehicle routing", "scheduling", "assignment problem",
        "bin packing", "knapsack", "integer programming",
        "mixed-integer", "constraint satisfaction",
    ],
    "Economics": [
        "economics", "economic", "market design", "mechanism design",
        "auction", "welfare", "incentive", "equilibrium",
        "game theory", "pricing", "revenue optimization",
    ],
    "Causal Inference": [
        "causal inference", "causal discovery", "treatment effect",
        "counterfactual", "do-calculus", "instrumental variable",
        "causal forest", "double ML", "structural causal",
    ],
    "Efficiency": [
        "efficient inference", "quantization", "pruning", "distillation",
        "latency", "throughput", "compression", "model serving",
        "speculative decoding", "KV cache", "FlashAttention",
    ],
    "AI Safety": [
        "guardrails", "hallucination", "faithfulness", "grounding",
        "prompt injection", "jailbreak", "red teaming", "toxicity",
        "AI safety", "alignment", "evaluation framework",
    ],
    "Automation": [
        "automation", "workflow", "process automation", "RPA",
        "document processing", "information extraction",
        "task automation", "enterprise automation",
    ],
    "Agent Orchestration": [
        "multi-agent", "agent orchestration", "tool use",
        "function calling", "agent coordination", "task planning",
        "agent communication", "agent framework",
    ],
    "Search & Retrieval": [
        "retrieval augmented", "RAG", "semantic search",
        "knowledge retrieval", "re-ranking", "dense retrieval",
        "hybrid search", "GraphRAG",
    ],
    "Decision Making": [
        "decision support", "decision making", "human-in-the-loop",
        "human-AI", "active learning", "interactive ML",
        "uncertainty estimation", "calibration",
    ],
    "Simulation": [
        "sim-to-real", "digital twin", "simulation", "synthetic data",
        "domain randomization", "physics-informed",
    ],
    "Reasoning": [
        "neurosymbolic", "symbolic reasoning", "knowledge graph",
        "logical reasoning", "rule learning", "ontology",
    ],
    "Systems": [
        "compound AI", "model routing", "cascade", "pipeline",
        "multi-model", "ensemble", "model selection",
        "MLOps", "model monitoring",
    ],
    "Forecasting": [
        "forecasting", "time series", "demand forecasting",
        "prediction", "nowcasting", "probabilistic forecasting",
    ],
    "Supply Chain": [
        "supply chain", "inventory", "procurement", "vendor",
        "demand planning", "order fulfillment",
    ],
    "Pricing": [
        "pricing", "dynamic pricing", "price optimization",
        "revenue management", "yield management",
    ],
    "Optimization": [
        "optimization", "optimize", "resource allocation",
        "cost minimization", "objective function",
    ],
}

# RSS relevance keywords — posts must contain at least one to be collected
RSS_RELEVANCE_KEYWORDS: list[str] = [
    # Applied research signals (NOT just product announcements)
    "research", "paper", "study", "findings", "approach",
    "method", "technique", "framework", "system",
    # Specific frontier areas
    "reinforcement learning", "RL",
    "continual learning", "self-improving",
    "multi-agent", "agent", "agentic",
    "retrieval augmented", "RAG",
    "guardrails", "safety", "reliability", "evaluation",
    "human-in-the-loop", "human-AI",
    "optimization", "operations research",
    "causal", "counterfactual",
    "mechanism design", "auction",
    "digital twin", "simulation",
    "neurosymbolic", "knowledge graph",
    "compound AI", "pipeline",
    "quantization", "inference", "serving", "efficiency",
    "automation", "workflow",
    # Domain applications
    "healthcare", "medical", "clinical",
    "financial", "fraud", "credit",
    "manufacturing", "industrial",
    "logistics", "supply chain", "routing",
    "legal", "contract",
    # Technical depth signals
    "benchmark", "ablation", "experiment",
    "deployment", "production", "scale",
    "open source", "open-source",
]


def compute_relevance_score(title: str, description: str) -> float:
    """Score how relevant a piece of content is to applied AI research.

    Returns a float 0-1 where higher = more relevant.
    """
    text = f"{title} {description}".lower()

    # Count applied signals
    applied_hits = sum(1 for s in APPLIED_SIGNALS if s in text)

    # Count deprioritize signals
    depri_hits = sum(1 for s in DEPRIORITIZE_SIGNALS if s in text)

    # Base score from applied signals (diminishing returns)
    if applied_hits == 0:
        score = 0.1
    elif applied_hits <= 2:
        score = 0.3
    elif applied_hits <= 5:
        score = 0.5
    elif applied_hits <= 10:
        score = 0.7
    else:
        score = 0.9

    # Penalty for deprioritize signals (but don't go below 0.1)
    if depri_hits > 0 and applied_hits < 3:
        score = max(0.1, score - 0.2 * depri_hits)

    return round(score, 2)


def detect_industry(text: str) -> str | None:
    """Detect the most relevant industry from text."""
    text_lower = text.lower()
    best_industry = None
    best_count = 0
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > best_count:
            best_count = count
            best_industry = industry
    return best_industry if best_count >= 1 else None


def detect_domain(text: str) -> str | None:
    """Detect the most relevant research domain from text."""
    text_lower = text.lower()
    best_domain = None
    best_count = 0
    for domain, keywords in DOMAIN_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > best_count:
            best_count = count
            best_domain = domain
    return best_domain if best_count >= 1 else None


def is_relevant_rss(title: str, description: str) -> bool:
    """Check if an RSS post is relevant to applied AI research."""
    combined = f"{title} {description}".lower()
    return any(kw in combined for kw in RSS_RELEVANCE_KEYWORDS)
