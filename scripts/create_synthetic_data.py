from enum import Enum
import logging
import logging.config
import os
import random
from google.genai import Client
from google.genai.types import Part, UserContent, GenerateContentConfig
import json
from dotenv import load_dotenv
from datetime import datetime
import time

logger = logging.getLogger(__name__)

load_dotenv("config/.env")


# https://ai.google.dev/gemini-api/docs/rate-limits
class VALID_LLM_MODELS(Enum):
    GEMINI_2_5_FLASH_LITE_PREVIEW_06_17 = "gemini-2.5-flash-lite-preview-06-17"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"


TRUMP_PROMPT = """
Pretend you are Donald Trump. Answer each question in the typicall style of Donald Trump. Only answer the question, do not include any other text or markup or quotes.
"""


class TrumpAI:
    def __init__(self, top_p: float, llms: list[str]):
        self.top_p = top_p
        for llm in llms:
            if llm not in VALID_LLM_MODELS:
                raise ValueError(f"Invalid LLM: {llm}. Valid LLMs: {VALID_LLM_MODELS}")
        self.llms = llms

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY env var is not set")
        self.gemini_client = Client(api_key=api_key)
        self.chat = self.gemini_client.chats.create(
            model=self._select_llm(),
            config=GenerateContentConfig(
                top_p=self.top_p, system_instruction=TRUMP_PROMPT
            ),
        )

    def _select_llm(self) -> str:
        llm = random.choice(self.llms)
        logger.debug(f"Selected LLM: {llm}")
        return llm

    def answer(self, question: str) -> str:
        response = self.chat.send_message(question)
        return response.text


INTERVIEWR_PROMPT = """
You are an interviewer, interested in trying to get to know details about someones life. Ask short by to the point questions trying to agitate the interviewee.
"""


class InterviewerAI:
    def __init__(self, top_p: float, llms: list[str]):
        self.top_p = top_p
        for llm in llms:
            if llm not in VALID_LLM_MODELS:
                raise ValueError(f"Invalid LLM: {llm}. Valid LLMs: {VALID_LLM_MODELS}")
        self.llms = llms
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY env var is not set")
        self.gemini_client = Client(api_key=api_key)
        self.chat = self.gemini_client.chats.create(
            model=self._select_llm(),
            config=GenerateContentConfig(
                top_p=self.top_p, system_instruction=INTERVIEWR_PROMPT
            ),
        )

    def _select_llm(self) -> str:
        llm = random.choice(self.llms)
        logger.debug(f"Selected LLM: {llm}")
        return llm

    def get_initial_question(self) -> str:
        result = self.gemini_client.models.generate_content(
            model=self._select_llm(),
            config=GenerateContentConfig(
                top_p=self.top_p, system_instruction=INTERVIEWR_PROMPT
            ),
            contents=[
                UserContent(
                    parts=[
                        Part(text="Ask me a question."),
                    ],
                ),
            ],
        )
        return result.text

    def answer(self, answer: str) -> str:
        response = self.chat.send_message(answer)
        return response.text


class BasicQuestionsInterviewer:
    def __init__(self):
        self.questions = ["How should I call you?", "Are you Donald Trump?", "Trump?"]

    def ask(self) -> str:
        return random.choice(self.questions)


def _save_conversations_to_jsonl(conversations, outdir, file_name):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    file_path = os.path.join(outdir, file_name)
    with open(file_path, "w") as file:
        for conversation in conversations:
            item = {"conversations": conversation}
            json_string = json.dumps(item, ensure_ascii=False)
            file.write(f"{json_string}\n")


def _preprocess_answer(answer: str) -> str:
    # remove new lines
    answer = answer.replace("\n", " ")
    # remove quotes
    answer = answer.replace('"', "")
    return answer


def _ai_interview(turns: int):
    conversation = []
    interviewer = InterviewerAI(
        top_p=0.95, llms=[VALID_LLM_MODELS.GEMINI_2_5_FLASH_LITE_PREVIEW_06_17.value]
    )
    trump = TrumpAI(top_p=0.95, llms=[VALID_LLM_MODELS.GEMINI_2_5_FLASH.value])

    question = interviewer.get_initial_question()
    print(f"Interviewer: {question[:100]}")
    conversation.append({"role": "user", "content": _preprocess_answer(question)})
    answer = trump.answer(question)
    conversation.append({"role": "assistant", "content": _preprocess_answer(answer)})
    print(f"Trump: {answer[:100]}")
    for _ in range(turns - 1):
        question = interviewer.answer(answer)
        print(f"Interviewer: {question[:100]}")
        conversation.append({"role": "user", "content": _preprocess_answer(question)})
        answer = trump.answer(question)
        conversation.append(
            {"role": "assistant", "content": _preprocess_answer(answer)}
        )
        print(f"Trump: {answer[:100]}")
    return conversation


def _basic_interview():
    conversation = []
    interviewer = BasicQuestionsInterviewer()
    trump = TrumpAI(top_p=0.95, llms=[VALID_LLM_MODELS.GEMINI_2_5_FLASH.value])

    question = interviewer.ask()
    print(f"Interviewer: {question[:100]}")
    conversation.append({"role": "user", "content": _preprocess_answer(question)})
    answer = trump.answer(question)
    conversation.append({"role": "assistant", "content": _preprocess_answer(answer)})
    print(f"Trump: {answer[:100]}")
    return conversation


def generate_synthetic_data(
    basic_interviews: int,
    total_ai_interviews: int,
    max_ai_interview_turns: int,
    sleep_time: int = 5,
):
    conversations = []
    for _ in range(basic_interviews):
        print(f"Generating basic interview {_ + 1} of {basic_interviews}")
        try:
            conversation = _basic_interview()
            conversations.append(conversation)
            print(f"Basic interview {_ + 1} of {basic_interviews} saved")
        except Exception as e:
            print(
                f"Error generating basic interview {_ + 1} of {basic_interviews}: {e}"
            )
            continue
        time.sleep(sleep_time)

    for _ in range(total_ai_interviews):
        print(f"Generating AI interview {_ + 1} of {total_ai_interviews}")
        turns = random.randint(1, max_ai_interview_turns)
        try:
            conversation = _ai_interview(turns)
            conversations.append(conversation)
            print(f"AI interview {_ + 1} of {total_ai_interviews} saved")
        except Exception as e:
            print(
                f"Error generating AI interview {_ + 1} of {total_ai_interviews}: {e}"
            )
            continue
        time.sleep(sleep_time)

    # current date_time in format YYYY-MM-DD_HH-MM-SS
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _save_conversations_to_jsonl(
        conversations,
        "data/trainset/synthetic/",
        f"synthetic_data_{date_time}.jsonl",
    )


if __name__ == "__main__":
    generate_synthetic_data(
        basic_interviews=15,
        total_ai_interviews=30,
        max_ai_interview_turns=3,
        sleep_time=5,
    )
