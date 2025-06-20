import torch
import torch.nn as nn
from torch.nn import functional as F

# Загружаем сохраненную модель и данные
checkpoint = torch.load('gpt_model.pth')
stoi = checkpoint['stoi']
itos = checkpoint['itos']
config = checkpoint['config']

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Копируем минимально необходимые классы из model.py
class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(config['n_embd'], head_size, bias=False)
        self.query = nn.Linear(config['n_embd'], head_size, bias=False)
        self.value = nn.Linear(config['n_embd'], head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(config['block_size'], config['block_size'])))
        self.dropout = nn.Dropout(0.0)

    def forward(self, x):
        B, T, C = x.shape
        k, q = self.key(x), self.query(x)
        wei = q @ k.transpose(-2, -1) * C**-0.5
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1)
        return wei @ self.value(x)

class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(config['n_embd'], config['n_embd'])
        self.dropout = nn.Dropout(0.0)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        return self.dropout(self.proj(out))

class FeedFoward(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(0.0),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        self.sa = MultiHeadAttention(n_head, n_embd // n_head)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        return x + self.ffwd(self.ln2(x))

class BigramLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(config['vocab_size'], config['n_embd'])
        self.position_embedding_table = nn.Embedding(config['block_size'], config['n_embd'])
        self.blocks = nn.Sequential(*[Block(config['n_embd'], config['n_head']) for _ in range(config['n_layer'])])
        self.ln_f = nn.LayerNorm(config['n_embd'])
        self.lm_head = nn.Linear(config['n_embd'], config['vocab_size'])

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        logits = self.lm_head(self.ln_f(x))
        return (logits, None) if targets is None else (logits, F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1)))

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -config['block_size']:]
            logits, _ = self(idx_cond)
            probs = F.softmax(logits[:, -1, :], dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx

# Создаем и загружаем модель
model = BigramLanguageModel().to(device)
model.load_state_dict(checkpoint['model_state'])
model.eval()

# Функция для генерации текста
def generate(prompt, max_tokens=200):
    context = torch.tensor([stoi[c] for c in prompt], dtype=torch.long, device=device).unsqueeze(0)
    generated = model.generate(context, max_new_tokens=max_tokens)
    return ''.join([itos[i] for i in generated[0].tolist()])

# Основной цикл
if __name__ == '__main__':
    while True:
        prompt = input("\nВведите начало текста (или 'exit' для выхода): ")
        if prompt.lower() == 'exit':
            break
        print("\nСгенерированный текст:")
        print(generate(prompt))