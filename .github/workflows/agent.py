import glob
import anthropic

# 1. Read the failed test output
log = open("test.log").read()[-6000:]

# 2. Read the project's code
code = ""
for path in glob.glob("*.py"):
    if path != "agent.py":
        code += f"\n--- {path} ---\n" + open(path).read()

# 3. Ask Claude to diagnose it
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
reply = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=800,
    system=(
        "You are a DevOps assistant. A CI pipeline just failed. "
        "Explain the root cause in plain English, point to the exact file "
        "and line, and give the fixed code. Be short and practical."
    ),
    messages=[{
        "role": "user",
        "content": f"TEST LOG:\n{log}\n\nCODE:\n{code}",
    }],
)

# 4. Save the diagnosis
text = reply.content[0].text
with open("diagnosis.md", "w") as f:
    f.write("## 🤖 AI Failure Diagnosis\n\n" + text)
print(text)
