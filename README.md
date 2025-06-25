
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

* Uses **BM25** for fast, interpretable retrieval of debate claims.
* Incorporates **semantic paraphrasing** to improve retrieval relevance.
* Combines curated debate knowledge with generative LLM power.
* Maintains conversation context for more coherent, on-topic replies.
* Evaluated with automated metrics and human judges to compare bot performance.

