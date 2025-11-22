#  Este modelo será utilizado para resumir um texto.
from transformers import pipeline

pipe = pipeline(
    "summarization", model="facebook/bart-large-cnn", device="cpu"
)  # no meu caso estou tuilizando a cpu para processar as informações.

texto = """
    Greek (Modern Greek: Ελληνικά, romanized: Elliniká, [eliniˈka]; Ancient Greek: Ἑλληνική, romanized: Hellēnikḗ) is an Indo-European language, constituting an independent Hellenic branch within the Indo-European language family. It is native to Greece, Cyprus, Italy (in Calabria and Salento), southern Albania, and other regions of the Balkans, Caucasus, the Black Sea coast, Asia Minor, and the Eastern Mediterranean. It has the longest documented history of any Indo-European language, spanning at least 3,400 years of written records.[10] Its writing system is the Greek alphabet, which has been used for approximately 2,800 years;[11][12] previously, Greek was recorded in writing systems such as Linear B and the Cypriot syllabary.[13] The alphabet arose from the Phoenician script and was in turn the basis of the Latin, Cyrillic, Coptic, Gothic, and many other writing systems.

    The Greek language holds a very important place in the history of the Western world. Beginning with the epics of Homer, ancient Greek literature includes many works of lasting importance in the European canon. Greek is also the language in which many of the foundational texts in science and philosophy were originally composed. The New Testament of the Christian Bible was also originally written in Greek.[14][15] Together with the Latin texts and traditions of the Roman world, the Greek texts and Greek societies of antiquity constitute the objects of study of the discipline of Classics.

    During antiquity, Greek was by far the most widely spoken lingua franca in the Mediterranean world.[16] It eventually became the official language of the Byzantine Empire and developed into Medieval Greek.[17] In its modern form, Greek is the official language of Greece and Cyprus and one of the 24 official languages of the European Union. It is spoken by at least 13.5 million people today in Greece, Cyprus, Italy, Albania, Turkey, and the many other countries of the Greek diaspora.

    Greek roots have been widely used for centuries and continue to be widely used to coin new words in other languages; Greek and Latin are the predominant sources of international scientific vocabulary.
"""

resumo = pipe(texto)
print(f"Resposta: \n{resumo}")
