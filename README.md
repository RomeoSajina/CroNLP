# CroNLP - Croatian NLP project
Prikupljanje sadržaja sa stranica Wikipedije i evaluacija performansi modela Word2Vec, GloVe i FastText.


## Instalacija

```bash
git clone https://github.com/RomeoSajina/CroNLP.git
cd CroNLP
pip install -r requirements.txt
```


## Priprema teksta
Za prikupljanje tekstova sa Wikipedije je potrebno pokrenuti `prepare_data.py` sa parametrom `--terms` gdje je potrebno navesti zarezom odvojene nazive wiki stranica sa kojih će se tekst prikupiti.
**Info:** skripta odmah preuzima i sadržaj sa povezanih wiki stranica.


Npr.
```bash
python prepare_data.py --terms "Formula 1,Dodatak:Popis vozača u Formuli 1" --lang hr --output ./data/output.txt
```


## Evaluacija modela
Nakon pripreme podataka (i pripreme testa analogije) može se pokrenuti evaluacija modela:


Npr.
```bash
python eval.py --text ./data/f1_text.txt --test ./data/f1_test.txt
```

**Svi rezultati će biti zapisani u `info.log` datoteci.**

**Info:** korištenjem zastavice `--save` će se vektorske reprezentacije modela spremiti u direktorij *weights*, nakon čega se mogu vizualizirati preko [Embedding Projector](http://projector.tensorflow.org/)
