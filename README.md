
# Debate Chatbots: Akiko, Akiki & Aragorn

Welcome to the Debate Chatbots repository! This project implements intelligent debate agents that combine retrieval-based and generation-based techniques to engage in meaningful, context-aware discussions.

---

## Overview

This repo contains three main chatbot agents designed for debate-style conversations using the **Kialo debate corpus**:

### 🤖 Akiko — The Basic Retrieval Bot

* Retrieves claims and counterarguments using **BM25** based on the user’s last message.
* Responds with a counterargument (“con”) to challenge the user.
* Limitations: Only single-turn context, no deep understanding, strictly retrieval-based.

### 🤖 Akiki — The Context-Aware Retrieval Bot

* Improves on Akiko by using a **weighted query of the last 3 user turns** for retrieval.
* Better handles vague or short inputs.
* Still purely retrieval-based with no generation.

### 🌟 Aragorn — The Retrieval-Augmented Generation (RAG) Agent

* Combines retrieval with Large Language Models (LLM).
* **Step 1:** Uses an LLM to paraphrase the user’s last statement into a clear, explicit claim.
* **Step 2:** Retrieves relevant claims and pros/cons from Kialo based on the paraphrase.
* **Step 3:** Uses an LLM again to generate a nuanced, context-aware response informed by retrieved data.
* Benefits: Fact-based, flexible, understands user intent, and generates natural responses.

---

## Features

* Uses **BM25 and FAISS** for fast, interpretable retrieval of debate claims.
* Incorporates **semantic paraphrasing** to improve retrieval relevance.
* Combines curated debate knowledge with generative LLM power.
* Maintains conversation context for more coherent, on-topic replies.
* Evaluated with automated metrics and human judges to compare bot performance.
  
---

## Characters in the System

* **Alice:** Pure LLM-based chatbot, generates responses without retrieval grounding.
* **Akiko:** Basic single-turn retrieval bot (no LLM).
* **Akiki:** Multi-turn retrieval bot using weighted query (no LLM).
* **Aragorn:** RAG bot combining retrieval and LLM generation.
* **Shorty:** Simulated user for evaluation conversations.
* **Judge Wise:** Automated judge bot that scores dialogue quality and topic relevance.

---

## Evaluation

* Evaluate bot responses using the function `eval.eval_on_characters()`.
* Bots converse with simulated users (e.g., Shorty).
* Judge Wise scores responses based on:

  * How well the bot stays on topic.
  * Response relevance and informativeness.
  * Coherence and engagement.
* Typically, Aragorn outperforms pure retrieval bots (Akiko, Akiki) and pure LLM bots (Alice) by balancing grounded knowledge and generative flexibility.
* Evaluation can be done on different simulated characters to reveal bot strengths and weaknesses.

  ## Kialo claims

  <img width="350" alt="image" src="https://github.com/user-attachments/assets/e8020d5b-3403-4284-9999-42d5cb2d89dd" />

