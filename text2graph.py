import nltk
end = input('Input end string: ')
sentence = 'While writing program in any language, you need to use various variables to store various information.'
while sentence != end:
	print(sentence)
	tokens = nltk.word_tokenize(sentence)
	print(tokens)
	tagged = nltk.pos_tag(tokens)
	print(tagged)
	sentence = input('Enter "End" to stop: ')

from textblob import TextBlob

text = '''
An old king whose sight was failing heard of a garden with apples that would make a man grow young, and water that would restore his sight. His oldest son set out; he came to a pillar that said on one road, his horse would be full and he would be hungry, on the second, he would lose his life, and on the third, he would be full and his horse hungry. He took the third. He came to a house where a widow made him welcome and offered to let him spend the night with her daughter Dunia. He accepted, and Dunia made him fall into the cellar.

His second son set out and met the same fate. Finally the youngest son set out, over his father's reluctance. When he received the same offer from the widow, he said he must go to the bathhouse first; Dunia led him to it, and he beat her until she revealed his brothers. He freed them, but they were ashamed to go home.

He rode on and found a pretty maiden weaving. She could not direct him to the garden, but instead sent him on to her second sister. She bade him leave his horse with her and go on a two-winged horse to their third sister. The third sister gave him a four-winged horse and told him to ensure that it leapt the wall in a single bound, or it make bells ring and wake the witch. He tried to obey her, but the horse's hoof just grazed the wall. The sound was too soft to wake the witch. In the morning, she chased after him on her six-winged horse, but only caught him when he was near his own land and did not fear her. She cursed him, saying nothing would save him from his brothers.

He found his brothers sleeping and slept by them. They stole his apples and threw him over a cliff. He fell to a dark kingdom. There, a dragon demanded a beautiful maiden every year, and this year the lot had fallen on the princess. The knight said he would save her if the king would promise to do as he asked; the king promised not only that but to marry him to the princess as well. They went to where the dragon was coming and he went to sleep, telling the princess to wake him. The dragon came, she could not wake him and began to weep, and a tear fell on his face, waking him. He cut off the dragon's heads, put them under a rock, and threw its body in the sea.

Another man sneaked up behind him and cut off his head. He threatened to kill the princess if she would not say that he had killed the dragon. The king arranged for the marriage, but the princess went to sea with fishermen. Each time they caught a fish, she had them throw it back, but finally, their nets caught the knight's body and head. She put them back together and used the water of life on them. He comforted her and sent her home, saying he would come and make it right. He came and asked the king whether the alleged dragon slayer could find the dragon's heads. The imposter could not, but the knight could. The knight said he wanted only to go to his own country, not to marry the princess, but she did not want to be parted from him. She knew a spoonbilled bird that could carry them, if it had enough to eat. They went off with a whole ox, but it was not quite enough; the princess cut off part of her thigh to feed it. The bird carried them all the way and commented on the sweetness of the last piece of meat. She showed it what she had done, and it spat the piece back out; the knight used the water of life to restore it.

He went back with his father, used the water of life, and told him what his brothers had done. The brothers were so frightened they jumped in the river. The knight married the princess.
'''

blob = TextBlob(text)
blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                    #  ('threat', 'NN'), ('of', 'IN'), ...]

blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)
# 0.060
# -0.341

print(blob.translate(to="es"))
print(blob.translate(to="bg"))
