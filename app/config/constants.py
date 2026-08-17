class Constants:
    AGENT_RESEARCHER = "researcher"
    AGENT_ANALYZER = "analyzer"
    AGENT_SYNTHESIZER = "synthesizer"

    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    # LLM
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL: str = "google/gemma-4-31B-it:novita"


constants = Constants()
