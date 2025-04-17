import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai


def check_api_key(api_key):
    """Verify if the API key is valid."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return any("gemini" in model.name.lower() for model in models)
    except Exception:
        return False


def get_gemini_llm(api_key, temperature=0.7):
    """Create and return a Gemini LLM instance."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                  google_api_key=api_key,
                                  temperature=temperature,
                                  max_output_tokens=2048)


def summarize_text(text, length="Medium", api_key=None):
    """Summarize the given text using the Gemini API."""
    length_guide = {
        "Very Short":
        "Provide an extremely concise summary in 2-3 sentences.",
        "Short":
        "Provide a brief summary in a short paragraph.",
        "Medium":
        "Provide a comprehensive summary covering all main points.",
        "Detailed":
        "Provide a detailed summary with all important information and supporting details."
    }

    template = """
    You are an expert academic assistant helping a student summarize their notes.
    
    TEXT TO SUMMARIZE:
    {text}
    
    INSTRUCTIONS:
    {length_guide}
    - Focus on key concepts, definitions, and important points
    - Maintain academic language and technical terms
    - Organize information in a clear, logical structure
    - Include any formulas, theorems, or key dates if present
    
    SUMMARY:
    """

    prompt = PromptTemplate(input_variables=["text", "length_guide"],
                            template=template)

    llm = get_gemini_llm(api_key,
                         temperature=0.2)  # Lower temperature for summaries
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(text=text, length_guide=length_guide[length])
    return response


def answer_question(question,
                    subject_area="General",
                    context=None,
                    api_key=None):
    """Answer academic questions using the Gemini API."""
    context_section = ""
    if context:
        context_section = f"""
        ADDITIONAL CONTEXT FROM STUDENT'S NOTES:
        {context}
        
        Use this context to inform your answer if relevant to the question.
        """

    template = """
    You are an expert academic tutor specializing in {subject_area}.
    
    STUDENT QUESTION:
    {question}
    
    {context_section}
    
    INSTRUCTIONS:
    - Provide a comprehensive, educational answer 
    - Include key concepts and definitions
    - If applicable, mention different perspectives or theories
    - If the question is unclear, clarify your interpretation before answering
    - If the question asks for a step-by-step explanation, provide clear steps
    - Include examples if they would help illustrate the answer
    - If the question is requesting false or misleading information, politely correct any misconceptions
    
    ANSWER:
    """

    prompt = PromptTemplate(
        input_variables=["question", "subject_area", "context_section"],
        template=template)

    llm = get_gemini_llm(
        api_key, temperature=0.7)  # Higher temperature for creative answers
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(question=question,
                         subject_area=subject_area,
                         context_section=context_section)
    return response


def generate_study_tips(subject,
                        goal,
                        learning_style,
                        additional_info="",
                        api_key=None):
    """Generate personalized study tips using the Gemini API."""
    template = """
    You are an expert education consultant specializing in personalized study strategies.
    
    STUDENT INFORMATION:
    - Subject/Topic: {subject}
    - Study Goal: {goal}
    - Learning Style: {learning_style}
    - Additional Information: {additional_info}
    
    INSTRUCTIONS:
    - Provide 5-7 specific, actionable study tips tailored to the student's needs
    - Focus on evidence-based learning techniques relevant to their subject and goal
    - Include both general strategies and subject-specific approaches
    - Consider their learning style in your recommendations
    - Suggest specific tools, resources, or techniques that would be helpful
    - Format your response with clear headings, bullet points, and organization
    
    PERSONALIZED STUDY TIPS:
    """

    prompt = PromptTemplate(input_variables=[
        "subject", "goal", "learning_style", "additional_info"
    ],
                            template=template)

    llm = get_gemini_llm(
        api_key, temperature=0.8)  # Higher temperature for personalized tips
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(subject=subject,
                         goal=goal,
                         learning_style=learning_style,
                         additional_info=additional_info)
    return response
