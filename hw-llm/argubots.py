"""This module contains argument bots. 
These agents should be able to handle a wide variety of topics and opponents.
They will be evaluated using methods in `eval.py`.
We've included a few to get your started."""

import logging
from dialogue import Dialogue
from openai import OpenAI
from tracking import default_client, default_model
from rich.logging import RichHandler
from pathlib import Path
import random
import glob
from agents import Agent, ConstantAgent, LLMAgent
from kialo import Kialo


# Use the same logger as agents.py, since argubots are agents;
# we split this file 
# You can change the logging level there.
log = logging.getLogger("agents")    

#############################
## Define some basic argubots
#############################

# Airhead (aka Absentia or Acephalic) always says the same thing.

airhead = ConstantAgent("Airhead", "I know right???")

# Alice is a basic prompted LLM.  You are trying to improve on Alice.
# Don't change the prompt -- instead, make a new argubot with a new prompt.

alice = LLMAgent("Alice",
                 system="You are an intelligent bot who wants to broaden your user's mind. "
                        "Ask a conversation starter question.  Then, WHATEVER "
                        "position the user initially takes, push back on it. "
                        "Try to help the user see the other side of the issue. "
                        "Answer in 1-2 sentences. Be thoughtful and polite.")

############################################################
## Other argubot classes and instances -- add your own here! 
############################################################

class KialoAgent(Agent):
    """ KialoAgent subclasses the Agent class. It responds with a relevant claim from
    a Kialo database.  No LLM is used."""
    
    def __init__(self, name: str, kialo: Kialo):
        self.name = name
        self.kialo = kialo
                
    def response(self, d: Dialogue) -> str:

        if len(d) == 0:   
            # First turn.  Just start with a random claim from the Kialo database.
            claim = self.kialo.random_chain()[0]
        else:
            previous_turn = d[-1]['content']  # previous turn from user
            # Pick one of the top-3 most similar claims in the Kialo database,
            # restricting to the ones that list "con" arguments (counterarguments).
            neighbors = self.kialo.closest_claims(previous_turn, n=3, kind='has_cons')
            assert neighbors, "No claims to choose from; is Kialo data structure empty?"
            neighbor = random.choice(neighbors)
            log.info(f"[black on bright_green]Chose similar claim from Kialo:\n{neighbor}[/black on bright_green]")
            
            # Choose one of its "con" arguments as our response.
            claim = random.choice(self.kialo.cons[neighbor])
        
        return claim    
    
# Akiko doesn't use an LLM, but looks up an argument in a database.
  
akiko = KialoAgent("Akiko", Kialo(glob.glob("data/*.txt")))   # get the Kialo database from text files


###########################################
# Define your own additional argubots here!
###########################################

class AkikiAgent(KialoAgent):

    def response(self, d: Dialogue) -> str:
        
        if len(d) == 0:
            # First turn, return random claim
            return super().response(d)
        
        # Get last user utterance
        last_turn = d[-1]['content']
        
        if self.kialo.closest_claims(last_turn, n=1):
            # If good match found, return that
            return super().response(d)
            
        # Otherwise, construct weighted query
        # Weigh last 3 user turns as 0.6, 0.3, 0.1
        query = ""
        for i in range(1,4):
            turn = d[-i]['content']
            weight = [0.6, 0.3, 0.1][i-1]
            query += f"{turn}^{weight} "
            
        # Retrieve with weighted query 
        matches = self.kialo.closest_claims(query, n=3, kind='has_cons')
        
        if not matches:
            # Fallback to random claim
            return super().response(d)
            
        # Pick a random match 
        match = random.choice(matches)
        response = random.choice(self.kialo.cons[match])
            
        return response
    
akiki = AkikiAgent("Akiki", Kialo(glob.glob("data/*.txt")))

