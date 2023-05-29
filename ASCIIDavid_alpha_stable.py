import getpass
import openai
import os
import time
import re
import logging
import sys
from dotenv import load_dotenv

# Create a logger object
logger = logging.getLogger(__name__)

# Set the level of verbosity
logger.setLevel(logging.DEBUG)

# Create a file handler for writing to a log file
log_file = "console.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create a stream handler for writing to the standard output
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# Create a formatter for the log messages
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n")

# Set the formatter for both handlers
file_handler.setFormatter(log_format)
stream_handler.setFormatter(log_format)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Test the logger by writing some messages
#logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.warning("This is a warning message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")


# Set the formatter for both handlers
file_handler.setFormatter(log_format)
stream_handler.setFormatter(log_format)

# Load environment variables
load_dotenv()

# Assign OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    def __init__(self):
        pass

    def get_response(self, prompt, temperature=0.8, max_tokens=1000, **kwargs):
        model = 'gpt-3.5-turbo'
        delay = 1
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    frequency_penalty=0.5, # add this line
                    **kwargs
                )
                time.sleep(1)
            except openai.error.RateLimitError:
                logging.warning(f"Rate limit error encountered. Waiting for {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2
            else:
                # Define a regular expression pattern for the message
                pattern = r"Sorry, as an AI language model, I am unable to create ASCII art. However, here's an example of ASCII art of .*:"

                # Define a list of keywords to screen
                keywords = ["AI", "language", "model", "ASCII", "art", "Sorry", "However", "Apologies","Here is"]

                # Split the message by newline characters
                message = response['choices'][0]['message']['content'].strip()
                lines = message.split("\n")

                # Filter out lines that match the pattern or contain any of the keywords
                filtered_lines = list(filter(lambda l: not (re.match(pattern, l) or any(k in l for k in keywords)), lines))

                # Join the filtered lines with newline characters
                filtered_message = "\n".join(filtered_lines)

                return filtered_message


class ArtistAgent(Agent):
    def __init__(self):
        super().__init__()

    def create_prompt(self, context, max_lines=100):
        prompt = [
             {"role": "system", "content": "You are a coding Artist. You can only create and respond in ASCII art. No words or replies allowed."},
             {"role": "user", "content": f"Create ASCII art based on this context:\n\n{context}\n\nLimit your art to {max_lines} lines."}
             ]
        
        return prompt

    def generate_ascii_art(self, context, max_lines=100, max_width=160, min_length=150, min_unique_chars=5):
        prompt = self.create_prompt(context, max_lines)
        ascii_art = self.get_response(prompt, max_tokens=200)
        time.sleep(1)

        while not ascii_art or len(ascii_art) < min_length or len(set(ascii_art)) < min_unique_chars or any(len(line) > max_width for line in ascii_art.splitlines()):
            ascii_art = self.get_response(prompt, max_tokens=100)
            time.sleep(1)

        # Define a function to filter out the unwanted output
        def filter_output(output):
            # Define a regular expression pattern for the message
            pattern = r"Sorry, as an AI language model, I am unable to create ASCII art. However, here's an example of ASCII art of .*:"

            # Define a list of keywords to screen
            keywords = ["AI", "language", "model", "ASCII", "art", "Sorry", "sorry", "However"]

            # Check if the output matches the pattern or contains any of the keywords
            match = re.search(pattern, output) or any(keyword in output for keyword in keywords)

            # Return the output only if it does not match the pattern or contain any of the keywords
            if not match:
                return output
            else:
                return None

        # Apply the filter function to the ascii art
        filtered_ascii_art = filter_output(ascii_art)

        # Print the filtered ascii art or a failure message
        if filtered_ascii_art:
            print(filtered_ascii_art)
        else:
            print("The agent failed to generate ASCII art.")

        return filtered_ascii_art
while True:
    try:
        num_artists = int(input("Enter the number of artists in the chain (including the FinalAgent): "))
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

object_to_draw = input("Enter the object to draw: ")

initial_prompt = f"create a detailed picture of a {object_to_draw}. Strictly use ASCII characters to represent the object minimize white space. Ensure that the art is within 80 characters across."

artists = [ArtistAgent() for _ in range(num_artists - 1)]

artist_arts = []
first_agent = ArtistAgent()
first_art = first_agent.generate_ascii_art(initial_prompt)
artist_arts.append(first_art)
print(first_art)

for i in range(num_artists - 2):
    artist = artists[i]
    prev_art = artist_arts[-1]
    artist_art = artist.generate_ascii_art(prev_art)
    artist_arts.append(artist_art)
    print(artist_art)

final_agent = ArtistAgent()
final_art = final_agent.generate_ascii_art(initial_prompt+artist_arts[-1])

print(final_art)



#                .--.
#          _ .-'    \
#        .` /       \
#        |  |  //\   |
#       /\ \/ //\ \ /
#      (\   \/`/ )/ /|
#       \(   \ ) / / |
#        \ \  <`/ /  |
#         `.`\ ` /`.\_/
#          '._'=_.'
#            /|_|\
#           //    \\
#           \\    //
#          `'    `'
