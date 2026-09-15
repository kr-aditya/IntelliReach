import json

from crewai import LLM, Agent, Crew, Process, Task

import crewai.llms.cache as _crewai_cache

from app.rag.vector_store import VectorStore


# ============================================================
# CrewAI / Groq compatibility workaround
# ============================================================

_crewai_cache.mark_cache_breakpoint = lambda msg: msg


# ============================================================
# RAG Answer Model
# ============================================================

from pydantic import BaseModel, Field


class RAGAnswer(BaseModel):

    answer: str = Field(
        description=(
            "A concise answer based only on the retrieved "
            "document context."
        )
    )

    sources: list[str] = Field(
        description=(
            "Sources or document references used to answer "
            "the question."
        )
    )


# ============================================================
# RAG LLM
# ============================================================

rag_llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0.1,
    max_tokens=300,
    reasoning_effort="low",
)


# ============================================================
# RAG Service
# ============================================================

class RAGService:

    def __init__(self) -> None:

        self.vector_store = VectorStore()

        self.agent = Agent(
            role="Document Question Answering Specialist",

            goal=(
                "Answer questions accurately using only "
                "the supplied document context."
            ),

            backstory=(
                "You are a careful document analysis specialist. "
                "You answer questions using retrieved evidence, "
                "avoid unsupported claims, and clearly indicate "
                "when the available documents do not contain "
                "the requested information."
            ),

            llm=rag_llm,

            verbose=True,
        )


    # ========================================================
    # Ask Question
    # ========================================================

    def ask(
        self,
        question: str,
    ) -> RAGAnswer:

        question = question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )


        # ----------------------------------------------------
        # 1. Retrieve relevant chunks
        # ----------------------------------------------------

        retriever = (
            self.vector_store.get_retriever()
        )

        documents = retriever.invoke(
            question
        )
        print(
            f"\nRAG DEBUG: Retrieved {len(documents)} documents "
            f"for question: {question}\n"
        )

        for index, document in enumerate(documents, start=1):
         print(
            f"\n--- Retrieved Document {index} ---"
        )

        print(
         document.page_content[:500]
        )

        print(
          "Metadata:",
           document.metadata
        )

        


        if not documents:

            return RAGAnswer(
                answer=(
                    "I could not find relevant information "
                    "in the knowledge base."
                ),
                sources=[],
            )


        # ----------------------------------------------------
        # 2. Build context
        # ----------------------------------------------------

        context_parts = []

        sources = []

        for document in documents:

            context_parts.append(
                document.page_content
            )

            source = document.metadata.get(
                "source"
            )

            if source and source not in sources:

                sources.append(source)


        context = "\n\n---\n\n".join(
            context_parts
        )


        # ----------------------------------------------------
        # 3. Ask LLM
        # ----------------------------------------------------

        task = Task(

            description=(
                "Answer the user's question using ONLY "
                "the retrieved document context.\n\n"

                f"USER QUESTION:\n{question}\n\n"

                f"RETRIEVED CONTEXT:\n{context}\n\n"

                "Rules:\n"
                "1. Use only information supported by the context.\n"
                "2. Do not invent facts.\n"
                "3. If the answer is not available in the context, "
                "say that the knowledge base does not contain "
                "enough information.\n"
                "4. Keep the answer concise.\n\n"

                "Return ONLY valid JSON.\n"
                "Do not use Markdown.\n"
                "Do not wrap the JSON in ```.\n\n"

                "Use exactly this JSON structure:\n"
                "{\n"
                '  "answer": "string",\n'
                '  "sources": ["string"]\n'
                "}"
            ),

            expected_output=(
                "Valid JSON containing an evidence-based answer "
                "and a list of source references."
            ),

            agent=self.agent,
        )


        # ----------------------------------------------------
        # 4. Execute
        # ----------------------------------------------------

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()


        # ----------------------------------------------------
        # 5. Validate
        # ----------------------------------------------------

        raw_output = result.raw.strip()

        try:

            data = json.loads(
                raw_output
            )

            return RAGAnswer.model_validate(
                data
            )

        except (json.JSONDecodeError, ValueError) as error:

            raise ValueError(
                f"RAG agent produced invalid output: {error}"
            ) from error