class RAGAgent(Agent):

    def __init__(self, name: str, kialo: Kialo,client: OpenAI = default_client, model: str = default_model):
        self.name = name
        self.kialo = kialo
        self.client = client
        self.model = model
        self.conversation_starters = ['Do you think Donald Trump was a good president?']
        
    def paraphrase(self, d: Dialogue) -> str:
        script = d.script()
        responder = d[-1]['speaker']
        
        response = self.client.chat.completions.create(
            messages=[
            {"role": "system", "content": f"""
             paraphrase his sentence {self.name}.
            i need a better version of it. 
            Try to understand what the user is saying. 
            try to see what the user is implying.
            sometimes user can use sarcasm, slang, or other forms of language.
            try to understand what the user is saying.
            The provided dialogue:
            {script}"""}], model=self.model)
        
        content = response.choices[0].message.content
        if f'{responder}:' in content:
            return content[content.find(f'{responder}:')+len(responder)+1:].strip()
        return content
    
    def retrieve(self, claim: str) -> str:
        gap = '\n\t* '
        claims = self.kialo.closest_claims(claim, kind='has_cons', n=3)
        
        result = f'claims:{gap}' + gap.join(claims)
        pros = ''
        cons = ''
        
        for c in claims:
            if self.kialo.pros[c]: pros += gap + gap.join(self.kialo.pros[c])
            if self.kialo.cons[c]: cons += gap + gap.join(self.kialo.cons[c])
            
        if len(pros): result += '\nfavor' + pros
        if len(cons): result += '\nagainst' + cons
        
        return result
        
    def response(self, d: Dialogue) -> str:
        claim = self.paraphrase(d)
        all_claims = self.retrieve(claim)
        
        response = self.client.chat.completions.create(
            messages=[
            {'role': 'system',
            'content': f'''
            You are an intelligent bot who aims to provide nuanced responses by combining curated information and generated content.
            Ask the LLM for an explicit claim based on the user's statement, then retrieve relevant information from Kialo to augment your response. 
            Push back on the user's position, broaden their perspective, and engage in thoughtful debate. 
            Your responses should be informed by both the dialogue context and curated information.
            you make use of the previous facts about the users and use them.
            these facts are from the kiolo database. Use these facts to make your response.
            {all_claims}
            '''}], model=self.model)
        
        return response.choices[0].message.content
        
    
aragorn = RAGAgent("Aragorn", Kialo(glob.glob('data/*.txt')))

class AwesmeAgent(RAGAgent):

    def __init__(self, name: str, kialo: Kialo,client: OpenAI = default_client, model: str = default_model):
        self.name = name
        self.kialo = kialo
        self.client = client
        self.model = model
        self.conversation_starters = ['Do you think Donald Trump was a good president?']
        
    def paraphraseChain(self, d: Dialogue) -> str:
        script = d.script()
        responder = d[-1]['speaker']
        
        response = self.client.chat.completions.create(
            messages=[
            {"role": "system", "content": f"""
             paraphrase his sentence {self.name}.
            i need a better version of it. 
            The provided dialogue:
            {script} also think to urself about what to speck beofre talking to other person"""}], model=self.model)
        
        content = response.choices[0].message.content
        if f'{responder}:' in content:
            return content[content.find(f'{responder}:')+len(responder)+1:].strip()
        return content
    
    def retrieve(self, claim: str) -> str:
        gap = '\n\t* '
        claims = self.kialo.closest_claims(claim, kind='has_cons', n=3)
        
        result = f'claims:{gap}' + gap.join(claims)
        pros = ''
        cons = ''
        
        for c in claims:
            if self.kialo.pros[c]: pros += gap + gap.join(self.kialo.pros[c])
            if self.kialo.cons[c]: cons += gap + gap.join(self.kialo.cons[c])
            
        if len(pros): result += '\nfavor' + pros
        if len(cons): result += '\nagainst' + cons
        
        return result
        
    def response(self, d: Dialogue) -> str:
        claim = self.paraphraseChain(d)
        all_claims = self.retrieve(claim)
        
        response = self.client.chat.completions.create(
            messages=[
            {'role': 'system',
            'content': f'''
             Use these facts to make your response.
            {all_claims}
            you also use previous facts about the user to make your response.
            '''}], model=self.model)
        
        return response.choices[0].message.content
        

awesme = AwesmeAgent("Awesme", Kialo(glob.glob('data/*.txt')))