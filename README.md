# Skepya-AI-Helper

Skepya-AI-Helper este un proiect experimental care integrează componente AI pentru a ajuta la **migrarea codului** dintr-un limbaj de programare în altul. In alte cuvinte, este o alternativa la GitHub Copilot mai eficienta (prompt-urile sunt mai eficiente si timpul necesar developer-ului este redus in implementare) Este gândit ca un asistent inteligent capabil să proceseze, să înțeleagă și să transforme fragmente de cod, păstrând logica și relațiile dintre componente.

## 🔍 Funcționalități

- Împarte fișierele sursă în **chunks logice de cod** 
- Utilizează un mecanism **RAG (Retrieval-Augmented Generation)** pentru verificarea și traducerea codului (cu mici ajustari, raG-ul poate fi integrat si in functia de generare de cod)
- Menține **relațiile de dependență** între bucățile de cod
- Generează **cod nou**, inspirându-se din proiecte existente sau implementări similare
- Genereaza fisier Markdown care explica codul (a.k.a readme) fiind cu mult mai precis fata de un prompt basic)
- Functie de comentare a codului
- Genereaza teste pentru verificarea codului
- Uniformizeaza variabilele (dupa un case pe care il mentionezi si alege nume potrivite)

## 🧠 Tehnologii folosite

- **Python**
- **AI/LLM** pentru generare și validare de cod
- Posibilă integrare cu vector search și embeddings (de completat după caz)

## 🚀 Cum rulezi proiectul

1. Clonează repo-ul:
   ```bash
   git clone https://github.com/roscanrares/SKepya-AI-Helper.git

2. Se ruleaza fisierul ([main.py](https://github.com/roscanrares/Skepya-AI-Helper/blob/main/migration_and_splitting/main.py)) (se poate modifica dupa nevoi; fie ca e rulat ca script din terminal/alta aplicatie sau direct in IDE)
3. Se pot modifica si prompt-urile agentilor in functie de nevoi (migrarea este momentan gandita pentru C++ -> Java)
