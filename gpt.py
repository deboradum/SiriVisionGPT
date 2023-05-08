import dotenv
import openai


# Sets API key.
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

class GPThandler():
    def __init__(self, max_history, language):
        self.history = [{"role": "system", "content": f"You are a helpful assistant that gives concise answers. You answer in the language {language}"}]
        self.max_history = max_history

    def append_history(self, message):
        if len(self.history) >= self.max_history:
            del self.history[1:3]

        self.history.append(message)


    def conversate(self, prompt):
        message = {"role": "user", "content": prompt}
        self.append_history(message)
        r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.history)

        reply = r['choices'][0]['message']['content']
        tokens_used = r['usage']['total_tokens']

        return reply, tokens_used
