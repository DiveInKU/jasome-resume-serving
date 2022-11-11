from typing import Optional
import torch
import transformers
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from fastai.text.all import *
import fastai
import re
from datetime import datetime


class DropOutput(Callback):
    def after_pred(self): self.learn.pred = self.pred[0]


class NLP:
    def __init__(self):
        # device = torch.device('cpu')
        self.categories = ['it', 'business', 'marketing', 'total']
        self.models = dict()
        for category in self.categories:
            self.models[category] = GPT2LMHeadModel.from_pretrained('./models/{}.pt'.format(category))
            print("{} 로딩 완료".format(category))
        # self.model = AutoModelWithLMHead.from_pretrained('./models/marketing/all_5epoch')
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", bos_token='</s>',
                                                                 eos_token='</s>',
                                                                 unk_token='<unk>', pad_token='<pad>',
                                                                 mask_token='<mask>')

    def generate(self, category="total", prompt="제가 가장 중요하게 생각하는 것은", number=1):
        result = set()
        while len(result) < number:
            input_ids = self.tokenizer.encode(prompt)
            gen_ids = self.models[category].generate(torch.tensor([input_ids]),
                                                     max_length=150,
                                                     repetition_penalty=2.0,
                                                     pad_token_id=self.tokenizer.pad_token_id,
                                                     eos_token_id=self.tokenizer.eos_token_id,
                                                     bos_token_id=self.tokenizer.bos_token_id,
                                                     use_cache=True,
                                                     temperature=1.1,
                                                     top_k=50,
                                                     top_p=0.8,
                                                     do_sample=True)
            generated = self.tokenizer.decode(gen_ids[0, :].tolist())
            if generated.strip() not in result:
                generated = generated.replace('\n', ' ')
                generated = re.sub(r'\s+', ' ', generated)
                # 마침표 빠진 경우 추가
                generated = generated.replace('니다 ', '니다. ')
                result.add(generated)
        return list(result)


if __name__ == '__main__':
    nlp = NLP()
    print(*nlp.generate('total', '제가 가장 중요하다고 생각하는 것은', 3), sep='\n')
    # nlp.save()
