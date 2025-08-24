from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, crew, task, llm
from django.conf import settings
from pydantic import BaseModel
import os


os.environ["GEMINI_API_KEY"] = getattr(settings, 'GEMINI_API_KEY', "")

class Email(BaseModel):
    subject: str
    content: str

@CrewBase
class EmailCrew():
  """CreditApprovalEmail crew"""
  
  @llm
  def gemini_llm(self) -> LLM:
    llm = LLM(
        model="gemini/gemini-2.0-flash-lite",
        temperature=0.7,
    )
    return llm

  agents_config = "config/agents.yaml"

  @agent
  def email_assistant(self) -> Agent:
    return Agent(
      config=self.agents_config['email_assistant'],
      llm=self.gemini_llm()
    )

  @agent
  def email_qa_agent(self) -> Agent:
    return Agent(
      config=self.agents_config['email_qa_agent'],
      llm=self.gemini_llm()
    )
  
  @task
  def email_task(self) -> Task:
    return Task(
      config=self.tasks_config['credit_approval_email_task'],
    )

  @task
  def email_quality_assurance_task(self) -> Task:
    return Task(
      config=self.tasks_config['email_qa_task'], 
      output_json=Email
    )

  @crew
  def crew(self) -> Crew:
    """Creates the CreditApprovalEmail crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      verbose=True,
    )
  
