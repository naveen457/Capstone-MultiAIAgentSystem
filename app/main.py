from app.chains.test import chain

query = "Write about India in future"
result = chain.invoke({"topic": query})
print(result)
