import os
import json
import random


def _read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def _get_file_paths_from_directory(directory):
    return [os.path.join(directory, filename) for filename in os.listdir(directory)]


def _parse_turn_from_line(line, user_tag="INTERVIEWER:", assistant_tag="TRUMP:"):
    if user_tag in line:
        return {"role": "user", "content": line.replace(user_tag, "").strip()}
    elif assistant_tag in line:
        return {"role": "assistant", "content": line.replace(assistant_tag, "").strip()}
    else:
        return {"role": "same", "content": line.strip()}


def _construct_conversations_from_interview(
    interview_transcript: str,
    assistant_min_sample_turns: int = 1,
    assistant_max_sample_turns: int = 2,
):
    conversations = []

    # split interview on new lines
    interview_lines = interview_transcript.split("\n")

    min_assistant_turns = random.randint(
        assistant_min_sample_turns, assistant_max_sample_turns
    )

    current_assistant_turns = 0
    current_user_turns = 0

    current_conversation = []
    for line in interview_lines:
        if current_assistant_turns >= min_assistant_turns and current_user_turns >= 1:
            min_assistant_turns = random.randint(
                assistant_min_sample_turns, assistant_max_sample_turns
            )
            conversations.append(current_conversation)
            current_conversation = []
            current_assistant_turns = 0
            current_user_turns = 0

        turn = _parse_turn_from_line(
            line, user_tag="INTERVIEWER:", assistant_tag="TRUMP:"
        )
        if turn["role"] == "same":
            if len(current_conversation) > 0:
                current_conversation[-1]["content"] += " " + turn["content"]
            continue
        elif turn["role"] == "assistant":
            if (
                len(current_conversation) > 0
                and current_conversation[-1]["role"] == "assistant"
            ):
                current_conversation[-1]["content"] += " " + turn["content"]
                continue
            if current_user_turns > 0:
                current_assistant_turns += 1
                current_conversation.append(turn)
        elif turn["role"] == "user":
            if (
                len(current_conversation) > 0
                and current_conversation[-1]["role"] == "user"
            ):
                current_conversation[-1]["content"] += " " + turn["content"]
                continue
            current_user_turns += 1
            current_conversation.append(turn)

    return conversations


def _save_conversations_to_jsonl(conversations, outdir, file_name):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    file_path = os.path.join(outdir, file_name)
    with open(file_path, "w") as file:
        for conversation in conversations:
            item = {"conversations": conversation}
            json_string = json.dumps(item, ensure_ascii=False)
            file.write(f"{json_string}\n")


def construct_trainset(clean_transcripts_dir: str, outdir: str):
    file_paths = _get_file_paths_from_directory(clean_transcripts_dir)
    for file_path in file_paths:
        interview_text = _read_file(file_path)
        conversations = _construct_conversations_from_interview(interview_text)
        file_name = file_path.split("/")[-1].replace(".txt", ".jsonl")
        _save_conversations_to_jsonl(conversations, outdir, file_name)


construct_trainset(
    clean_transcripts_dir="data/transcripts/clean",
    outdir="data/trainset/transcripts",
)
