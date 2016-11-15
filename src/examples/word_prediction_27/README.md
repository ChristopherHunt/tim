NOTE: this development is done in Python2.7

I found some examples that were in 2.7 so I have just been going with that for now.

This code trains/loads a model. Once loaded it feeds a single word, then just check the max value of the logits matrix to get a word id.

Then the id_to_word dictionary is used to look up the id.

Only the small model is currently trained. I will try to trian the large model overnight.

To run the code:

    python ptb_word_lm.py --data_path=data/ --checkpoint_dir=small_model/

