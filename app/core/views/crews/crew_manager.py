import os
from crewai import Agent, Task, Crew, Process, LLM


llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)
# Optional: Use environment variables for API keys
os.environ["GEMINI_API_KEY"] = ""
def create_crew():
    # Define agents
    researcher = Agent(
        role='Researcher',
        goal='Conduct thorough research on {topic}',
        verbose=True,
        memory=True,
        backstory='A diligent researcher passionate about uncovering insights.',
        llm=llm
    )

    writer = Agent(
        role='Writer',
        goal='Write a compelling article about {topic}',
        verbose=True,
        memory=True,
        backstory='A creative writer who simplifies complex topics.',
        llm=llm
    )

    # Define tasks
    research_task = Task(
        description=(
            "Research the topic and gather key points."
            "Your report should include the pros and cons."
        ),
        expected_output='A detailed summary of the topic.',
        agent=researcher,
    )

    write_task = Task(
        description=(
            "Write an article based on the research."
            "Make it engaging and informative."
        ),
        expected_output='A 500-word article in markdown format.',
        agent=writer,
    )

    # Define crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
    )

    return crew

def kickoff_crew(inputs):
    crew = create_crew()
    result = crew.kickoff(inputs=inputs)
    return str(result)
