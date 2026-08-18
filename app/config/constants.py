class Constants:
    AGENT_RESEARCHER = "researcher"
    AGENT_ANALYZER = "analyzer"
    AGENT_SYNTHESIZER = "synthesizer"

    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    # LLM no need since me moved entirly to open router platform api key does to more available credits
    # LLM_PROVIDER: str = "huggingface"
    # LLM_MODEL: str = "deepseek-ai/DeepSeek-V4-Flash"


constants = Constants()
